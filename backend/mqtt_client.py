import json
import logging
import time
import asyncio
from typing import Callable, Any, List
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from config import settings

logger = logging.getLogger("mqtt_service")
logging.basicConfig(level=logging.INFO)

class MQTTService:
    def __init__(self):
        self.client: mqtt.Client | None = None
        self.is_connected = False
        self.latest_telemetry: dict[str, Any] | None = None
        self.telemetry_history: list[dict[str, Any]] = []
        self.led_state: bool = False
        self.device_online: bool = False
        self.last_seen: float | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self.subscribers: List[Callable[[dict[str, Any]], Any]] = []

    def register_callback(self, callback: Callable[[dict[str, Any]], Any]):
        """Register an async callback invoked whenever new telemetry or state arrives."""
        self.subscribers.append(callback)

    def _notify_subscribers(self, message_type: str, data: Any):
        """Dispatches event to async subscribers safely on the event loop."""
        if not self.loop or not self.loop.is_running():
            return
        
        payload = {
            "type": message_type,
            "data": data,
            "timestamp": time.time(),
            "device_online": self.device_online,
            "led_state": self.led_state
        }

        for cb in self.subscribers:
            try:
                asyncio.run_coroutine_threadsafe(cb(payload), self.loop)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

    def on_connect(self, client, userdata, flags, rc, *args, **kwargs):
        if rc == 0:
            self.is_connected = True
            logger.info(f"Connected to MQTT Broker: {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
            # Subscribe to relevant topics
            client.subscribe(settings.TOPIC_TELEMETRY)
            client.subscribe(settings.TOPIC_LED_STATUS)
            client.subscribe(settings.TOPIC_DEVICE_STATUS)
            logger.info(f"Subscribed to topics: {settings.TOPIC_TELEMETRY}, {settings.TOPIC_LED_STATUS}, {settings.TOPIC_DEVICE_STATUS}")
            self._notify_subscribers("broker_status", {"status": "connected", "broker": settings.MQTT_BROKER})
        else:
            self.is_connected = False
            logger.error(f"Failed to connect to MQTT Broker, return code {rc}")
            self._notify_subscribers("broker_status", {"status": "error", "code": rc})

    def on_disconnect(self, client, userdata, *args, **kwargs):
        self.is_connected = False
        logger.warning("Disconnected from MQTT Broker")
        self._notify_subscribers("broker_status", {"status": "disconnected"})

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
        except Exception:
            # Fallback for plain string / boolean messages
            payload_str = msg.payload.decode("utf-8", errors="ignore").strip()
            data = {"raw": payload_str}

        logger.debug(f"Received MQTT [{topic}]: {data}")

        if topic == settings.TOPIC_TELEMETRY:
            self.device_online = True
            self.last_seen = time.time()
            data["server_timestamp"] = self.last_seen
            self.latest_telemetry = data
            
            # Append to in-memory history buffer
            self.telemetry_history.append(data)
            if len(self.telemetry_history) > settings.HISTORY_BUFFER_SIZE:
                self.telemetry_history.pop(0)

            # Sync led state if reported in telemetry
            if "led_state" in data:
                self.led_state = bool(data["led_state"])

            self._notify_subscribers("telemetry", data)

        elif topic == settings.TOPIC_LED_STATUS:
            if isinstance(data, dict) and "led_state" in data:
                self.led_state = bool(data["led_state"])
            elif isinstance(data, dict) and "state" in data:
                self.led_state = bool(data["state"])
            elif payload_str.lower() in ("true", "1", "on"):
                self.led_state = True
            elif payload_str.lower() in ("false", "0", "off"):
                self.led_state = False
            
            logger.info(f"ESP32 confirmed LED state: {self.led_state}")
            self._notify_subscribers("led_status", {"led_state": self.led_state})

        elif topic == settings.TOPIC_DEVICE_STATUS:
            status_val = data.get("status") if isinstance(data, dict) else payload_str
            if status_val == "online":
                self.device_online = True
                self.last_seen = time.time()
            elif status_val == "offline":
                self.device_online = False
            
            logger.info(f"ESP32 LWT Status changed: {status_val}")
            self._notify_subscribers("device_status", {"device_online": self.device_online, "status": status_val})

    def start(self, loop: asyncio.AbstractEventLoop):
        """Initializes and starts the non-blocking MQTT client network loop."""
        self.loop = loop
        self.client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=settings.MQTT_CLIENT_ID
        )

        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        try:
            logger.info(f"Attempting to connect to MQTT broker {settings.MQTT_BROKER}:{settings.MQTT_PORT}...")
            self.client.connect_async(settings.MQTT_BROKER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to start MQTT loop: {e}")

    def stop(self):
        """Stops the MQTT client loop."""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT Client stopped")

    def publish_led(self, state: bool) -> bool:
        """Publishes LED command payload to ESP32."""
        if not self.client:
            logger.warning("Cannot publish LED command: MQTT client is not initialized")
            return False

        payload = json.dumps({"state": state})
        info = self.client.publish(settings.TOPIC_LED_SET, payload, qos=1)
        self.led_state = state  # Optimistic local update
        self._notify_subscribers("led_status", {"led_state": self.led_state, "pending": True})
        logger.info(f"Published LED command to {settings.TOPIC_LED_SET}: {payload} (rc={info.rc})")
        return info.rc == mqtt.MQTT_ERR_SUCCESS

    def inject_mock_reading(self, reading: dict[str, Any]):
        """Allows backend or test simulator to inject reading as if received from MQTT."""
        self.device_online = True
        self.last_seen = time.time()
        reading["server_timestamp"] = self.last_seen
        self.latest_telemetry = reading
        self.telemetry_history.append(reading)
        if len(self.telemetry_history) > settings.HISTORY_BUFFER_SIZE:
            self.telemetry_history.pop(0)
        if "led_state" in reading:
            self.led_state = bool(reading["led_state"])
        self._notify_subscribers("telemetry", reading)

mqtt_service = MQTTService()
