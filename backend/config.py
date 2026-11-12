import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # MQTT Broker Configuration
    # Defaults to broker.emqx.io for instant zero-configuration testing over mobile hotspot.
    # Can be changed to "localhost" or local laptop IP (e.g. 192.168.43.x) if using local Mosquitto.
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "broker.emqx.io")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    MQTT_KEEPALIVE: int = int(os.getenv("MQTT_KEEPALIVE", 60))
    MQTT_USERNAME: str | None = os.getenv("MQTT_USERNAME", None)
    MQTT_PASSWORD: str | None = os.getenv("MQTT_PASSWORD", None)

    # Topics (unique project namespace to avoid collision on public brokers)
    TOPIC_TELEMETRY: str = os.getenv("TOPIC_TELEMETRY", "aerosense_iot/sensors/data")
    TOPIC_LED_SET: str = os.getenv("TOPIC_LED_SET", "aerosense_iot/actuators/led/set")
    TOPIC_LED_STATUS: str = os.getenv("TOPIC_LED_STATUS", "aerosense_iot/actuators/led/status")
    TOPIC_DEVICE_STATUS: str = os.getenv("TOPIC_DEVICE_STATUS", "aerosense_iot/device/status")

    # Client identifier
    MQTT_CLIENT_ID: str = os.getenv("MQTT_CLIENT_ID", "aerosense_fastapi_backend_99")

    # FastAPI Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    # In-memory history buffer size for dashboard charts
    HISTORY_BUFFER_SIZE: int = 50

settings = Settings()
