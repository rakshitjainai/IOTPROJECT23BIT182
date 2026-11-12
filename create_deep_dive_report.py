"""
Generates the comprehensive in-depth Word Document (.docx) for AeroSense IoT,
embedding all 4 high-resolution connection and architecture diagrams.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text_content, title="TECHNICAL SPECIFICATION"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_background(c, "f0f9ff")
    set_cell_margins(c, top=120, bottom=120, left=180, right=180)
    p = c.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(0)
    r_title = p.add_run(f"[{title}]\n")
    r_title.bold = True
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)
    r_body = p.add_run(text_content)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_with_caption(doc, image_path, caption_title, caption_desc):
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        r_cap_title = p_cap.add_run(caption_title + ": ")
        r_cap_title.bold = True
        r_cap_title.font.size = Pt(9.5)
        r_cap_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        r_cap_desc = p_cap.add_run(caption_desc)
        r_cap_desc.font.size = Pt(9.5)
        r_cap_desc.font.italic = True
        r_cap_desc.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)

def build_comprehensive_report():
    doc = Document()

    # Standard Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)

    # =========================================================================
    # DOCUMENT COVER / TITLE
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(24)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AeroSense IoT")
    r_title.font.size = Pt(30)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Comprehensive Technical Architectural Report & Wiring Guide\nReal-Time Environmental Climate Monitoring & Remote Actuator Control System")
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)

    # Accent divider
    div_table = doc.add_table(rows=1, cols=1)
    div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = div_table.cell(0, 0)
    set_cell_background(cell, "0284c7")
    cell.paragraphs[0].paragraph_format.space_before = Pt(2)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    r_div = cell.paragraphs[0].add_run("")
    r_div.font.size = Pt(2)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Meta banner
    add_callout(
        doc,
        "Platform Architecture: ESP32 SoC (30-Pin NodeMCU) • AHT21 (Temp & Humidity) • ENS160 (TVOC, eCO2, AQI)\n"
        "Protocols & Transports: MQTT over 2.4GHz Wi-Fi (EMQX Broker) • Full-Duplex WebSockets • REST API\n"
        "Software Stack: Arduino C++ (Native I2C Drivers) • Python 3.13 FastAPI • React 18 + Vite (Cyber-Glassmorphism UI)\n"
        "GitHub Repository: https://github.com/rakshitjainai/IOTPROJECT23BIT182.git",
        title="SYSTEM OVERVIEW & REPOSITORY METADATA"
    )

    # =========================================================================
    # 1. EXECUTIVE SUMMARY & SYSTEM CAPABILITIES
    # =========================================================================
    h1 = doc.add_heading("1. Executive Summary & Problem Formulation", level=1)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "AeroSense IoT is an enterprise-grade, cyber-physical Internet of Things (IoT) system engineered for high-precision "
        "environmental telemetry collection, real-time chemical air quality analysis, and bidirectional edge actuator control. "
        "Indoor air quality (IAQ) and ambient microclimates significantly govern human cognitive performance, occupational health, "
        "and building safety. Elevated concentrations of Volatile Organic Compounds (VOCs) and accumulated equivalent Carbon Dioxide (eCO2) "
        "induce lethargy, headaches ('Sick Building Syndrome'), and respiratory distress. Simultaneously, fluctuations in ambient "
        "temperature and relative humidity distort environmental comfort and cause measurement drift in metal-oxide chemical gas sensors."
    )
    doc.add_paragraph(
        "To address these critical engineering challenges, AeroSense IoT integrates a dedicated physical edge sensing node (ESP32), "
        "scientific-grade digital transducers (AHT21 and ENS160), a decoupled MQTT publish-subscribe messaging backbone, an asynchronous "
        "FastAPI Python backend service, and a high-definition (HD) React web dashboard. The system features dynamic closed-loop "
        "environmental compensation directly at the hardware layer, sub-200ms end-to-end data delivery, and bidirectional remote control "
        "of a physical LED actuator with real-time state confirmation."
    )

    # =========================================================================
    # 2. HARDWARE ARCHITECTURE & CONNECTION DIAGRAMS
    # =========================================================================
    h2 = doc.add_heading("2. Hardware Architecture, Electrical Pinout & Wiring", level=1)
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The physical edge node is built around the Espressif ESP32-WROOM-32 microcontroller. The sensors interface with the ESP32 "
        "via a shared two-wire Inter-Integrated Circuit (I2C) bus operating at 3.3V logic. An external indicator LED is wired to GPIO 4 "
        "through an analytically calculated current-limiting resistor."
    )

    # Insert Diagram 1 (Hardware Connection Diagram)
    add_image_with_caption(
        doc,
        os.path.join(os.getcwd(), "diagram1_hardware_wiring.png"),
        "FIGURE 2.1",
        "AeroSense IoT Hardware Wiring & Pinout Connection Diagram showing ESP32, AHT21, ENS160, and GPIO 4 Actuator."
    )

    # Hardware Components Table
    t_hw = doc.add_table(rows=5, cols=4)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers_hw = ["Component / Module", "Electrical Interface", "Operating Voltage", "Functional Description"]
    for i, h in enumerate(headers_hw):
        c = t_hw.cell(0, i)
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    hw_specs = [
        ("ESP32 DevKit (30-Pin)", "2.4 GHz 802.11 b/g/n Wi-Fi, Xtensa Dual-Core 240MHz", "3.3V Logic / 5V USB", "Central computing engine, I2C bus master, FreeRTOS task loop, and MQTT client node."),
        ("AHT21 Sensor Module", "I2C (7-bit address 0x38)", "3.3V DC (Regulated)", "Precision ambient temperature (-40°C to +85°C, ±0.3°C) and relative humidity (0% to 100% RH, ±2%)."),
        ("ENS160 Multi-Gas Sensor", "I2C (7-bit address 0x53 / 0x52)", "3.3V DC (Regulated)", "4 independent MOX hotplates calculating TVOC (0-65,000 ppb), eCO2 (400-65,000 ppm), and AQI (1-5)."),
        ("LED Actuator Unit", "GPIO 4 (via 220Ω series resistor)", "3.3V Digital Output", "Physical actuator with remote state synchronization, visual verification, and status feedback.")
    ]
    for row_idx, row in enumerate(hw_specs, start=1):
        for col_idx, val in enumerate(row):
            c = t_hw.cell(row_idx, col_idx)
            bg = "f8fafc" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            c.paragraphs[0].add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Detailed Wiring Pinout Table
    doc.add_heading("2.1 Complete Pin-to-Pin Wiring Specification", level=2)
    doc.add_paragraph(
        "Both the AHT21 and ENS160 share the same physical I2C bus lines on the ESP32 (GPIO 21 for SDA and GPIO 22 for SCL). "
        "Because each sensor has a unique 7-bit hardware address (0x38 for AHT21 and 0x53 for ENS160), there are no address collisions."
    )

    t_pin = doc.add_table(rows=7, cols=5)
    t_pin.alignment = WD_TABLE_ALIGNMENT.CENTER
    pin_headers = ["Sensor / Component Pin", "ESP32 Target Pin", "Standard Wire Color", "Signal Nature", "Engineering Guidelines"]
    for i, h in enumerate(pin_headers):
        c = t_pin.cell(0, i)
        set_cell_background(c, "0f766e")
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    pin_details = [
        ("VCC (AHT21 & ENS160)", "3V3 Pin", "Red", "3.3V DC Regulated Power", "CRITICAL: Connect strictly to 3V3 rail. 5V will permanently destroy the ENS160/AHT21 silicon!"),
        ("GND (AHT21 & ENS160)", "GND Pin", "Black", "0V Common Ground", "Common reference ground plane across all microcontrollers, sensors, and actuators."),
        ("SDA (AHT21 & ENS160)", "GPIO 21 (D21)", "Green / Blue", "Shared I2C Serial Data", "Open-drain bidirectional data line pulled up to 3.3V logic."),
        ("SCL (AHT21 & ENS160)", "GPIO 22 (D22)", "Yellow", "Shared I2C Serial Clock", "Synchronous clock line generated by ESP32 I2C hardware master controller."),
        ("LED Anode (+ Long Leg)", "GPIO 4 (D4)", "Purple / Orange", "Digital Output (3.3V)", "Wired through in-series 220Ω current limiting resistor to prevent GPIO overcurrent."),
        ("LED Cathode (- Short Leg)", "GND Pin", "Black", "Ground Return", "Tied directly to the ESP32 common ground bus.")
    ]
    for row_idx, row in enumerate(pin_details, start=1):
        for col_idx, val in enumerate(row):
            c = t_pin.cell(row_idx, col_idx)
            bg = "f0fdfa" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            c.paragraphs[0].add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Actuator Ohm's Law Calculation
    doc.add_heading("2.2 Actuator Circuit Analysis: Ohm's Law Calculation", level=2)
    doc.add_paragraph(
        "To ensure long-term stability and prevent electrical damage to the ESP32's internal GPIO driver transistors, "
        "the current flowing through the LED diode must be precisely throttled. The series resistance R is governed by Ohm's Law:\n\n"
        "    R = (V_GPIO - V_F) / I_F\n\n"
        "Where:\n"
        "• V_GPIO = 3.3V (Logic high output voltage supplied by ESP32 GPIO 4)\n"
        "• V_F = 2.0V (Standard forward voltage drop across an indicator LED)\n"
        "• I_F = 6.0 mA = 0.006 A (Target continuous forward current for crisp visual illumination)\n\n"
        "Calculation:\n"
        "    R = (3.3V - 2.0V) / 0.006 A = 1.3V / 0.006 A = 216.67 Ω\n\n"
        "A standard commercial E24 series resistor of 220 Ω (5% tolerance) is utilized. The operational current is therefore "
        "I = 1.3V / 220 Ω = 5.91 mA. This value comfortably respects the ESP32 pin maximum continuous rating of 12 mA (absolute limit 40 mA)."
    )

    # =========================================================================
    # 3. END-TO-END SYSTEM ARCHITECTURE & DATAFLOW
    # =========================================================================
    h3 = doc.add_heading("3. End-to-End System Architecture & Dataflow", level=1)
    h3.paragraph_format.space_before = Pt(18)
    h3.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The AeroSense IoT system adopts a modern 4-tier decoupled architecture designed for high throughput, minimal transmission latency, "
        "and clean separation of concerns: Physical Edge Layer, Network & Broker Layer, Application Server Layer, and Presentation Layer."
    )

    # Insert Diagram 2 (System Architecture)
    add_image_with_caption(
        doc,
        os.path.join(os.getcwd(), "diagram2_system_architecture.png"),
        "FIGURE 3.1",
        "AeroSense IoT 4-Tier End-to-End System Architecture and Bidirectional Communication Dataflow."
    )

    doc.add_paragraph(
        "1. Layer 1 (Physical Edge Layer): The ESP32 SoC executes non-blocking polling loops, communicates natively with AHT21 and ENS160, "
        "packages measurements into a serialized JSON payload, and toggles the GPIO 4 actuator pin.\n"
        "2. Layer 2 (Network & MQTT Broker Layer): Provides decoupled, publish-subscribe message routing using MQTT broker broker.emqx.io (port 1883). "
        "Ensures low packet overhead and handles device availability via Last Will and Testament (LWT).\n"
        "3. Layer 3 (FastAPI Application Server): Python 3.13 service running Uvicorn. Integrates a background Paho-MQTT client thread, "
        "maintains an in-memory 50-item circular history buffer for zero-delay chart hydration, and bridges packets into full-duplex WebSockets (/ws/telemetry).\n"
        "4. Layer 4 (React HD Dashboard): React 18 single-page application built on Vite. Connects to the WebSocket bridge, updates radial SVG gauges, "
        "renders dynamic time-series charts, and allows one-click bidirectional control of the remote physical LED."
    )

    # =========================================================================
    # 4. SENSOR FUSION & DYNAMIC ENVIRONMENTAL COMPENSATION
    # =========================================================================
    h4 = doc.add_heading("4. Native I2C Drivers & Dynamic Environmental Compensation", level=1)
    h4.paragraph_format.space_before = Pt(18)
    h4.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "One of the standout technical innovations of AeroSense IoT is the implementation of native direct I2C drivers coupled with "
        "real-time dynamic environmental compensation for chemical gas sensing."
    )

    # Insert Diagram 3 (Sensor Compensation)
    add_image_with_caption(
        doc,
        os.path.join(os.getcwd(), "diagram3_sensor_compensation.png"),
        "FIGURE 4.1",
        "Closed-Loop Sensor Fusion: Dynamic Injection of AHT21 Temperature & Humidity into ENS160 MOX Gas Algorithm Engine."
    )

    doc.add_heading("4.1 The Physics of MOX Gas Cross-Sensitivity", level=2)
    doc.add_paragraph(
        "The ENS160 multi-gas sensor utilizes four independent micro-hotplate Metal-Oxide Semiconductor (MOX) sensing elements. "
        "Gas detection occurs via catalytic oxidation-reduction reactions on heated tin-dioxide (SnO2) thin-film layers. However, ambient "
        "relative humidity introduces water vapor (H2O), whose hydroxyl (-OH) groups compete directly with target volatile compounds for surface "
        "chemisorption sites. Furthermore, temperature variations modulate the electron carrier density of the semiconductor film. Uncompensated "
        "MOX sensors suffer from severe baseline drift—yielding false spikes in TVOC and eCO2 during atmospheric shifts."
    )

    doc.add_heading("4.2 Closed-Loop Mathematical Compensation Formula", level=2)
    doc.add_paragraph(
        "AeroSense IoT overcomes this fundamental limitation by executing an automated compensation routine before every gas read cycle:\n"
        "1. The ESP32 queries the AHT21 sensor over I2C, acquiring calibrated temperature (T in °C) and relative humidity (H in % RH).\n"
        "2. The firmware converts temperature into Absolute Kelvin and scales it by 64:\n"
        "       T_Kelvin = (T_Celsius + 273.15)\n"
        "       TEMP_IN_REG = (uint16_t)(T_Kelvin * 64.0)\n"
        "3. The firmware scales relative humidity by 512:\n"
        "       HUM_IN_REG = (uint16_t)(Humidity_% * 512.0)\n"
        "4. These 4 bytes are written directly via I2C into ENS160 register 0x13 (TEMP_IN). The ENS160 on-chip microprocessor dynamically "
        "adapts its baseline algorithms, delivering laboratory-grade TVOC (ppb), eCO2 (ppm), and AQI (1-5) ratings."
    )

    # =========================================================================
    # 5. FIRMWARE IMPLEMENTATION & STATE MACHINE FLOWCHART
    # =========================================================================
    h5 = doc.add_heading("5. Firmware Implementation & Execution Flowchart", level=1)
    h5.paragraph_format.space_before = Pt(18)
    h5.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The firmware is authored in Arduino C++ (firmware/esp32_iot_node/esp32_iot_node.ino) and is structured around a non-blocking, "
        "deterministic state machine. It avoids software delays in the main loop, ensuring immediate reaction to incoming MQTT actuator commands."
    )

    # Insert Diagram 4 (Firmware Flowchart)
    add_image_with_caption(
        doc,
        os.path.join(os.getcwd(), "diagram4_firmware_flowchart.png"),
        "FIGURE 5.1",
        "Firmware State Machine Flowchart: Cold Boot, Native I2C Polling, MQTT Loop, and Bidirectional Actuation."
    )

    # =========================================================================
    # 6. MQTT PROTOCOL SPECIFICATION & DATA CONTRACTS
    # =========================================================================
    h6 = doc.add_heading("6. MQTT Protocol Specification & Data Contracts", level=1)
    h6.paragraph_format.space_before = Pt(18)
    h6.paragraph_format.space_after = Pt(8)

    t_mqtt = doc.add_table(rows=5, cols=4)
    t_mqtt.alignment = WD_TABLE_ALIGNMENT.CENTER
    mqtt_headers = ["MQTT Topic", "Direction", "Payload Format", "Operational Role"]
    for i, h in enumerate(mqtt_headers):
        c = t_mqtt.cell(0, i)
        set_cell_background(c, "4338ca")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    mqtt_data = [
        ("aerosense_iot/sensors/data", "ESP32 ➔ Backend", "JSON Object", "Transmits live sensor readings every 2500ms (Temperature, Humidity, TVOC, eCO2, AQI, RSSI, Uptime)."),
        ("aerosense_iot/actuators/led/set", "Backend ➔ ESP32", '{"state": true/false}', "Command topic used by dashboard to turn the GPIO 4 physical LED on or off."),
        ("aerosense_iot/actuators/led/status", "ESP32 ➔ Backend", '{"led_state": true/false}', "Published by ESP32 immediately after changing pin state to confirm hardware actuation."),
        ("aerosense_iot/device/status", "ESP32 ➔ Backend", '{"status": "online/offline"}', "Device heartbeat and MQTT Last Will and Testament (LWT) for automatic offline detection.")
    ]
    for row_idx, row in enumerate(mqtt_data, start=1):
        for col_idx, val in enumerate(row):
            c = t_mqtt.cell(row_idx, col_idx)
            bg = "eef2ff" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            c.paragraphs[0].add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # JSON Telemetry Contract Callout
    add_callout(
        doc,
        '{\n'
        '  "device_id": "aerosense_esp32_node_01",\n'
        '  "temperature": 26.4,\n'
        '  "humidity": 51.8,\n'
        '  "tvoc": 85,\n'
        '  "eco2": 462,\n'
        '  "aqi": 1,\n'
        '  "aqi_status": "Excellent",\n'
        '  "is_simulated": false,\n'
        '  "sensor_mode": "physical_i2c",\n'
        '  "led_state": false,\n'
        '  "wifi_rssi": -54,\n'
        '  "ip": "192.168.43.105",\n'
        '  "uptime_sec": 1420\n'
        '}',
        title="CANONICAL MQTT TELEMETRY PAYLOAD SCHEMA"
    )

    # =========================================================================
    # 7. BACKEND ARCHITECTURE (FASTAPI & WEBSOCKETS)
    # =========================================================================
    h7 = doc.add_heading("7. Backend Architecture (Python FastAPI)", level=1)
    h7.paragraph_format.space_before = Pt(18)
    h7.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The backend server is implemented using Python 3.13 and FastAPI. It serves as the intelligent bridge linking the asynchronous "
        "world of MQTT to browser WebSocket clients.\n\n"
        "Key Backend Components:\n"
        "• Asynchronous Lifespan Management: Initializes the Paho-MQTT client background thread on startup and safely disconnects on shutdown.\n"
        "• Thread-Safe Event Loop Integration: Dispatches incoming MQTT message payloads into the asyncio event loop using asyncio.run_coroutine_threadsafe.\n"
        "• Circular History Buffer: Stores the 50 most recent telemetry readings in memory. When a client opens the dashboard, the backend instantly "
        "hydrates historical charts without waiting for future ticks.\n"
        "• ConnectionManager WebSocket Broadcaster: Tracks active browser connections and broadcasts JSON packets concurrently.\n"
        "• REST API Fallback Endpoints: Offers /api/status, /api/telemetry/latest, /api/telemetry/history, and /api/led for headless integrations."
    )

    # =========================================================================
    # 8. FRONTEND DASHBOARD (REACT + VITE GLASSMORPHISM UI)
    # =========================================================================
    h8 = doc.add_heading("8. Frontend Dashboard Architecture (React + Vite)", level=1)
    h8.paragraph_format.space_before = Pt(18)
    h8.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The user presentation layer is built as a single-page React 18 application with a dark-mode Cyber-Glassmorphism aesthetic:\n\n"
        "• Radial SVG AQI Gauge: Displays the real-time Air Quality Index (1 to 5) with color-coded gradients (Emerald for Excellent, Green for Good, "
        "Yellow for Moderate, Orange for Poor, Crimson for Hazardous).\n"
        "• 3D Illuminated LED Control Unit: Features an interactive, radially glowing diode bulb and master tactile toggle switch.\n"
        "• Metric Cards: Display Temperature (with °C/°F toggle), Relative Humidity, TVOC (ppb), and eCO2 (ppm).\n"
        "• Live SVG Trend Charts: High-performance vector charts plotting multi-channel environmental curves with gradient fills and tooltips.\n"
        "• Diagnostics Drawer: Direct technical inspector displaying raw JSON MQTT frames, Wi-Fi RSSI signal strength, and broker health."
    )

    # =========================================================================
    # 9. EXECUTION & QUICK-START GUIDE
    # =========================================================================
    h9 = doc.add_heading("9. Execution, Flashing & Operational Guide", level=1)
    h9.paragraph_format.space_before = Pt(18)
    h9.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "1. Flashing Firmware:\n"
        "   - Open firmware/esp32_iot_node/esp32_iot_node.ino in Arduino IDE.\n"
        "   - Install libraries: PubSubClient, ArduinoJson.\n"
        "   - Set Wi-Fi hotspot SSID and Password in the code.\n"
        "   - Select Board: ESP32 Dev Module, choose COM Port, and click Upload.\n\n"
        "2. One-Click Server Launcher:\n"
        "   - Double-click run_servers.bat in the project root directory.\n"
        "   - It automatically starts FastAPI (port 8000), Vite (port 5173), and launches your browser to http://localhost:5173.\n\n"
        "3. One-Click Shutdown:\n"
        "   - Double-click stop_servers.bat to terminate all background processes cleanly."
    )

    # =========================================================================
    # 10. CONCLUSION & FUTURE ROADMAP
    # =========================================================================
    h10 = doc.add_heading("10. Conclusion & Future Roadmap", level=1)
    h10.paragraph_format.space_before = Pt(18)
    h10.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "AeroSense IoT represents a complete, highly reliable, and extensible cyber-physical IoT architecture. "
        "By fusing native I2C register programming, dynamic MOX gas compensation, lightweight MQTT telemetry, and full-duplex WebSockets, "
        "the system delivers industrial-grade environmental monitoring in a compact and accessible format.\n\n"
        "Future Roadmap Enhancements:\n"
        "• Persistent Time-Series Database: Integration with InfluxDB or TimescaleDB for multi-month trend analysis.\n"
        "• Automated Ventilation Relays: Interfacing relay modules to automatically trigger exhaust fans or air purifiers when AQI > 3.\n"
        "• Over-the-Air (OTA) Updates: Remote firmware updating via Wi-Fi without requiring USB physical connection."
    )

    # Save final report
    out_file = os.path.join(os.getcwd(), "AeroSense_IoT_Complete_System_Report.docx")
    doc.save(out_file)
    print(f"Report built successfully at: {out_file}")

if __name__ == "__main__":
    build_comprehensive_report()
