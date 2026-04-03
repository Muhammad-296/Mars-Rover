<div align="center">

# 🚀 MARS ROVER MISSION CONTROL

**`v5.1 Enhanced Edition`**

![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-00ff91?style=for-the-badge&labelColor=001a0e)
![Version](https://img.shields.io/badge/VERSION-v5.1-00e6ff?style=for-the-badge&labelColor=001822)
![License](https://img.shields.io/badge/LICENSE-MIT-ffb900?style=for-the-badge&labelColor=1a1100)
![Platform](https://img.shields.io/badge/PLATFORM-ESP32-FF2D37?style=for-the-badge&logo=espressif&logoColor=white&labelColor=1a0003)
![GUI](https://img.shields.io/badge/GUI-PyQt5-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0f1a)
![Protocol](https://img.shields.io/badge/PROTOCOL-WebSocket-ff8800?style=for-the-badge&labelColor=1a0d00)

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white)

</div>

---

## 🛸 Mission Overview

> **Mars Rover Mission Control** is a full-stack robotics project combining a custom **ESP32-powered 6-wheel rover chassis** with a **Python PyQt5 GUI** for real-time telemetry, remote driving, camera panning, and gripper control — all over Wi-Fi via **WebSocket**.

---

## ⚡ Core Features

| Icon | Feature | Description |
|:----:|:--------|:------------|
| ⚙️ | **6 DC Motors** | Paired as 3 channels for tank-style differential drive — direction only, no PWM needed |
| 📷 | **ESP32-CAM on Servo** | Live camera with 0°–180° pan control, step 10° per command via GPIO 19 |
| 🌡️ | **BMP280 Sensor** | Real-time temperature, pressure & altitude over I²C at 0x76 / 0x77 |
| 📡 | **HC-SR04 Radar** | Ultrasonic proximity with **WARN @ 80 cm** and **CRIT @ 30 cm** threshold alerts |
| 🦾 | **Servo Gripper** | Object manipulation via GPIO 18 — Open: 90° · Close: 10° with state confirmation |
| 🟣 | **Custom PCB** | ESP32 breakout with all motor, servo & sensor headers fully populated |
| 🎮 | **Sci-Fi GUI** | PyQt5 Mission Control with live charts, arc gauges, radar display & safety watchdog |
| 🖥️ | **Dual OLED Display** | 128×64 panels at 0x3C and 0x3D — drive state left, sensors & camera right |

---

## 🗺️ System Architecture

```
┌─────────────────────────────────────┐         ┌─────────────────────────────────────┐
│      🖥️  MISSION CONTROL            │         │         ⚡ ESP32 FIRMWARE            │
│         Python PyQt5                │         │          Arduino C++                │
│                                     │         │                                     │
│  ┌─────────────────────────────┐    │         │  ┌─────────────────────────────┐    │
│  │ 🎮 PyQt5 GUI v5.1           │    │         │  │ 🔧 Motor Driver             │    │
│  │  Boot · KeyOverlay · Config │    │         │  │  L298D×2 · IN1:27 IN2:26   │    │
│  └─────────────────────────────┘    │         │  │  IN3:25  · IN4:33           │    │
│  ┌──────────────┐ ┌──────────────┐  │         │  └─────────────────────────────┘    │
│  │ 📊 Arc Gauges│ │📈 Telemetry  │  │         │  ┌──────────────┐ ┌──────────────┐  │
│  │  Temp·Press  │ │  4 Streams   │  │         │  │📷 Camera Servo│ │🦾 Gripper    │  │
│  │  Alt·Dist    │ │  80-pt Hist  │  │         │  │  GPIO 19      │ │  GPIO 18     │  │
│  └──────────────┘ └──────────────┘  │         │  │  0°–180°      │ │  10° / 90°   │  │
│  ┌──────────────┐ ┌──────────────┐  │         │  └──────────────┘ └──────────────┘  │
│  │🔴 Proximity  │ │📶 Latency    │  │         │  ┌──────────────┐ ┌──────────────┐  │
│  │  WARN 80 cm  │ │  Ping Graph  │  │         │  │🌡️ BMP280 I²C │ │🖥️ Dual OLED  │  │
│  │  CRIT 30 cm  │ │  Auto-Retry  │  │         │  │  Trig:17     │ │  0x3C  0x3D  │  │
│  └──────────────┘ └──────────────┘  │         │  │  Echo:16     │ │              │  │
└─────────────────────────────────────┘         │  └──────────────┘ └──────────────┘  │
                    │                           └─────────────────────────────────────┘
                    │                                           │
          ┌─────────▼─────────────────────────────────────────▼──────────┐
          │                   📡  WebSocket  ·  ws://ESP32_IP:81          │
          │                                                                │
          │  GUI → ESP32 :  F  B  L  R  S  A  D  O  C  SENSOR  PING      │
          │  ESP32 → GUI :  t,p,alt,d  ·  <angle>  ·  GRIPPER_STATE       │
          └────────────────────────────────────────────────────────────────┘
```

---

## 🔩 Hardware Components

| # | Component | Qty | GPIO / Bus | Details |
|:--:|:----------|:---:|:----------:|:--------|
| 01 | 🔵 **ESP32** DevKit / WROOM | 1 | — | Wi-Fi · WebSocket server port **81** |
| 02 | 📷 **ESP32-CAM** | 1 | GPIO **19** | Mounted on pan servo · 0°–180° |
| 03 | ⚙️ **DC Gear Motors** | 6 | IN1–IN4 | Paired 3+3 wired as **2 channels** |
| 04 | 🔌 **L298D Motor Driver** | 2 | 27 · 26 · 25 · 33 | No Enable pin · direction only |
| 05 | 🦾 **Servo — Camera Pan** | 1 | GPIO **19** | Range 0°–180° · Step 10° |
| 06 | 🤖 **Servo — Gripper** | 1 | GPIO **18** | Open: 90° · Close: 10° |
| 07 | 📡 **HC-SR04 Ultrasonic** | 1 | Trig **17** · Echo **16** | Proximity radar 0–500 cm |
| 08 | 🌡️ **BMP280** | 1 | I²C · 0x76/0x77 | Temperature · Pressure · Altitude |
| 09 | 🖥️ **SSD1306 OLED 128×64** | 2 | I²C · 0x3C · 0x3D | Left: Drive state · Right: Cam + Sensors |
| 10 | 🟣 **Custom PCB** | 1 | — | ESP32 breakout · all headers populated |

### ⚡ Motor Channel Wiring

| Channel | IN+ | IN− | Side | Motors |
|:-------:|:---:|:---:|:----:|:------:|
| **CH 1** | GPIO **27** | GPIO **26** | ◀ Left | 3 × DC motor (parallel) |
| **CH 2** | GPIO **25** | GPIO **33** | Right ▶ | 3 × DC motor (parallel) |

> Each channel drives **3 motors wired in parallel** — all spin together as one unit. No PWM / Enable pin needed.

---

## 🗃️ Pin Mapping

| Function | GPIO | Type | Notes |
|:---------|:----:|:----:|:------|
| `IN1` — Left Motor Forward | **27** | Digital Out | Left motor group |
| `IN2` — Left Motor Reverse | **26** | Digital Out | Left motor group |
| `IN3` — Right Motor Forward | **25** | Digital Out | Right motor group |
| `IN4` — Right Motor Reverse | **33** | Digital Out | Right motor group |
| Camera Servo Signal | **19** | PWM | 0°–180° · step 10° per command |
| Gripper Servo Signal | **18** | PWM | 10° = closed · 90° = open |
| Ultrasonic `TRIG` | **17** | Digital Out | HC-SR04 trigger pulse |
| Ultrasonic `ECHO` | **16** | Digital In | HC-SR04 echo receive |
| BMP280 `SDA` | SDA | I²C | Shared I²C bus |
| BMP280 `SCL` | SCL | I²C | Shared I²C bus |
| OLED Left `0x3C` | SDA / SCL | I²C | Drive state display |
| OLED Right `0x3D` | SDA / SCL | I²C | Camera gauge + sensor readout |

---

## 💻 Software Stack

| Layer | Technology | Details |
|:-----:|:----------|:--------|
| 🎮 **GUI** | Python 3 + PyQt5 v5.1 | Sci-fi Mission Control · Boot sequence · Keyboard overlay |
| 📡 **Communication** | WebSocket | `websocket-client` ↔ `WebSocketsServer` (port 81) |
| ⚡ **Firmware** | Arduino C++ / ESP32 | Motor · Servo · Sensor · OLED control loop |
| 🌡️ **Sensor Library** | Adafruit BMP280 | Temperature · Pressure · Altitude |
| 🖥️ **Display Library** | Adafruit SSD1306 + GFX | Dual OLED animated panels |
| 🦾 **Servo Library** | ESP32Servo | Smooth sweep movement |

---

## 🎮 GUI Panels

| Panel | What It Shows | Details |
|:-----:|:-------------|:--------|
| 📊 **Arc Gauges** | 4 animated dials | Temperature · Pressure · Altitude · Distance |
| 📈 **Telemetry Charts** | Scrolling line charts | 80-point history · 4 live data streams |
| 🔴 **Proximity Radar** | Concentric ring display | ⚠️ WARN @ **80 cm** · 🚫 CRIT @ **30 cm** |
| 📶 **Latency Monitor** | Bar graph ping history | Color-coded green / amber / red by latency |
| 📷 **Camera Panel** | Servo arc gauge | `A` ← pan left · pan right → `D` |
| 🦾 **Gripper Panel** | Position indicator | `O` → Open · `C` → Close |
| 🤖 **Rover Visualizer** | Animated state renderer | IDLE · FORWARD · BACKWARD · TURN L/R |
| 🕹️ **D-Pad Widget** | On-screen controller | Highlights active direction in real time |
| 📋 **Mission Log** | Timestamped event log | Auto-scrolling · last 50 events |
| 📡 **Status Bar** | Connection indicator | Signal bars · Ping ms · Clock |

### ✨ Special Features

| Feature | Description |
|:--------|:------------|
| 🚀 **Boot Sequence** | 17-stage POST initialization with animated progress bar |
| 🔗 **Startup Config Dialog** | Enter ESP32 IP at launch — no code editing needed |
| ⌨️ **Keyboard Shortcut Overlay** | Press `?` to toggle semi-transparent full-screen help panel |
| 🛡️ **Safety Watchdog** | Auto-stop motors after **3 s** of no key input |
| 🛑 **Instant Stop** | `S` sent on key release — bypasses all async queues |
| 🌐 **Hex-Grid Background** | Sci-fi background with depth-layered vignette |

---

## ⌨️ Keyboard Controls

| Key | Action | Category |
|:---:|:-------|:--------:|
| `↑` | Drive **Forward** | 🚗 Movement |
| `↓` | Drive **Backward** | 🚗 Movement |
| `←` | **Turn Left** | 🚗 Movement |
| `→` | **Turn Right** | 🚗 Movement |
| *(release)* | ⚡ **Instant Stop** | 🛑 Safety |
| `A` | Camera pan **Left** | 📷 Camera |
| `D` | Camera pan **Right** | 📷 Camera |
| `O` | **Open** gripper | 🦾 Gripper |
| `C` | **Close** gripper | 🦾 Gripper |
| `?` | Toggle keyboard overlay | ℹ️ App |
| `ESC` | Exit application | ℹ️ App |

---

## 📡 WebSocket Command Protocol

| Command | Direction | Action |
|:-------:|:---------:|:-------|
| `F` | GUI → ESP32 | 🟢 Move Forward |
| `B` | GUI → ESP32 | 🟡 Move Backward |
| `L` | GUI → ESP32 | 🔵 Turn Left |
| `R` | GUI → ESP32 | 🔵 Turn Right |
| `S` | GUI → ESP32 | 🔴 **INSTANT STOP** |
| `A` | GUI → ESP32 | 📷 Camera pan left |
| `D` | GUI → ESP32 | 📷 Camera pan right |
| `O` | GUI → ESP32 | 🦾 Open gripper |
| `C` | GUI → ESP32 | 🦾 Close gripper |
| `SENSOR` | GUI → ESP32 | 🌡️ Request sensor reading |
| `PING` | GUI → ESP32 | 📶 Latency measurement |
| `t,p,alt,d` | ESP32 → GUI | 📊 Sensor telemetry (CSV) |
| `<angle>` | ESP32 → GUI | 📷 Camera position (integer) |
| `GRIPPER_OPEN` | ESP32 → GUI | 🦾 Gripper state confirm |
| `GRIPPER_CLOSE` | ESP32 → GUI | 🦾 Gripper state confirm |

---

## 🛡️ Safety Features

| Feature | Trigger | Response |
|:--------|:-------:|:---------|
| ⚡ **Instant Stop** | Key released | `S` sent immediately · bypasses async queue |
| ⏱️ **GUI Watchdog** | No key input > **3 s** | Auto-sends `S` · resets state to IDLE |
| ⏱️ **ESP32 Watchdog** | No command > **500 ms** | Hardware-level motor cutoff |
| 🔄 **Auto-Reconnect** | Link dropped | GUI retries every **2 s** automatically |
| ⚠️ **Obstacle Warning** | Distance < **80 cm** | Yellow alert + log entry |
| 🚫 **Obstacle Critical** | Distance < **30 cm** | Red alert + log entry |

---

## 🖥️ OLED Display Panels

| OLED | I²C Address | Displays | Animation Style |
|:----:|:-----------:|:---------|:----------------|
| **Left** | `0x3C` | Drive state: IDLE / FWD / REV / TURN L / TURN R | Pulse rings · motion lines · turn arcs |
| **Right** | `0x3D` | Camera gauge + BMP280 + HC-SR04 + Gripper status | Sweeping servo arc · scan line |

> Both OLEDs run a **welcome animation** on boot: border reveal → particle burst → countdown → **GO!** splash

---

## 🚀 Getting Started

### 1️⃣ Flash the ESP32

**Install these Arduino libraries via Library Manager:**

| Library | Purpose |
|:--------|:--------|
| `ESP32Servo` | Servo motor control |
| `WebSockets` by Markus Sattler | WebSocket server |
| `Adafruit BMP280` | Temperature & pressure |
| `Adafruit SSD1306` | OLED display driver |
| `Adafruit GFX Library` | Graphics primitives |

**Update credentials** in `firmware/mars_rover_esp32.ino`:

```cpp
// Update Wi-Fi credentials before flashing
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
```

> Flash via Arduino IDE. The IP address appears on the **left OLED** after connecting to Wi-Fi.

---

### 2️⃣ Run the Python GUI

```bash
# Install Python dependencies
pip install PyQt5 websocket-client

# Launch Mission Control
python mars_rover_gui.py
```

Enter your rover's IP in the startup dialog:

```
ws://192.168.x.x:81
```

---

## 📁 Project Structure

```
mars-rover/
├── 📁 firmware/
│   └── mars_rover_esp32.ino      ← ESP32 Arduino firmware
├── 📁 gui/
│   └── mars_rover_gui.py         ← Python PyQt5 Mission Control v5.1
├── 📁 hardware/
│   ├── pcb/                      ← KiCad PCB design files
│   └── cad/                      ← SolidWorks 3D model files
├── 📁 docs/
│   ├── pcb_layout.png
│   └── rover_3d.png
└── README.md
```

---

## 🤝 Contributing

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/my-feature

# 3. Commit your changes
git commit -m "Add my feature"

# 4. Push and open a Pull Request
git push origin feature/my-feature
```

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**🚀 MARS ROVER MISSION CONTROL v5.1**

*ESP32 · Python · WebSocket · Real-Time Telemetry*

`Built for Exploration`

</div>
