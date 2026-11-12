import asyncio
import json
import logging
import random
import time
from contextlib import asynccontextmanager
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import settings
from mqtt_client import mqtt_service

logger = logging.getLogger("fastapi_app")

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        
        dead_connections = set()
        text_data = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(text_data)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                dead_connections.add(connection)
        
        for dead in dead_connections:
            self.active_connections.discard(dead)

manager = ConnectionManager()

# Background Mock Sensor Generator (optional feature for instant previewing)
simulation_running = False
sim_task: asyncio.Task | None = None

async def mock_telemetry_generator():
    """Generates realistic telemetry if simulation is activated."""
    global simulation_running
    logger.info("Mock telemetry simulator loop started.")
    
    temp = 25.0
    hum = 55.0
    tvoc = 65
    eco2 = 420
    uptime = 0

    while simulation_running:
        uptime += 2
        # Smooth random walk
        temp = round(temp + random.uniform(-0.3, 0.3), 1)
        temp = max(18.0, min(38.0, temp))

        hum = round(hum + random.uniform(-0.8, 0.8), 1)
        hum = max(30.0, min(85.0, hum))

        tvoc = int(max(10, min(600, tvoc + random.randint(-15, 18))))
        eco2 = int(max(400, min(1800, eco2 + random.randint(-20, 25))))

        # AQI calculation (1-5 according to standard ENS160 classification)
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

        reading = {
            "device_id": "esp32_station_sim",
            "temperature": temp,
            "humidity": hum,
            "tvoc": tvoc,
            "eco2": eco2,
            "aqi": aqi,
            "aqi_status": aqi_status,
            "is_simulated": True,
            "led_state": mqtt_service.led_state,
            "wifi_rssi": -52 + random.randint(-3, 3),
            "uptime_sec": uptime
        }
        
        mqtt_service.inject_mock_reading(reading)
        await asyncio.sleep(2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start MQTT client with current asyncio loop
    loop = asyncio.get_running_loop()
    
    async def on_mqtt_event(payload: dict):
        await manager.broadcast(payload)
        
    mqtt_service.register_callback(on_mqtt_event)
    mqtt_service.start(loop)
    
    yield
    
    # Shutdown
    global simulation_running, sim_task
    simulation_running = False
    if sim_task:
        sim_task.cancel()
    mqtt_service.stop()

app = FastAPI(
    title="IoT ESP32 Real-Time Station API",
    description="FastAPI Backend for ESP32 + AHT21 + ENS160 MQTT Telemetry & LED Control",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware to allow React frontend (Vite dev server) to connect seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class LedCommand(BaseModel):
    state: bool

class SimulationToggle(BaseModel):
    enable: bool

# REST Endpoints
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "IoT ESP32 Backend",
        "broker": settings.MQTT_BROKER,
        "broker_connected": mqtt_service.is_connected,
        "device_online": mqtt_service.device_online,
        "ws_endpoint": "/ws/telemetry"
    }

@app.get("/api/status")
def get_status():
    device_online = mqtt_service.device_online
    # Auto-flag as offline if no message received in last 12 seconds
    if mqtt_service.last_seen and (time.time() - mqtt_service.last_seen > 12) and not simulation_running:
        device_online = False
        mqtt_service.device_online = False

    return {
        "broker": settings.MQTT_BROKER,
        "broker_port": settings.MQTT_PORT,
        "broker_connected": mqtt_service.is_connected,
        "device_online": device_online,
        "last_seen": mqtt_service.last_seen,
        "led_state": mqtt_service.led_state,
        "simulation_running": simulation_running,
        "history_count": len(mqtt_service.telemetry_history),
        "topics": {
            "telemetry": settings.TOPIC_TELEMETRY,
            "led_set": settings.TOPIC_LED_SET,
            "led_status": settings.TOPIC_LED_STATUS,
            "device_status": settings.TOPIC_DEVICE_STATUS
        }
    }

@app.get("/api/telemetry/latest")
def get_latest_telemetry():
    if not mqtt_service.latest_telemetry:
        raise HTTPException(status_code=404, detail="No telemetry data received yet")
    return mqtt_service.latest_telemetry

@app.get("/api/telemetry/history")
def get_telemetry_history():
    return {
        "count": len(mqtt_service.telemetry_history),
        "data": mqtt_service.telemetry_history
    }

@app.post("/api/led")
def set_led_state(cmd: LedCommand):
    success = mqtt_service.publish_led(cmd.state)
    return {
        "success": success,
        "led_state": cmd.state,
        "topic": settings.TOPIC_LED_SET
    }

@app.post("/api/simulation/toggle")
async def toggle_simulation(cmd: SimulationToggle):
    global simulation_running, sim_task
    if cmd.enable and not simulation_running:
        simulation_running = True
        sim_task = asyncio.create_task(mock_telemetry_generator())
        return {"simulation_running": True, "message": "Simulation started"}
    elif not cmd.enable and simulation_running:
        simulation_running = False
        if sim_task:
            sim_task.cancel()
        return {"simulation_running": False, "message": "Simulation stopped"}
    return {"simulation_running": simulation_running}

# WebSocket Endpoint
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    global simulation_running, sim_task
    await manager.connect(websocket)
    try:
        # Send initial full state bundle so dashboard immediately renders without waiting for next tick
        init_message = {
            "type": "init",
            "data": {
                "latest": mqtt_service.latest_telemetry,
                "history": mqtt_service.telemetry_history,
                "led_state": mqtt_service.led_state,
                "device_online": mqtt_service.device_online,
                "broker_connected": mqtt_service.is_connected,
                "broker": settings.MQTT_BROKER,
                "simulation_running": simulation_running
            },
            "timestamp": time.time()
        }
        await websocket.send_text(json.dumps(init_message))

        # Handle incoming commands over WebSocket from the dashboard
        while True:
            raw_text = await websocket.receive_text()
            try:
                msg = json.loads(raw_text)
                action = msg.get("action")
                if action == "toggle_led":
                    state = bool(msg.get("state", not mqtt_service.led_state))
                    mqtt_service.publish_led(state)
                    await manager.broadcast({
                        "type": "led_status",
                        "data": {"led_state": state},
                        "timestamp": time.time()
                    })
                elif action == "toggle_sim":
                    simulation_running = not simulation_running
                    if simulation_running:
                        sim_task = asyncio.create_task(mock_telemetry_generator())
                    elif sim_task:
                        sim_task.cancel()
                    await manager.broadcast({
                        "type": "simulation_status",
                        "data": {"simulation_running": simulation_running},
                        "timestamp": time.time()
                    })
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket unexpected error: {e}")
        manager.disconnect(websocket)
