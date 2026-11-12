"""
Generates a comprehensive Word (.docx) Project Report for AeroSense IoT
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2d, 0x37, 0x48)

    # =========================================================================
    # TITLE & HEADER
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(6)
    title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("AeroSense IoT")
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)

    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(18)
    subtitle_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = subtitle_p.add_run("Real-Time Environmental Climate Monitoring & Remote Actuator Control System\nESP32 • AHT21 • ENS160 • MQTT • FastAPI • React HD Dashboard")
    sub_run.font.name = 'Arial'
    sub_run.font.size = Pt(13)
    sub_run.font.color.rgb = RGBColor(0x02, 0x84, 0xc7)

    # Divider bar
    div_table = doc.add_table(rows=1, cols=1)
    div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = div_table.cell(0, 0)
    set_cell_background(cell, "0284c7")
    cell.paragraphs[0].paragraph_format.space_before = Pt(2)
    cell.paragraphs[0].paragraph_format.space_after = Pt(2)
    p_div = cell.paragraphs[0]
    r_div = p_div.add_run("")
    r_div.font.size = Pt(2)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 1. EXECUTIVE SUMMARY
    # =========================================================================
    h1 = doc.add_heading("1. Executive Summary", level=1)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(8)

    p = doc.add_paragraph(
        "AeroSense IoT is an end-to-end cyber-physical environmental monitoring and remote control system. "
        "The project integrates an ESP32 microcontroller, scientific-grade I2C sensors (AHT21 temperature and relative humidity sensor "
        "and ENS160 digital multi-gas sensor), an MQTT publish-subscribe messaging backbone, an asynchronous Python FastAPI backend server, "
        "and a high-definition (HD) React-based glassmorphism dashboard. In addition to continuous environmental telemetry, the system provides "
        "bidirectional remote actuator control, allowing users to toggle a physical LED on GPIO 4 with instant visual feedback."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(10)

    # Highlights box
    box_tbl = doc.add_table(rows=1, cols=1)
    box_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_cell = box_tbl.cell(0, 0)
    set_cell_background(b_cell, "f0f9ff")
    set_cell_margins(b_cell, top=140, bottom=140, left=200, right=200)
    bp = b_cell.paragraphs[0]
    bp_bold = bp.add_run("Key Architectural Highlights:\n")
    bp_bold.bold = True
    bp_bold.font.color.rgb = RGBColor(0x03, 0x69, 0xa1)
    bp.add_run(
        "• Native Direct I2C Sensing: Direct hardware register communication for AHT21 (0x38) and ENS160 (0x53).\n"
        "• Gas Accuracy Compensation: Dynamic temperature and humidity compensation injected from AHT21 into ENS160.\n"
        "• Lightweight Network Protocol: MQTT communication over local Wi-Fi mobile hotspot LAN.\n"
        "• Dual-Channel Web Architecture: FastAPI WebSocket telemetry streaming + REST API fallback.\n"
        "• Ultra-Clean HD UI: Cyber-glassmorphism theme, radial AQI gauges, live SVG trend lines, and illuminated 3D LED bulb."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # 2. HARDWARE SPECIFICATIONS & PINOUT
    # =========================================================================
    h2 = doc.add_heading("2. Hardware Architecture & Pinout", level=1)
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The hardware node consists of an ESP32 development board interfaced to environmental sensors via a shared two-wire "
        "I2C bus, accompanied by an actuator LED circuit connected to a dedicated general-purpose input/output pin (GPIO 4)."
    )

    # Table: Hardware Components
    t_hw = doc.add_table(rows=5, cols=4)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Component", "Interface", "Operating Voltage", "Function / Role"]
    for i, h in enumerate(headers):
        c = t_hw.cell(0, i)
        set_cell_background(c, "1e293b")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    hw_data = [
        ("ESP32 DevKit", "Wi-Fi (802.11 b/g/n), Dual-Core 240MHz", "3.3V Logic / 5V USB", "Central IoT Node, I2C Master & MQTT Client"),
        ("AHT21 Sensor", "I2C (Address 0x38)", "3.3V DC", "Ambient Temperature (-40 to 85°C) & Humidity (0-100% RH)"),
        ("ENS160 Sensor", "I2C (Address 0x53 / 0x52)", "3.3V DC", "Multi-Gas: TVOC (ppb), eCO2 (ppm), and AQI (1 to 5)"),
        ("LED Actuator", "GPIO 4 (via 220Ω Resistor)", "3.3V Signal", "Physical Actuator with Remote State Synchronization")
    ]
    for row_idx, data in enumerate(hw_data, start=1):
        for col_idx, text in enumerate(data):
            c = t_hw.cell(row_idx, col_idx)
            bg = "f8fafc" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            c.paragraphs[0].add_run(text)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Pinout Connections Table
    h3_pin = doc.add_heading("Hardware Pinout Wiring Table", level=2)
    h3_pin.paragraph_format.space_before = Pt(12)
    h3_pin.paragraph_format.space_after = Pt(6)

    t_pin = doc.add_table(rows=7, cols=4)
    t_pin.alignment = WD_TABLE_ALIGNMENT.CENTER
    pin_headers = ["Sensor / Module Pin", "ESP32 Target Pin", "Standard Color", "Wiring Notes"]
    for i, h in enumerate(pin_headers):
        c = t_pin.cell(0, i)
        set_cell_background(c, "0f766e")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    pin_data = [
        ("VCC (AHT21 & ENS160)", "3V3 Pin", "Red", "3.3V Regulated Power Output (Never connect 5V)"),
        ("GND (AHT21 & ENS160)", "GND Pin", "Black", "Common System Ground"),
        ("SDA (AHT21 & ENS160)", "GPIO 21 (D21)", "Green / Blue", "Shared I2C Serial Data Bus"),
        ("SCL (AHT21 & ENS160)", "GPIO 22 (D22)", "Yellow", "Shared I2C Serial Clock Bus"),
        ("LED Anode (+ Long Leg)", "GPIO 4 (D4)", "Purple / Orange", "Connected in series through 220Ω resistor"),
        ("LED Cathode (- Short Leg)", "GND Pin", "Black", "Direct connection to common Ground rail")
    ]
    for row_idx, data in enumerate(pin_data, start=1):
        for col_idx, text in enumerate(data):
            c = t_pin.cell(row_idx, col_idx)
            bg = "f0fdfa" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            c.paragraphs[0].add_run(text)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 3. COMMUNICATION ARCHITECTURE & MQTT PROTOCOL
    # =========================================================================
    h3 = doc.add_heading("3. Communication Architecture & MQTT Protocol", level=1)
    h3.paragraph_format.space_before = Pt(16)
    h3.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "Communication is orchestrated using the MQTT (Message Queuing Telemetry Transport) publish-subscribe model. "
        "The ESP32 microcontroller and the computer hosting the FastAPI backend and React frontend are connected to the same "
        "Wi-Fi Local Area Network (LAN) provided by a mobile phone hotspot (operating on the 2.4 GHz band)."
    )

    t_mqtt = doc.add_table(rows=5, cols=4)
    t_mqtt.alignment = WD_TABLE_ALIGNMENT.CENTER
    mqtt_headers = ["MQTT Topic", "Direction", "Payload Format", "Operational Description"]
    for i, h in enumerate(mqtt_headers):
        c = t_mqtt.cell(0, i)
        set_cell_background(c, "4338ca")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    mqtt_data = [
        ("aerosense_iot/sensors/data", "ESP32 ➔ Backend", "JSON", "Live telemetry packet published every 2.5s (T, H, TVOC, eCO2, AQI, RSSI)"),
        ("aerosense_iot/actuators/led/set", "Backend ➔ ESP32", '{"state": true/false}', "Command topic to toggle physical LED on GPIO 4"),
        ("aerosense_iot/actuators/led/status", "ESP32 ➔ Backend", '{"led_state": true/false}', "Hardware state confirmation feedback published upon toggle"),
        ("aerosense_iot/device/status", "ESP32 ➔ Backend", '{"status": "online/offline"}', "Heartbeat and MQTT Last Will and Testament (LWT) for link monitoring")
    ]
    for row_idx, data in enumerate(mqtt_data, start=1):
        for col_idx, text in enumerate(data):
            c = t_mqtt.cell(row_idx, col_idx)
            bg = "eef2ff" if row_idx % 2 == 1 else "ffffff"
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)
            c.paragraphs[0].add_run(text)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 4. BACKEND ARCHITECTURE (FASTAPI)
    # =========================================================================
    h4 = doc.add_heading("4. Backend Architecture (FastAPI & WebSockets)", level=1)
    h4.paragraph_format.space_before = Pt(16)
    h4.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The backend server is implemented in Python using the modern asynchronous FastAPI framework. "
        "It acts as a high-speed message broker bridge and state manager between the MQTT broker and browser clients."
    )
    doc.add_paragraph(
        "1. Embedded MQTT Client (Paho MQTT v2): Executes a non-blocking background loop subscribed to the telemetry and device topics. "
        "Incoming messages are pushed thread-safely into the asyncio event loop.\n"
        "2. In-Memory Time-Series Buffer: Maintains a circular buffer of the most recent 50 readings. When a new browser tab connects, "
        "this history is immediately transmitted to hydrate charts without waiting for incoming ticks.\n"
        "3. WebSocket Connection Manager (/ws/telemetry): Broadcasts instantaneous live JSON telemetry packets to all connected React clients.\n"
        "4. REST Endpoints (/api/status, /api/led, /api/telemetry/latest): Provides standard HTTP access for system health inspection and commands."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 5. FRONTEND DASHBOARD (REACT + VITE)
    # =========================================================================
    h5 = doc.add_heading("5. Frontend Dashboard Architecture (React + Vite)", level=1)
    h5.paragraph_format.space_before = Pt(16)
    h5.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The client-side interface is developed using React and Vite, featuring an ultra-premium HD Cyber-Glassmorphism theme. "
        "The design utilizes translucent frosted-glass cards, neon accent lighting (cyan, emerald, violet, amber), and fluid micro-animations."
    )
    doc.add_paragraph(
        "• Header & System Health: Displays live WebSocket connectivity, ESP32 status (Online/Offline), active MQTT broker host, and RSSI strength.\n"
        "• Air Quality Showcase: A dynamic SVG circular gauge representing the ENS160 Air Quality Index (AQI 1-5) with animated gradient stroke, "
        "color-coded status pills (Excellent, Good, Moderate, Poor, Hazardous), and physical hardware verification badge.\n"
        "• Remote LED Control Unit: Features an interactive 3D illuminated diode bulb with radial cyan light flares and a tactile master toggle switch.\n"
        "• Sensor Metric Grid: Dedicated cards for Ambient Temperature (°C/°F toggle), Relative Humidity (% RH), eCO2 (ppm), and TVOC (ppb).\n"
        "• Interactive Real-Time Trends Chart: Custom SVG time-series visualizer supporting multi-channel inspection (All Channels, Climate, Air Quality) "
        "with gradient area fills, glowing heads, and crosshair hover tooltips.\n"
        "• Telemetry Diagnostics Drawer: Real-time inspector for raw MQTT JSON payloads."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 6. ESP32 FIRMWARE DESIGN
    # =========================================================================
    h6 = doc.add_heading("6. ESP32 Firmware Implementation", level=1)
    h6.paragraph_format.space_before = Pt(16)
    h6.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The ESP32 firmware is written in Arduino C++ (esp32_iot_node.ino) and incorporates low-level native I2C drivers "
        "to ensure 100% reliable physical hardware communication without external library compilation issues."
    )
    doc.add_paragraph(
        "• Native AHT21 Driver: Directly writes soft-reset (0xBA) and measurement triggers (0xAC 0x33 0x00), reads the 6-byte payload over I2C, "
        "and computes temperature and relative humidity with 20-bit precision.\n"
        "• Native ENS160 Driver: Verifies device Part ID (0x0160) at register 0x00, sets Standard Operating Mode (0x02) at register 0x10, "
        "and reads DATA_STATUS, DATA_AQI, DATA_TVOC, and DATA_ECO2.\n"
        "• Live Compensation Injection: Automatically feeds the live temperature and humidity from AHT21 into the ENS160 compensation registers "
        "(0x13-0x16) to maximize chemical gas detection accuracy.\n"
        "• Fail-Safe Connection State Machine: Uses non-blocking loops to maintain Wi-Fi and MQTT connectivity, automatically re-subscribing "
        "upon any network interruption."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 7. EXECUTION & QUICK-START GUIDE
    # =========================================================================
    h7 = doc.add_heading("7. Execution & Operational Guide", level=1)
    h7.paragraph_format.space_before = Pt(16)
    h7.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "The project includes convenient one-click scripts for seamless execution on Windows:"
    )
    doc.add_paragraph(
        "1. One-Click Startup: Double-click 'run_servers.bat' in the project root directory. It automatically verifies Python venv and node_modules, "
        "launches the FastAPI backend on port 8000, launches Vite on port 5173, and opens your default browser to http://localhost:5173.\n"
        "2. One-Click Shutdown: Double-click 'stop_servers.bat' to terminate all background backend and frontend processes.\n"
        "3. ESP32 Upload: Open firmware/esp32_iot_node/esp32_iot_node.ino in Arduino IDE, select the COM port (COM5), and click Upload."
    )
    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # 8. CONCLUSION & FUTURE WORK
    # =========================================================================
    h8 = doc.add_heading("8. Conclusion & Future Enhancements", level=1)
    h8.paragraph_format.space_before = Pt(16)
    h8.paragraph_format.space_after = Pt(8)

    doc.add_paragraph(
        "AeroSense IoT successfully demonstrates a production-grade IoT architecture combining precision environmental sensing, "
        "bidirectional actuator control, low-latency telemetry streaming, and a modern web dashboard. "
        "Future enhancements may include SQLite/InfluxDB database persistence for long-term historical data logging, SMS/Email alerting "
        "thresholds for hazardous VOC or CO2 levels, and Over-The-Air (OTA) firmware update capabilities for remote maintenance."
    )

    # Save Document
    target_path = r"c:\Users\raksh\Desktop\IoT_Project\AeroSense_IoT_Project_Report.docx"
    doc.save(target_path)
    print(f"Report created successfully at: {target_path}")

if __name__ == "__main__":
    create_report()
