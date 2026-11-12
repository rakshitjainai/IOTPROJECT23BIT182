# 🌐 AeroSense IoT: ESP32 Climate & Air Quality Real-Time System

A complete IoT system with **ESP32**, **AHT21** (Temperature & Humidity), **ENS160** (AQI, TVOC, eCO2), **FastAPI** backend, and a modern **HD React Dashboard** communicating over **MQTT**.

---

## ⚡ Quick Start: Running the Project Locally

### Option A: One-Click Launcher (Recommended)
Simply double-click:
📁 **`run_servers.bat`** in the project folder.

It will automatically:
1. Verify backend Python venv and frontend node_modules.
2. Launch the **FastAPI Backend** on port `8000`.
3. Launch the **React HD Dashboard** on port `5173`.
4. Automatically open your default browser to [http://localhost:5173](http://localhost:5173).

To stop all servers at any time, simply double-click 📁 **`stop_servers.bat`** or close the terminal windows.

---

### Option B: Manual Terminal Launch:
1. **Start the FastAPI Backend:**
   ```bash
   cd backend
   .\.venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Start the React Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

---

## 🔌 Hardware Wiring & Pinout

Connect your sensors to your ESP32 board using the standard shared I2C pins:

| Sensor / Actuator Pin | ESP32 Pin | Purpose |
| :--- | :--- | :--- |
| **VCC (AHT21 & ENS160)** | **3V3** | 3.3V Power (Do not use 5V!) |
| **GND (AHT21 & ENS160)** | **GND** | Ground |
| **SDA (AHT21 & ENS160)** | **GPIO 21** | I2C Data Line (Shared) |
| **SCL (AHT21 & ENS160)** | **GPIO 22** | I2C Clock Line (Shared) |
| **LED** | **GPIO 2** | Built-in Blue LED (or external LED) |

---

## 🚀 Flashing the ESP32 Firmware

The firmware code is located at:
`firmware/esp32_iot_node/esp32_iot_node.ino`

### Key Features of the Firmware:
- **Smart Sensor Auto-Detection & Fallback Simulation:**
  At boot, the ESP32 checks for the physical AHT21 (`0x38`) and ENS160 (`0x53`) on the I2C bus.
  If the sensors are **not connected**, it automatically falls back to generating realistic simulated sensor data!
  This means you can test your ESP32 Wi-Fi, MQTT connectivity, and LED control immediately without waiting for sensors.
- **ENS160 Precision Compensation:**
  When physical sensors are connected, live Temperature and Humidity from AHT21 are injected into ENS160 for high-accuracy gas measurements.
- **MQTT Auto-Reconnect & LWT:**
  Includes Last-Will-and-Testament so the dashboard knows immediately when the ESP32 goes offline or comes online.

### Steps to Flash via Arduino IDE:
1. Open `firmware/esp32_iot_node/esp32_iot_node.ino` in **Arduino IDE**.
2. Install the required libraries in **Tools -> Manage Libraries**:
   - `PubSubClient` by Nick O'Leary
   - `ArduinoJson` by Benoit Blanchon
   - `Adafruit AHTX0` (for physical AHT21)
   - `ScioSense_ENS160` (for physical ENS160)
3. Set your mobile phone Wi-Fi hotspot credentials in the sketch:
   ```cpp
   const char* WIFI_SSID     = "YOUR_PHONE_HOTSPOT_NAME";
   const char* WIFI_PASSWORD = "YOUR_HOTSPOT_PASSWORD";
   ```
4. Select **Tools -> Board -> ESP32 Arduino -> ESP32 Dev Module**, choose your COM port, and click **Upload**.
5. Open the **Serial Monitor** at **115200 baud** to see real-time connection status!

---

## 📡 MQTT Topics Summary

| Topic | Direction | Payload Example | Description |
| :--- | :--- | :--- | :--- |
| `iot/sensors/data` | ESP32 ➔ Backend | `{"temperature": 26.2, "humidity": 52.4, "tvoc": 80, "eco2": 450, "aqi": 1}` | Live sensor readings |
| `iot/actuators/led/set` | Backend ➔ ESP32 | `{"state": true}` | Turn LED ON/OFF |
| `iot/actuators/led/status` | ESP32 ➔ Backend | `{"led_state": true}` | State confirmation |
| `iot/device/status` | ESP32 ➔ Backend | `{"status": "online"}` / `{"status": "offline"}` | Device heartbeat & LWT |
