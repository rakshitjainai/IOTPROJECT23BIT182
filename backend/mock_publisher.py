"""
Standalone MQTT Mock ESP32 Publisher
Simulates a physical ESP32 broadcasting real-time AHT21 and ENS160 sensor telemetry
and listening to LED commands over MQTT.
"""

import json
import logging
import random
import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("esp32_simulator")

led_state = False

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info(f"ESP32 Simulator connected to broker: {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
        # Subscribe to LED commands
        client.subscribe(settings.TOPIC_LED_SET)
        logger.info(f"Subscribed to LED command topic: {settings.TOPIC_LED_SET}")
        
        # Publish online status (LWT will publish offline if terminated abruptly)
        client.publish(settings.TOPIC_DEVICE_STATUS, json.dumps({"status": "online", "device_id": "esp32_sim_hardware"}), retain=True)
    else:
        logger.error(f"Failed to connect to broker, return code: {rc}")

def on_message(client, userdata, msg):
    global led_state
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        if "state" in data:
            led_state = bool(data["state"])
            logger.info(f">>> [ESP32 HARDWARE EVENT] LED physical state toggled: {'ON' if led_state else 'OFF'}")
            # Acknowledge back on LED status topic
            client.publish(settings.TOPIC_LED_STATUS, json.dumps({"led_state": led_state}))
    except Exception as e:
        logger.error(f"Error handling incoming MQTT message: {e}")

def main():
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id="esp32_hardware_simulator_01"
    )
    
    # Configure Last Will and Testament
    lwt_payload = json.dumps({"status": "offline", "device_id": "esp32_sim_hardware"})
    client.will_set(settings.TOPIC_DEVICE_STATUS, lwt_payload, qos=1, retain=True)

    client.on_connect = on_connect
    client.on_message = on_message

    logger.info(f"Connecting to broker {settings.MQTT_BROKER}...")
    client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    client.loop_start()

    temp = 26.2
    hum = 52.4
    tvoc = 50
    eco2 = 430
    uptime = 0

    try:
        while True:
            uptime += 2
            # Sensor value fluctuations
            temp = round(temp + random.uniform(-0.25, 0.25), 1)
            temp = max(19.0, min(36.0, temp))

            hum = round(hum + random.uniform(-0.5, 0.5), 1)
            hum = max(35.0, min(80.0, hum))

            tvoc = max(15, min(800, tvoc + random.randint(-12, 15)))
            eco2 = max(400, min(2000, eco2 + random.randint(-18, 22)))

            if tvoc < 65 and eco2 < 600:
                aqi = 1
                aqi_status = "Excellent"
            elif tvoc < 220 and eco2 < 800:
                aqi = 2
                aqi_status = "Good"
            elif tvoc < 660 and eco2 < 1200:
                aqi = 3
                aqi_status = "Moderate"
            elif tvoc < 2200 and eco2 < 1600:
                aqi = 4
                aqi_status = "Poor"
            else:
                aqi = 5
                aqi_status = "Unhealthy"

            payload = {
                "device_id": "esp32_sim_hardware",
                "temperature": temp,
                "humidity": hum,
                "tvoc": tvoc,
                "eco2": eco2,
                "aqi": aqi,
                "aqi_status": aqi_status,
                "is_simulated": True,
                "led_state": led_state,
                "wifi_rssi": -55 + random.randint(-2, 2),
                "uptime_sec": uptime
            }

            client.publish(settings.TOPIC_TELEMETRY, json.dumps(payload))
            logger.info(f"Published Telemetry: Temp={temp}C, Hum={hum}%, AQI={aqi} ({aqi_status}), LED={'ON' if led_state else 'OFF'}")
            time.sleep(2.5)

    except KeyboardInterrupt:
        logger.info("Stopping ESP32 simulator...")
        client.publish(settings.TOPIC_DEVICE_STATUS, json.dumps({"status": "offline"}), retain=True)
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
