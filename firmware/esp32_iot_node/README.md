# ESP32 Firmware Guide: AHT21 + ENS160 Air Quality Station & LED Control

## 1. Overview
This firmware runs on any standard ESP32 development board (NodeMCU-32S, ESP32-WROOM-32, etc.).
It connects to your mobile phone Wi-Fi hotspot, reads environmental metrics from **AHT21** & **ENS160**, controls an **LED**, and exchanges real-time data over **MQTT**.

### Smart Sensor Fallback Feature:
If the sensor board is **not connected** or disconnected, the ESP32 automatically detects this via an I2C bus scan at boot and **seamlessly switches to realistic simulated data**. 
- You can test your ESP32 board, Wi-Fi, MQTT communication, and LED toggling immediately, even before you wire your sensors!
- Once you wire the sensors and reboot, it automatically locks onto the real sensors.

---

## 2. Hardware Wiring

| Sensor / Component Pin | ESP32 Pin | Function | Description |
| :--- | :--- | :--- | :--- |
| **VCC (AHT21 & ENS160)** | **3V3** | Power (3.3V) | Connect to 3.3V output (Do not use 5V!) |
| **GND (AHT21 & ENS160)** | **GND** | Ground | Common Ground |
| **SDA (AHT21 & ENS160)** | **GPIO 21** | I2C Data | Shared bus between both sensors |
| **SCL (AHT21 & ENS160)** | **GPIO 22** | I2C Clock | Shared bus between both sensors |
| **LED Anode (+)** | **GPIO 2** (or 4) | Actuator | Built-in blue LED or external LED |
| **LED Cathode (-)** | **GND** via 220Ω | Ground | Required if using external LED |

---

## 3. Required Arduino IDE Libraries

Open **Arduino IDE** -> **Sketch** -> **Include Library** -> **Manage Libraries...** and install:

1. **`PubSubClient`** by Nick O'Leary (for MQTT communication)
2. **`ArduinoJson`** by Benoit Blanchon (Version 6.x or 7.x)
3. **`Adafruit AHTX0`** by Adafruit (for AHT21 temperature & humidity)
4. **`ScioSense_ENS160`** by ScioSense (for ENS160 air quality sensor)

*(Note: If you do not install the sensor libraries yet, the sketch will still compile and run the smart simulated fallback!)*

---

## 4. Configuration in `esp32_iot_node.ino`

Open `esp32_iot_node.ino` in Arduino IDE and set your Wi-Fi hotspot details:

```cpp
const char* WIFI_SSID     = "YOUR_MOBILE_HOTSPOT_NAME";
const char* WIFI_PASSWORD = "YOUR_HOTSPOT_PASSWORD";

// MQTT Broker (Matches your FastAPI backend & React Dashboard)
// Default is the public broker broker.emqx.io (zero-setup)
const char* MQTT_BROKER   = "broker.emqx.io";
const int   MQTT_PORT     = 1883;
```

---

## 5. Uploading to ESP32

1. Connect your ESP32 to your PC via Micro-USB or USB-C cable.
2. In Arduino IDE:
   - Go to **Tools** -> **Board** -> **ESP32 Arduino** -> Select **ESP32 Dev Module** (or your specific ESP32 model).
   - Go to **Tools** -> **Port** -> Select the COM port of your ESP32 (e.g. `COM3`, `COM5`).
   - Go to **Tools** -> **Upload Speed** -> `921600` or `115200`.
3. Click **Upload** (arrow icon).
4. Open **Serial Monitor** at **115200 baud** to view real-time logs, Wi-Fi connection, and MQTT publish activity!
