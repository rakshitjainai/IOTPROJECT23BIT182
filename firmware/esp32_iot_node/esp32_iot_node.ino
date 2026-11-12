/*
 * ======================================================================================
 * Project: AeroSense IoT — ESP32 Physical Climate & Air Quality Station
 * Hardware:
 *   - ESP32 Development Board
 *   - AHT21 (Temperature & Relative Humidity) via I2C (0x38)
 *   - ENS160 (TVOC, eCO2, AQI) via I2C (0x53)
 *   - External LED on GPIO 4
 * Protocol: MQTT over Wi-Fi (Mobile Hotspot)
 * 
 * Mode: 100% REAL PHYSICAL SENSOR DATA (No Simulation)
 * Features built-in native I2C drivers for direct hardware reading.
 * ======================================================================================
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <ArduinoJson.h> // ArduinoJson library (v6 or v7)

// ======================================================================================
// USER CONFIGURATION
// ======================================================================================
const char* WIFI_SSID     = "Galaxy A36 5G";     // Your mobile phone hotspot SSID
const char* WIFI_PASSWORD = "12345678";        // Your hotspot password

// MQTT Broker Settings
const char* MQTT_BROKER   = "broker.emqx.io";
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT_ID= "aerosense_esp32_node_01";
const char* MQTT_USER     = "";
const char* MQTT_PASSWORD = "";

// MQTT Topics (Matches FastAPI backend & React Dashboard)
const char* TOPIC_TELEMETRY    = "aerosense_iot/sensors/data";
const char* TOPIC_LED_SET      = "aerosense_iot/actuators/led/set";
const char* TOPIC_LED_STATUS   = "aerosense_iot/actuators/led/status";
const char* TOPIC_DEVICE_STATUS= "aerosense_iot/device/status";

// Pinout Definitions
#define I2C_SDA_PIN    21
#define I2C_SCL_PIN    22
#define LED_PIN        4    // External LED wired to GPIO 4 (via 220Ω resistor)

// I2C Addresses
#define AHT21_I2C_ADDR  0x38
#define ENS160_I2C_ADDR 0x53 // Default (or 0x52 if ADDR pin pulled LOW)

// Telemetry interval (milliseconds)
const unsigned long TELEMETRY_INTERVAL_MS = 2500;

// ======================================================================================
// GLOBAL OBJECTS & STATE
// ======================================================================================
WiFiClient espClient;
PubSubClient mqttClient(espClient);

bool ahtInitialized = false;
bool ensInitialized = false;
uint8_t ensActiveAddr = ENS160_I2C_ADDR;

bool ledState = false;
unsigned long lastTelemetryTime = 0;
unsigned long bootTime = 0;

// ======================================================================================
// NATIVE DIRECT I2C DRIVER: AHT21 (Temperature & Relative Humidity)
// ======================================================================================
bool initAHT21() {
  Wire.beginTransmission(AHT21_I2C_ADDR);
  Wire.write(0xBA); // Soft reset
  Wire.endTransmission();
  delay(30);

  // Send initialization command
  Wire.beginTransmission(AHT21_I2C_ADDR);
  Wire.write(0xBE);
  Wire.write(0x08);
  Wire.write(0x00);
  byte err = Wire.endTransmission();
  delay(30);
  
  return (err == 0);
}

bool readAHT21(float &temperature, float &humidity) {
  // Trigger measurement
  Wire.beginTransmission(AHT21_I2C_ADDR);
  Wire.write(0xAC);
  Wire.write(0x33);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  delay(80); // Wait for sensor conversion

  // Read 6 bytes
  if (Wire.requestFrom((uint8_t)AHT21_I2C_ADDR, (uint8_t)6) != 6) return false;

  uint8_t buf[6];
  for (int i = 0; i < 6; i++) {
    buf[i] = Wire.read();
  }

  // Check busy status (Bit 7)
  if (buf[0] & 0x80) return false;

  // Convert raw 20-bit humidity and temperature
  uint32_t rawHum = (((uint32_t)buf[1] << 12) | ((uint32_t)buf[2] << 4) | ((uint32_t)buf[3] >> 4));
  uint32_t rawTemp = ((((uint32_t)buf[3] & 0x0F) << 16) | ((uint32_t)buf[4] << 8) | (uint32_t)buf[5]);

  humidity = (float)rawHum * 100.0 / 1048576.0;
  temperature = ((float)rawTemp * 200.0 / 1048576.0) - 50.0;

  // Sanity check
  humidity = constrain(humidity, 0.0, 100.0);
  return true;
}

// ======================================================================================
// NATIVE DIRECT I2C DRIVER: ENS160 (Multi-Gas: TVOC, eCO2, AQI)
// ======================================================================================
bool checkI2CAddress(uint8_t address) {
  Wire.beginTransmission(address);
  return (Wire.endTransmission() == 0);
}

bool initENS160() {
  // Check for 0x53 or 0x52
  if (checkI2CAddress(ENS160_I2C_ADDR)) {
    ensActiveAddr = ENS160_I2C_ADDR;
  } else if (checkI2CAddress(0x52)) {
    ensActiveAddr = 0x52;
  } else {
    return false;
  }

  // Read PART_ID (Reg 0x00) -> expected 0x0160
  Wire.beginTransmission(ensActiveAddr);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;

  Wire.requestFrom(ensActiveAddr, (uint8_t)2);
  if (Wire.available() < 2) return false;
  uint8_t lsb = Wire.read();
  uint8_t msb = Wire.read();
  uint16_t partId = lsb | (msb << 8);
  Serial.printf("[ENS160] Part ID: 0x%04X at 0x%02X\n", partId, ensActiveAddr);

  // Set OPMODE (Reg 0x10) to Standard Operating Mode (0x02)
  Wire.beginTransmission(ensActiveAddr);
  Wire.write(0x10);
  Wire.write(0x02); // 0x02 = Standard Operation
  if (Wire.endTransmission() != 0) return false;

  delay(60);
  return true;
}

void setENS160Compensation(float temp, float hum) {
  // Temp: Kelvin * 64, Hum: % * 512
  uint16_t tempK = (uint16_t)((temp + 273.15) * 64.0);
  uint16_t humVal = (uint16_t)(hum * 512.0);

  Wire.beginTransmission(ensActiveAddr);
  Wire.write(0x13); // TEMP_IN register
  Wire.write(tempK & 0xFF);
  Wire.write((tempK >> 8) & 0xFF);
  Wire.write(humVal & 0xFF);
  Wire.write((humVal >> 8) & 0xFF);
  Wire.endTransmission();
}

bool readENS160(int &tvoc, int &eco2, int &aqi) {
  Wire.beginTransmission(ensActiveAddr);
  Wire.write(0x20); // DATA_STATUS register
  if (Wire.endTransmission() != 0) return false;

  // Request 6 bytes: DATA_STATUS, DATA_AQI, TVOC_LSB, TVOC_MSB, ECO2_LSB, ECO2_MSB
  Wire.requestFrom(ensActiveAddr, (uint8_t)6);
  if (Wire.available() < 6) return false;

  uint8_t status = Wire.read();
  uint8_t aqiRaw = Wire.read();
  uint8_t tvocL  = Wire.read();
  uint8_t tvocH  = Wire.read();
  uint8_t eco2L  = Wire.read();
  uint8_t eco2H  = Wire.read();

  aqi  = aqiRaw & 0x07;
  tvoc = tvocL | (tvocH << 8);
  eco2 = eco2L | (eco2H << 8);

  // Initial warmup validation (first few minutes of sensor boot)
  if (aqi < 1 || aqi > 5) aqi = 1;
  if (eco2 < 400) eco2 = 400;

  return true;
}

// ======================================================================================
// WIFI & MQTT CONNECTION MANAGEMENT
// ======================================================================================
void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("[WiFi] Connecting to: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 25) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Connected successfully!");
    Serial.print("[WiFi] IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("[WiFi] Signal (RSSI): ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("\n[WiFi] Hotspot connection pending. Will retry in loop...");
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.printf("[MQTT RECV] [%s]: %s\n", topic, message.c_str());

  if (String(topic) == TOPIC_LED_SET) {
    bool targetState = false;
    StaticJsonDocument<128> doc;
    DeserializationError error = deserializeJson(doc, message);

    if (!error && doc.containsKey("state")) {
      targetState = doc["state"].as<bool>();
    } else {
      message.trim();
      targetState = (message.equalsIgnoreCase("true") || message == "1" || message.equalsIgnoreCase("on"));
    }

    // Apply to hardware pin (GPIO 4)
    ledState = targetState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    Serial.printf("[ACTUATOR] LED set to: %s (Pin %d)\n", ledState ? "ON (HIGH)" : "OFF (LOW)", LED_PIN);

    // Confirm state back to MQTT
    StaticJsonDocument<128> responseDoc;
    responseDoc["led_state"] = ledState;
    responseDoc["device_id"] = MQTT_CLIENT_ID;
    char buffer[128];
    serializeJson(responseDoc, buffer);
    mqttClient.publish(TOPIC_LED_STATUS, buffer, true);
  }
}

void reconnectMQTT() {
  if (WiFi.status() != WL_CONNECTED) return;

  while (!mqttClient.connected()) {
    Serial.print("[MQTT] Connecting to broker: ");
    Serial.print(MQTT_BROKER);
    Serial.print("...");

    // Last Will and Testament
    StaticJsonDocument<128> lwtDoc;
    lwtDoc["status"] = "offline";
    lwtDoc["device_id"] = MQTT_CLIENT_ID;
    char lwtBuffer[128];
    serializeJson(lwtDoc, lwtBuffer);

    bool connected = false;
    if (strlen(MQTT_USER) > 0) {
      connected = mqttClient.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASSWORD, TOPIC_DEVICE_STATUS, 1, true, lwtBuffer);
    } else {
      connected = mqttClient.connect(MQTT_CLIENT_ID, TOPIC_DEVICE_STATUS, 1, true, lwtBuffer);
    }

    if (connected) {
      Serial.println(" connected!");

      // Publish Online Status
      StaticJsonDocument<128> onlineDoc;
      onlineDoc["status"] = "online";
      onlineDoc["device_id"] = MQTT_CLIENT_ID;
      onlineDoc["ip"] = WiFi.localIP().toString();
      char onlineBuffer[128];
      serializeJson(onlineDoc, onlineBuffer);
      mqttClient.publish(TOPIC_DEVICE_STATUS, onlineBuffer, true);

      // Subscribe to LED control topic
      mqttClient.subscribe(TOPIC_LED_SET);
      Serial.printf("[MQTT] Subscribed to topic: %s\n", TOPIC_LED_SET);

      // Sync LED state
      StaticJsonDocument<128> ledDoc;
      ledDoc["led_state"] = ledState;
      char ledBuf[128];
      serializeJson(ledDoc, ledBuf);
      mqttClient.publish(TOPIC_LED_STATUS, ledBuf, true);
    } else {
      Serial.print(" failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(". Retrying in 4 seconds...");
      delay(4000);
      break;
    }
  }
}

// ======================================================================================
// TELEMETRY PUBLISHER (100% REAL PHYSICAL READINGS)
// ======================================================================================
void publishTelemetry() {
  float temp = 0.0;
  float hum  = 0.0;
  int tvoc   = 0;
  int eco2   = 400;
  int aqi    = 1;
  const char* aqiStatus = "Excellent";

  // 1. Read Physical AHT21
  bool ahtOk = readAHT21(temp, hum);
  if (!ahtOk) {
    Serial.println("[AHT21] Reading failed, retrying init...");
    initAHT21();
  }

  // 2. Feed Compensation into ENS160 & Read
  if (ahtOk) {
    setENS160Compensation(temp, hum);
  }
  
  bool ensOk = readENS160(tvoc, eco2, aqi);
  if (!ensOk) {
    Serial.println("[ENS160] Reading failed, retrying init...");
    initENS160();
  }

  // Determine AQI classification
  if (aqi == 1) aqiStatus = "Excellent";
  else if (aqi == 2) aqiStatus = "Good";
  else if (aqi == 3) aqiStatus = "Moderate";
  else if (aqi == 4) aqiStatus = "Poor";
  else aqiStatus = "Hazardous";

  // Build JSON Payload
  StaticJsonDocument<384> doc;
  doc["device_id"]      = MQTT_CLIENT_ID;
  doc["temperature"]    = serialized(String(temp, 1));
  doc["humidity"]       = serialized(String(hum, 1));
  doc["tvoc"]           = tvoc;
  doc["eco2"]           = eco2;
  doc["aqi"]            = aqi;
  doc["aqi_status"]     = aqiStatus;
  doc["is_simulated"]   = false;
  doc["sensor_mode"]    = "physical_i2c";
  doc["led_state"]      = ledState;
  doc["wifi_rssi"]      = WiFi.RSSI();
  doc["ip"]             = WiFi.localIP().toString();
  doc["uptime_sec"]     = (millis() - bootTime) / 1000;

  char jsonBuffer[384];
  serializeJson(doc, jsonBuffer);

  bool published = mqttClient.publish(TOPIC_TELEMETRY, jsonBuffer);
  if (published) {
    Serial.printf("[PHYSICAL TELEMETRY] Temp=%.1f C | Hum=%.1f %% | TVOC=%d ppb | eCO2=%d ppm | AQI=%d (%s) | LED=%s (Pin %d)\n",
                  temp, hum, tvoc, eco2, aqi, aqiStatus, ledState ? "ON" : "OFF", LED_PIN);
  } else {
    Serial.println("[TELEMETRY] Publish failed, will retry...");
  }
}

// ======================================================================================
// SETUP & LOOP
// ======================================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  bootTime = millis();

  Serial.println("\n=======================================================");
  Serial.println("  AeroSense IoT: Physical Sensor Node (AHT21 + ENS160) ");
  Serial.println("=======================================================");

  // Initialize LED on Pin 4
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.printf("[SETUP] Actuator configured on GPIO %d\n", LED_PIN);

  // Initialize I2C Bus on GPIO 21 (SDA) and GPIO 22 (SCL)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  Wire.setTimeOut(1000);
  delay(200);

  // Initialize Physical Sensors via Native I2C
  Serial.println("[I2C] Initializing AHT21 sensor at 0x38...");
  ahtInitialized = initAHT21();
  Serial.printf("[AHT21] Status: %s\n", ahtInitialized ? "INITIALIZED (OK)" : "FAILED");

  Serial.println("[I2C] Initializing ENS160 sensor at 0x53...");
  ensInitialized = initENS160();
  Serial.printf("[ENS160] Status: %s\n", ensInitialized ? "INITIALIZED (OK)" : "FAILED");

  // Connect to Wi-Fi
  setupWiFi();

  // Configure MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setBufferSize(512);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setupWiFi();
  }

  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = now;
    publishTelemetry();
  }
}
