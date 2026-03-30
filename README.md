<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Courier+New&weight=700&size=28&duration=3000&pause=1000&color=00E6FF&center=true&vCenter=true&width=600&lines=◈+MARS+ROVER+MISSION+CONTROL+◈;v5.1+Enhanced+Edition;ESP32+%2B+PyQt5+Real-Time+Control" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-00e6ff?style=for-the-badge&logo=python&logoColor=white&labelColor=020A14)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-00ff91?style=for-the-badge&logo=qt&logoColor=white&labelColor=020A14)
![ESP32](https://img.shields.io/badge/ESP32-WebSocket-ffb900?style=for-the-badge&logo=espressif&logoColor=white&labelColor=020A14)
![Arduino](https://img.shields.io/badge/Arduino-C%2B%2B-ff2d37?style=for-the-badge&logo=arduino&logoColor=white&labelColor=020A14)
![License](https://img.shields.io/badge/License-MIT-b450ff?style=for-the-badge&labelColor=020A14)

<br/>

> **A full-featured, sci-fi styled real-time Mars Rover Mission Control interface.**
> Control an ESP32-powered rover over Wi-Fi with live telemetry, obstacle detection, servo control, and animated OLED feedback — all from a slick PyQt5 desktop GUI.

<br/>

</div>

---

## 🛸 Project Overview

This project is a complete ground-control system for a 4-wheel ESP32 rover. The **Python PyQt5 GUI** communicates with the **ESP32 firmware** over WebSocket (Wi-Fi), providing:

- Real-time sensor telemetry (temperature, pressure, altitude, distance)
- Keyboard-driven rover movement with instant stop safety
- Camera pan servo and gripper servo control
- Live scrolling telemetry charts and arc gauges
- Proximity obstacle radar with pulsing alerts
- Dual OLED displays on the rover itself
- An animated boot sequence and sci-fi HUD aesthetic

---

## 📸 Screenshots & Diagrams

### 🔌 Full Wiring Diagram

![Robot Wiring Diagram](1774878779185_Robot_Wiring.png)

> Complete power and signal wiring for the ESP32 rover — motors, servos, sensors, OLEDs, and buck converters all in one diagram.

---

### 🖥️ Software Architecture

![Station Architecture](1774878779186_Station.png)

> Mission Control software architecture: from startup dialog through boot screen to the full telemetry + control main window.

---

## ✨ Features

### 🖥️ Mission Control GUI (PyQt5)

| Feature | Description |
|---|---|
| 🎬 **Animated Boot Sequence** | 17-stage initialization animation with progress bar |
| 🌐 **Startup Config Dialog** | Enter your ESP32 WebSocket URL before launch |
| 📊 **Live Telemetry Charts** | Scrolling 80-sample history for Temp · Pressure · Altitude · Distance |
| 🎛️ **Arc Gauges** | Animated arc gauges for all 4 sensor channels |
| 🚨 **Obstacle Radar** | Proximity radar with WARN @ 80 cm / CRITICAL @ 30 cm |
| 📶 **Ping / Latency Display** | Live ping bar chart with color-coded latency |
| 🎮 **D-Pad Visualizer** | On-screen directional pad shows active movement |
| 🤖 **Rover State Renderer** | Animated rover graphic with wheel rotation |
| ⌨️ **Keyboard Overlay** | Press `?` to toggle a semi-transparent shortcut reference |
| 🛑 **Instant Stop** | Key-release triggers immediate motor stop command |
| 🛡️ **Safety Watchdog** | Auto-stops rover after 3 s of no movement command |
| 📋 **Mission Log** | Timestamped scrolling event log (50-line buffer) |

### 🤖 ESP32 Firmware (Arduino C++)

| Feature | Description |
|---|---|
| ⚡ **WebSocket Server** | Port 81 — receives commands, sends sensor data |
| 🏎️ **L298N Motor Control** | 4-wheel drive via IN1–IN4 GPIO pins |
| 📷 **Camera Pan Servo** | Smooth sweep on GPIO19 (0–180°, 10° steps) |
| 🦾 **Gripper Servo** | Open/close on GPIO18 (10° closed / 90° open) |
| 🌡️ **BMP280 Sensor** | Temperature · Pressure · Altitude over I²C |
| 📡 **HC-SR04 Ultrasonic** | Distance measurement on GPIO17/16 |
| 🖥️ **Dual SSD1306 OLEDs** | Left: rover animation · Right: camera + sensor data |
| ⏱️ **500 ms Watchdog** | Auto-stops motors if no command received |
| 🎬 **Boot Animation** | 3-stage welcome sequence on both OLEDs |

---

## 🗂️ Repository Structure

```
Mars-Rover/
│
├── 📄 main.py                         # PyQt5 Mission Control GUI (v5.1)
├── 📄 esp32_firmware.ino              # ESP32 Arduino firmware
│
├── 📸 1774878779185_Robot_Wiring.png  # Full wiring diagram
├── 📸 1774878779186_Station.png       # Software architecture diagram
│
└── 📄 README.md                       # This file
```

---

## ⚙️ Hardware Requirements

### 🔧 Components

| Component | Specification | Qty |
|---|---|---|
| **ESP32 DevKit** | Any 38-pin variant | 1 |
| **L298N H-Bridge** | Dual motor driver | 1 |
| **DC Motors** | 5V DC geared motors | 4 |
| **SG90 Servo** | Camera pan | 1 |
| **SG90 Servo** | Gripper | 1 |
| **BMP280** | Temp/Pressure/Altitude, I²C | 1 |
| **HC-SR04** | Ultrasonic distance | 1 |
| **SSD1306 OLED** | 128×64, I²C (0x3C) | 1 |
| **SSD1306 OLED** | 128×64, I²C (0x3D) | 1 |
| **Buck Converter** | LM2596 12V → 5V, 3A | 1 |
| **Battery** | 12V LiPo or lead-acid | 1 |

### 📌 ESP32 Pin Mapping

```
Motor Driver (L298N)         Servos
  IN1  → GPIO 27               Camera   → GPIO 19
  IN2  → GPIO 26               Gripper  → GPIO 18
  IN3  → GPIO 25
  IN4  → GPIO 33             Ultrasonic (HC-SR04)
                               TRIG     → GPIO 17
I²C Bus (BMP280 + OLEDs)       ECHO     → GPIO 16
  SDA  → GPIO 21
  SCL  → GPIO 22             I²C Addresses
                               BMP280   → 0x76 or 0x77
                               OLED L   → 0x3C
                               OLED R   → 0x3D
```

---

## 💻 Software Requirements

### Python GUI

```bash
Python 3.8+
PyQt5
websocket-client
```

Install dependencies:

```bash
pip install PyQt5 websocket-client
```

### Arduino / ESP32

Install these libraries via **Arduino Library Manager**:

- `WebSocketsServer` (by Markus Sattler)
- `ESP32Servo`
- `Adafruit GFX Library`
- `Adafruit SSD1306`
- `Adafruit BMP280 Library`

---

## 🚀 Getting Started

### 1️⃣ Flash the ESP32

1. Open `esp32_firmware.ino` in Arduino IDE
2. Update your Wi-Fi credentials:
   ```cpp
   const char* ssid     = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
3. Select your ESP32 board and COM port
4. Upload — the OLED will display the assigned IP address after connecting

### 2️⃣ Launch the GUI

```bash
git clone https://github.com/Muhammad-296/Mars-Rover.git
cd Mars-Rover
pip install PyQt5 websocket-client
python main.py
```

3. In the **Startup Dialog**, enter your rover's WebSocket URL:
   ```
   ws://192.168.x.x:81
   ```
4. Click **▶ INITIATE UPLINK** — enjoy the boot sequence, then take control!

---

## ⌨️ Keyboard Controls

| Key | Action |
|---|---|
| `↑` Arrow Up | Drive Forward |
| `↓` Arrow Down | Drive Backward |
| `←` Arrow Left | Turn Left |
| `→` Arrow Right | Turn Right |
| `A` | Pan Camera Right |
| `D` | Pan Camera Left |
| `O` | Open Gripper |
| `C` | Close Gripper |
| `?` | Toggle Keyboard Overlay |
| `ESC` | Exit Application |

> **Safety:** Releasing any movement key immediately sends a STOP command. A 3-second watchdog auto-stops the rover if the GUI freezes or disconnects.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│              PyQt5 Mission Control               │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │   Arc    │  │  Live    │  │ Rover State  │  │
│  │  Gauges  │  │  Charts  │  │  Visualizer  │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │   Keyboard Handler + Safety Watchdog     │   │
│  └──────────────────┬─────────────────────┘    │
│                     │ WebSocket Client           │
└─────────────────────┼───────────────────────────┘
                      │ Wi-Fi  ws://rover-ip:81
┌─────────────────────┼───────────────────────────┐
│              ESP32 Firmware                      │
│                     │                           │
│  ┌──────────┐  ┌────┴─────┐  ┌──────────────┐  │
│  │  L298N   │  │WebSocket │  │  BMP280 +    │  │
│  │  Motors  │  │  Server  │  │  HC-SR04     │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Camera  │  │ Gripper  │  │  Dual OLED   │  │
│  │  Servo   │  │  Servo   │  │   Displays   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 📡 WebSocket Protocol

| Command | Direction | Description |
|---|---|---|
| `F` | GUI → ESP32 | Drive Forward |
| `B` | GUI → ESP32 | Drive Backward |
| `L` | GUI → ESP32 | Turn Left |
| `R` | GUI → ESP32 | Turn Right |
| `S` | GUI → ESP32 | Instant Stop |
| `A` | GUI → ESP32 | Camera Pan Right |
| `D` | GUI → ESP32 | Camera Pan Left |
| `O` | GUI → ESP32 | Open Gripper |
| `C` | GUI → ESP32 | Close Gripper |
| `SENSOR` | GUI → ESP32 | Request sensor data |
| `PING` | GUI → ESP32 | Latency measurement |
| `T,P,A,D` | ESP32 → GUI | Sensor CSV: temp,pressure,alt,distance |
| `<angle>` | ESP32 → GUI | Camera servo position in degrees |
| `GRIPPER_OPEN` | ESP32 → GUI | Gripper state confirmation |
| `GRIPPER_CLOSE` | ESP32 → GUI | Gripper state confirmation |

---

## 🔒 Safety Features

- **Instant Stop on Key Release** — no key held = no movement
- **3-Second Auto-Stop Watchdog** — GUI-side timer halts rover if movement command stalls
- **500 ms ESP32 Watchdog** — firmware stops motors if no command received (covers Wi-Fi drops)
- **Obstacle Critical Alert** — visual + log warning at < 30 cm; caution at < 80 cm
- **Auto-Reconnect Loop** — GUI automatically retries WebSocket connection on failure

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for robotics enthusiasts**

⭐ Star this repo if it helped you build something awesome! ⭐

</div>
