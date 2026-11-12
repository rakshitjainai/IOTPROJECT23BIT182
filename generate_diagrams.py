"""
Script to generate high-resolution technical diagrams for the AeroSense IoT Project Report.
Produces:
1. diagram1_hardware_wiring.png - Physical wiring schematic between ESP32, AHT21, ENS160, and LED.
2. diagram2_system_architecture.png - End-to-end 4-tier cyber-physical architecture and dataflow.
3. diagram3_sensor_compensation.png - Native I2C sensor fusion and dynamic gas compensation flow.
4. diagram4_firmware_flowchart.png - Firmware state machine and bidirectional communication flowchart.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_diagram1():
    """Generates the Hardware Connection & Wiring Diagram."""
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_facecolor("#0b132b")
    fig.patch.set_facecolor("#0b132b")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title Banner
    ax.text(50, 95, "AeroSense IoT: Hardware Wiring & Pinout Connection Diagram", 
            fontsize=18, fontweight='bold', color="#ffffff", ha="center")
    ax.text(50, 91, "Direct Hardware Interfacing of ESP32 with AHT21 (0x38), ENS160 (0x53), and GPIO 4 Actuator", 
            fontsize=11, color="#64dfdf", ha="center")

    # Draw ESP32 Board (Center-Left)
    esp_box = patches.FancyBboxPatch((8, 20), 28, 62, boxstyle="round,pad=1.5", 
                                    facecolor="#1c2541", edgecolor="#00b4d8", linewidth=2.5)
    ax.add_patch(esp_box)
    ax.text(22, 77, "ESP32 DevKit\n(30-Pin NodeMCU)", fontsize=13, fontweight='bold', color="#ffffff", ha="center")
    ax.text(22, 70, "Xtensa LX6 Dual-Core 240MHz\nWi-Fi 802.11 b/g/n (2.4GHz)", fontsize=8.5, color="#90e0ef", ha="center")

    # ESP32 Pin Labels
    pins = [
        ("3V3 (3.3V Out)", 60, "#ff4d6d"),
        ("GND (Ground)", 50, "#adb5bd"),
        ("GPIO 21 (I2C SDA)", 40, "#06d6a0"),
        ("GPIO 22 (I2C SCL)", 30, "#ffd166"),
        ("GPIO 4 (Actuator Out)", 20, "#9d4edd")
    ]
    for name, y, col in pins:
        # Pin dot
        ax.plot(36, y, marker='o', markersize=9, color=col)
        ax.text(34, y, name, fontsize=9.5, fontweight='bold', color=col, ha="right", va="center")

    # Draw AHT21 Sensor Box (Top-Right)
    aht_box = patches.FancyBboxPatch((65, 62), 26, 22, boxstyle="round,pad=1", 
                                    facecolor="#1e3a5f", edgecolor="#06d6a0", linewidth=2)
    ax.add_patch(aht_box)
    ax.text(78, 80, "AHT21 Sensor Module", fontsize=12, fontweight='bold', color="#ffffff", ha="center")
    ax.text(78, 76, "Temp (-40 to 85°C) & Humidity (0-100%)\nI2C Address: 0x38 | VCC: 3.3V Only", fontsize=8, color="#a7c957", ha="center")
    
    aht_pins = [("VIN", 70, "#ff4d6d"), ("GND", 68, "#adb5bd"), ("SCL", 66, "#ffd166"), ("SDA", 64, "#06d6a0")]
    for p_name, py, col in aht_pins:
        ax.plot(65, py, marker='o', markersize=7, color=col)
        ax.text(67, py, p_name, fontsize=8, fontweight='bold', color=col, va="center")

    # Draw ENS160 Sensor Box (Middle-Right)
    ens_box = patches.FancyBboxPatch((65, 34), 26, 22, boxstyle="round,pad=1", 
                                    facecolor="#2d1b4e", edgecolor="#9d4edd", linewidth=2)
    ax.add_patch(ens_box)
    ax.text(78, 52, "ENS160 Multi-Gas Sensor", fontsize=12, fontweight='bold', color="#ffffff", ha="center")
    ax.text(78, 48, "TVOC (ppb) • eCO2 (ppm) • AQI (1 to 5)\nI2C Address: 0x53 (or 0x52) | VCC: 3.3V", fontsize=8, color="#c77dff", ha="center")

    ens_pins = [("VCC", 42, "#ff4d6d"), ("GND", 40, "#adb5bd"), ("SCL", 38, "#ffd166"), ("SDA", 36, "#06d6a0")]
    for p_name, py, col in ens_pins:
        ax.plot(65, py, marker='o', markersize=7, color=col)
        ax.text(67, py, p_name, fontsize=8, fontweight='bold', color=col, va="center")

    # Draw LED Actuator Circuit (Bottom-Right)
    led_box = patches.FancyBboxPatch((65, 8), 26, 20, boxstyle="round,pad=1", 
                                     facecolor="#3a1c28", edgecolor="#f72585", linewidth=2)
    ax.add_patch(led_box)
    ax.text(78, 24, "External LED Actuator Unit", fontsize=11, fontweight='bold', color="#ffffff", ha="center")
    ax.text(78, 20, "GPIO 4 Control -> 220Ω Resistor -> LED -> GND\nOhm's Law: I = (3.3V - 2.0V) / 220Ω = 5.91mA", fontsize=7.5, color="#ff758f", ha="center")

    ax.plot(65, 15, marker='o', markersize=7, color="#9d4edd")
    ax.text(67, 15, "Anode (+) [via 220Ω]", fontsize=8, fontweight='bold', color="#9d4edd", va="center")
    ax.plot(65, 11, marker='o', markersize=7, color="#adb5bd")
    ax.text(67, 11, "Cathode (-) [to GND]", fontsize=8, fontweight='bold', color="#adb5bd", va="center")

    # WIRING CONNECTIONS (Lines with distinct styling and colors)
    # 1. 3V3 Power Rail (Red)
    ax.plot([36, 45, 45, 65], [60, 60, 70, 70], color="#ff4d6d", linewidth=2.2, label="3V3 Power (3.3V DC)")
    ax.plot([45, 45, 65], [70, 42, 42], color="#ff4d6d", linewidth=2.2)

    # 2. GND Common Ground Rail (Black / Light Grey)
    ax.plot([36, 48, 48, 65], [50, 50, 68, 68], color="#adb5bd", linewidth=2.2, linestyle='--', label="Common Ground (GND)")
    ax.plot([48, 48, 65], [68, 40, 40], color="#adb5bd", linewidth=2.2, linestyle='--')
    ax.plot([48, 48, 65], [40, 11, 11], color="#adb5bd", linewidth=2.2, linestyle='--')

    # 3. SDA Shared I2C Data Line (Green)
    ax.plot([36, 52, 52, 65], [40, 40, 64, 64], color="#06d6a0", linewidth=2.5, label="I2C SDA (GPIO 21 - Shared)")
    ax.plot([52, 52, 65], [64, 36, 36], color="#06d6a0", linewidth=2.5)

    # 4. SCL Shared I2C Clock Line (Yellow)
    ax.plot([36, 56, 56, 65], [30, 30, 66, 66], color="#ffd166", linewidth=2.5, label="I2C SCL (GPIO 22 - Shared)")
    ax.plot([56, 56, 65], [66, 38, 38], color="#ffd166", linewidth=2.5)

    # 5. GPIO 4 Actuator Link (Purple)
    ax.plot([36, 65], [20, 15], color="#9d4edd", linewidth=2.5, label="Actuator Control (GPIO 4)")

    # Legend at bottom
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 0.01), ncol=5, fontsize=8.5, 
              facecolor="#1c2541", edgecolor="#00b4d8", labelcolor="#ffffff")

    plt.tight_layout()
    output_path = os.path.join(os.getcwd(), "diagram1_hardware_wiring.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {output_path}")

def generate_diagram2():
    """Generates the End-to-End System Architecture & Dataflow Diagram."""
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_facecolor("#0a0f1d")
    fig.patch.set_facecolor("#0a0f1d")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title Banner
    ax.text(50, 95, "AeroSense IoT: End-to-End System Architecture & Dataflow", 
            fontsize=18, fontweight='bold', color="#ffffff", ha="center")
    ax.text(50, 91, "Cyber-Physical Multi-Tier Architecture: Edge Node ➔ MQTT Broker ➔ FastAPI ➔ React HD Dashboard", 
            fontsize=10.5, color="#38bdf8", ha="center")

    # 4 Architectural Columns / Layers
    layers = [
        ("LAYER 1: PHYSICAL EDGE", 4, 20, "#1e293b", "#0284c7"),
        ("LAYER 2: NETWORK & BROKER", 28, 20, "#0f172a", "#6366f1"),
        ("LAYER 3: FASTAPI BACKEND", 52, 20, "#111827", "#10b981"),
        ("LAYER 4: REACT DASHBOARD", 76, 20, "#1e1b4b", "#ec4899")
    ]
    for title, x, w, bg, border in layers:
        layer_box = patches.FancyBboxPatch((x, 10), w, 76, boxstyle="round,pad=1", 
                                           facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(layer_box)
        ax.text(x + w/2, 83, title, fontsize=10.5, fontweight='bold', color="#ffffff", ha="center")

    # Layer 1 Components (Edge Node)
    ax.text(14, 75, "ESP32 SoC", fontsize=12, fontweight='bold', color="#38bdf8", ha="center")
    ax.text(14, 69, "• FreeRTOS Task Loop\n• PubSubClient MQTT\n• Direct Native I2C\n• Wi-Fi STA Mode", 
            fontsize=8.5, color="#94a3b8", ha="center")

    ax.plot([14, 14], [62, 58], color="#0284c7", linewidth=2)
    
    sens_box = patches.FancyBboxPatch((6, 38), 16, 18, boxstyle="round,pad=0.5", 
                                      facecolor="#0f172a", edgecolor="#38bdf8", linewidth=1.5)
    ax.add_patch(sens_box)
    ax.text(14, 52, "Sensors & Actuator", fontsize=10, fontweight='bold', color="#38bdf8", ha="center")
    ax.text(14, 44, "• AHT21 (T & H)\n• ENS160 (Gas/AQI)\n• Dynamic Calib.\n• LED (GPIO 4)", 
            fontsize=8, color="#cbd5e1", ha="center")

    ax.text(14, 26, "Telemetry Packet:\nJSON over 2.4GHz Wi-Fi\n(Every 2.5 seconds)", 
            fontsize=8, color="#f59e0b", ha="center")

    # Layer 2 Components (MQTT Broker)
    ax.text(38, 75, "MQTT Broker\n(broker.emqx.io)", fontsize=11.5, fontweight='bold', color="#a5b4fc", ha="center")
    ax.text(38, 67, "Port 1883 • QoS 0/1\nPub/Sub Decoupled Hub", fontsize=8.5, color="#cbd5e1", ha="center")

    topic_box = patches.FancyBboxPatch((30, 22), 16, 40, boxstyle="round,pad=0.5", 
                                       facecolor="#1e1b4b", edgecolor="#818cf8", linewidth=1.5)
    ax.add_patch(topic_box)
    ax.text(38, 58, "Active Topics:", fontsize=9.5, fontweight='bold', color="#c7d2fe", ha="center")
    ax.text(38, 42, "1. Telemetry:\n   aerosense_iot/\n   sensors/data\n2. LED Set:\n   aerosense_iot/\n   actuators/led/set\n3. LED Status:\n   aerosense_iot/\n   actuators/led/status\n4. LWT Heartbeat:\n   aerosense_iot/\n   device/status", 
            fontsize=7.2, color="#e0e7ff", ha="center")

    # Layer 3 Components (FastAPI Backend)
    ax.text(62, 75, "FastAPI Service\n(Python 3.13 / Asyncio)", fontsize=11.5, fontweight='bold', color="#34d399", ha="center")
    ax.text(62, 67, "Uvicorn Server :8000\nCORS Middleware Enabled", fontsize=8.5, color="#a7f3d0", ha="center")

    be_box = patches.FancyBboxPatch((54, 22), 16, 40, boxstyle="round,pad=0.5", 
                                    facecolor="#064e3b", edgecolor="#10b981", linewidth=1.5)
    ax.add_patch(be_box)
    ax.text(62, 58, "Core Modules:", fontsize=9.5, fontweight='bold', color="#6ee7b7", ha="center")
    ax.text(62, 42, "• Paho-MQTT Thread\n• In-Memory Buffer\n  (50 Historical Pkts)\n• ConnectionManager\n  WebSocket Broadcaster\n• REST Endpoints:\n  /api/status\n  /api/led\n  /api/telemetry/history\n• Fallback Simulator", 
            fontsize=7.5, color="#ecfdf5", ha="center")

    # Layer 4 Components (React Dashboard)
    ax.text(86, 75, "React HD Dashboard\n(Vite Dev Server :5173)", fontsize=11.5, fontweight='bold', color="#f472b6", ha="center")
    ax.text(86, 67, "Modern Glassmorphism\nLucide React Icons", fontsize=8.5, color="#fbcfe8", ha="center")

    fe_box = patches.FancyBboxPatch((78, 22), 16, 40, boxstyle="round,pad=0.5", 
                                    facecolor="#500724", edgecolor="#f43f5e", linewidth=1.5)
    ax.add_patch(fe_box)
    ax.text(86, 58, "Visual Widgets:", fontsize=9.5, fontweight='bold', color="#fda4af", ha="center")
    ax.text(86, 42, "• Radial SVG AQI Gauge\n  (Color Coded 1-5)\n• 3D Illuminated LED Bulb\n  Tactile Remote Switch\n• Live SVG Chart\n  (Multi-Channel Trends)\n• Sensor Metric Cards\n  (°C, %RH, TVOC, eCO2)\n• Diagnostics Drawer", 
            fontsize=7.5, color="#fff1f2", ha="center")

    # FLOW ARROWS
    # Telemetry flow (Left to Right - Cyan Arrow)
    ax.annotate("", xy=(28, 55), xytext=(24, 55),
                arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2.5, headwidth=8))
    ax.text(26, 57.5, "PUBLISH", fontsize=7.5, fontweight='bold', color='#38bdf8', ha='center')

    ax.annotate("", xy=(52, 55), xytext=(48, 55),
                arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2.5, headwidth=8))
    ax.text(50, 57.5, "SUBSCRIBE", fontsize=7.5, fontweight='bold', color='#38bdf8', ha='center')

    ax.annotate("", xy=(76, 55), xytext=(72, 55),
                arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=2.5, headwidth=8))
    ax.text(74, 57.5, "WEBSOCKET", fontsize=7, fontweight='bold', color='#10b981', ha='center')

    # Actuator Control flow (Right to Left - Magenta/Orange Arrow)
    ax.annotate("", xy=(72, 30), xytext=(76, 30),
                arrowprops=dict(facecolor='#f43f5e', edgecolor='#f43f5e', width=2.5, headwidth=8))
    ax.text(74, 32.5, "LED TOGGLE", fontsize=7, fontweight='bold', color='#f43f5e', ha='center')

    ax.annotate("", xy=(48, 30), xytext=(52, 30),
                arrowprops=dict(facecolor='#f43f5e', edgecolor='#f43f5e', width=2.5, headwidth=8))
    ax.text(50, 32.5, "MQTT PUB", fontsize=7.5, fontweight='bold', color='#f43f5e', ha='center')

    ax.annotate("", xy=(24, 30), xytext=(28, 30),
                arrowprops=dict(facecolor='#f43f5e', edgecolor='#f43f5e', width=2.5, headwidth=8))
    ax.text(26, 32.5, "SUB COMMAND", fontsize=7, fontweight='bold', color='#f43f5e', ha='center')

    plt.tight_layout()
    output_path = os.path.join(os.getcwd(), "diagram2_system_architecture.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {output_path}")

def generate_diagram3():
    """Generates the Native I2C Sensor Fusion & Dynamic Environmental Compensation Architecture."""
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_facecolor("#0b132b")
    fig.patch.set_facecolor("#0b132b")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title Banner
    ax.text(50, 95, "AeroSense IoT: Sensor Fusion & Dynamic Environmental Compensation", 
            fontsize=17, fontweight='bold', color="#ffffff", ha="center")
    ax.text(50, 91, "Mathematical Closed-Loop Coupling between AHT21 and ENS160 MOX Gas Sensing Matrix", 
            fontsize=10.5, color="#64dfdf", ha="center")

    # Step 1: AHT21 Measurement
    b1 = patches.FancyBboxPatch((5, 48), 24, 36, boxstyle="round,pad=1", facecolor="#1e3a5f", edgecolor="#06d6a0", linewidth=2)
    ax.add_patch(b1)
    ax.text(17, 80, "Step 1: Physical Climate\nMeasurement (AHT21)", fontsize=11, fontweight='bold', color="#ffffff", ha="center")
    ax.text(17, 65, "• Sends trigger: 0xAC 0x33 0x00\n• Awaits 80ms conversion\n• Reads 6-byte raw buffer\n• Decodes 20-bit formulas:\n  Hum = (rawHum * 100) / 2^20\n  Temp = (rawTemp * 200)/2^20 - 50", 
            fontsize=8, color="#a7c957", ha="center")

    # Step 2: ESP32 Math Engine
    b2 = patches.FancyBboxPatch((38, 48), 24, 36, boxstyle="round,pad=1", facecolor="#1c2541", edgecolor="#00b4d8", linewidth=2)
    ax.add_patch(b2)
    ax.text(50, 80, "Step 2: ESP32 Compensation\nRegister Synthesis", fontsize=11, fontweight='bold', color="#ffffff", ha="center")
    ax.text(50, 65, "• Converts Ambient Temperature:\n  T_Kelvin = Temp_C + 273.15\n  RegVal_T = uint16(T_Kelvin * 64)\n• Converts Relative Humidity:\n  RegVal_H = uint16(Hum_% * 512)\n• Formats 4 bytes for I2C write\n• Direct inject into Reg 0x13", 
            fontsize=8, color="#90e0ef", ha="center")

    # Step 3: ENS160 Gas Engine
    b3 = patches.FancyBboxPatch((71, 48), 24, 36, boxstyle="round,pad=1", facecolor="#2d1b4e", edgecolor="#9d4edd", linewidth=2)
    ax.add_patch(b3)
    ax.text(83, 80, "Step 3: ENS160 Multi-Gas\nBaseline Tuning", fontsize=11, fontweight='bold', color="#ffffff", ha="center")
    ax.text(83, 65, "• 4 Independent MOX Hotplates\n• Real-time temperature & moisture\n  cross-sensitivity canceled\n• Computes true resistance shifts:\n  TVOC: 0 to 65,000 ppb\n  eCO2: 400 to 65,000 ppm\n  AQI Index: 1 to 5 (UBA Rating)", 
            fontsize=8, color="#c77dff", ha="center")

    # Arrows between steps
    ax.annotate("", xy=(38, 66), xytext=(29, 66),
                arrowprops=dict(facecolor='#06d6a0', edgecolor='#06d6a0', width=3, headwidth=9))
    ax.text(33.5, 69, "Temp & Hum\nFloat Data", fontsize=7.5, fontweight='bold', color='#06d6a0', ha='center')

    ax.annotate("", xy=(71, 66), xytext=(62, 66),
                arrowprops=dict(facecolor='#00b4d8', edgecolor='#00b4d8', width=3, headwidth=9))
    ax.text(66.5, 69, "I2C Write\nReg 0x13-0x16", fontsize=7.5, fontweight='bold', color='#00b4d8', ha='center')

    # Bottom Section: Why Compensation is Essential
    b_bot = patches.FancyBboxPatch((5, 10), 90, 30, boxstyle="round,pad=1", facecolor="#111827", edgecolor="#f59e0b", linewidth=2)
    ax.add_patch(b_bot)
    ax.text(50, 36, "Why Dynamic Environmental Compensation is Essential in MOX Sensing", 
            fontsize=12, fontweight='bold', color="#fbbf24", ha="center")
    ax.text(50, 23, 
            "1. Physics of MOX Sensors: Metal Oxide Semiconductor sensors detect volatile gases through catalytic oxidation on heated tin dioxide (SnO2) surfaces.\n"
            "2. Environmental Cross-Sensitivity: Ambient humidity introduces water molecules (H2O) that compete with gas molecules for adsorption sites,\n"
            "    falsely elevating VOC readings. Temperature variations similarly alter semiconductor carrier concentration and surface resistance.\n"
            "3. Closed-Loop Solution: By reading the AHT21 (±0.3°C / ±2% RH) every cycle and writing the values into ENS160 registers before every gas poll,\n"
            "    the embedded ScioSense gas algorithm dynamically shifts its baseline, ensuring laboratory-grade, drift-free air quality assessment.",
            fontsize=8.5, color="#e5e7eb", ha="center")

    plt.tight_layout()
    output_path = os.path.join(os.getcwd(), "diagram3_sensor_compensation.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {output_path}")

def generate_diagram4():
    """Generates the Network & Firmware State Machine Execution Flowchart."""
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Title Banner
    ax.text(50, 95, "AeroSense IoT: Firmware & Communication State Machine", 
            fontsize=17, fontweight='bold', color="#ffffff", ha="center")
    ax.text(50, 91, "Deterministic Non-Blocking Loop: I2C Sampling, MQTT Synchronization & Bidirectional Actuation", 
            fontsize=10.5, color="#38bdf8", ha="center")

    # Flowchart Blocks
    blocks = [
        ("Power On / Reset\nESP32 Cold Boot", 15, 76, 22, 10, "#1e293b", "#38bdf8"),
        ("Native I2C Bus Init\n(SDA=21, SCL=22)", 40, 76, 22, 10, "#1e293b", "#38bdf8"),
        ("Wi-Fi Hotspot Connect\n(Galaxy A36 5G - STA Mode)", 65, 76, 24, 10, "#1e293b", "#38bdf8"),
        
        ("MQTT Connect + LWT\nSub: /actuators/led/set", 65, 52, 24, 12, "#312e81", "#818cf8"),
        ("Read AHT21 Sensor\n(Temp & Rel Humidity)", 40, 52, 22, 12, "#064e3b", "#10b981"),
        ("Compensate & Read ENS160\n(TVOC, eCO2, AQI 1-5)", 15, 52, 22, 12, "#064e3b", "#10b981"),

        ("Build JSON Telemetry\nPublish: /sensors/data", 15, 24, 22, 12, "#701a75", "#f43f5e"),
        ("Poll MQTT Network Loop\n(mqttClient.loop())", 40, 24, 22, 12, "#854d0e", "#eab308"),
        ("Incoming Actuator Command?\nSet GPIO 4 & Publish Status", 65, 24, 24, 12, "#831843", "#ec4899"),
    ]

    for title, x, y, w, h, bg, border in blocks:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8", 
                                     facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, title, fontsize=9, fontweight='bold', color="#ffffff", 
                ha="center", va="center")

    # Connect arrows
    # Row 1 Left to Right
    ax.annotate("", xy=(40, 81), xytext=(37, 81), arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2, headwidth=6))
    ax.annotate("", xy=(65, 81), xytext=(62, 81), arrowprops=dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2, headwidth=6))
    
    # Down to Row 2
    ax.annotate("", xy=(77, 64), xytext=(77, 76), arrowprops=dict(facecolor='#818cf8', edgecolor='#818cf8', width=2, headwidth=6))

    # Row 2 Right to Left
    ax.annotate("", xy=(62, 58), xytext=(65, 58), arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=2, headwidth=6))
    ax.annotate("", xy=(37, 58), xytext=(40, 58), arrowprops=dict(facecolor='#10b981', edgecolor='#10b981', width=2, headwidth=6))

    # Down to Row 3
    ax.annotate("", xy=(26, 36), xytext=(26, 52), arrowprops=dict(facecolor='#f43f5e', edgecolor='#f43f5e', width=2, headwidth=6))

    # Row 3 Left to Right
    ax.annotate("", xy=(40, 30), xytext=(37, 30), arrowprops=dict(facecolor='#eab308', edgecolor='#eab308', width=2, headwidth=6))
    ax.annotate("", xy=(65, 30), xytext=(62, 30), arrowprops=dict(facecolor='#ec4899', edgecolor='#ec4899', width=2, headwidth=6))

    # Loop back from bottom right to telemetry timer
    ax.annotate("", xy=(26, 24), xytext=(77, 24), 
                arrowprops=dict(facecolor='#94a3b8', edgecolor='#94a3b8', width=1.5, headwidth=6, connectionstyle="arc3,rad=-0.3"))
    ax.text(50, 11, "Repeat Every 2500ms (Non-Blocking millis() Tick)", fontsize=9, fontweight='bold', color="#94a3b8", ha="center")

    plt.tight_layout()
    output_path = os.path.join(os.getcwd(), "diagram4_firmware_flowchart.png")
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    generate_diagram1()
    generate_diagram2()
    generate_diagram3()
    generate_diagram4()
    print("All 4 diagrams generated successfully!")
