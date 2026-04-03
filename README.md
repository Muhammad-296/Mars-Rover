<div align="center">

# MARS ROVER

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

<br/>

![Stars](https://img.shields.io/github/stars/Muhammad-296/mars-rover?style=flat-square&color=ffb900&labelColor=1a1100&label=⭐%20Stars)
![Forks](https://img.shields.io/github/forks/Muhammad-296/mars-rover?style=flat-square&color=00ff91&labelColor=001a0e&label=🍴%20Forks)
![Issues](https://img.shields.io/github/issues/Muhammad-296/mars-rover?style=flat-square&color=ff2d37&labelColor=1a0003&label=🐛%20Issues)
![Last Commit](https://img.shields.io/github/last-commit/Muhammad-296/mars-rover?style=flat-square&color=00e6ff&labelColor=001822&label=📅%20Last%20Commit)

</div>

---

## 📋 Table of Contents

- [📊 Project Stats](#-project-stats-at-a-glance)
- [🛸 Mission Overview](#-mission-overview)
- [⚡ Core Features](#-core-features)
- [🗺️ System Architecture](#system-architecture)
- [🔌 Wiring Diagram](#wiring-diagram)
- [🔩 Hardware Components](#-hardware-components)
- [🗃️ Pin Mapping](#pin-mapping)
- [📍 ESP32 Pinout Visual](#-esp32-pinout-visual)
- [💻 Software Stack](#-software-stack)
- [🎮 GUI Panels](#-gui-panels)
- [⌨️ Keyboard Controls](#keyboard-controls)
- [📡 WebSocket Protocol](#-websocket-command-protocol)
- [🛡️ Safety Features](#safety-features)
- [🖥️ OLED Display Panels](#oled-display-panels)
- [🚀 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [🗺️ Roadmap](#roadmap)
- [❓ FAQ](#-faq)
- [🔧 Troubleshooting](#-troubleshooting)
- [📋 Changelog](#-changelog)
- [⚠️ Known Limitations](#️-known-limitations)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 📊 Project Stats at a Glance

| Stat | Value |
|:-----|:-----:|
| 🔧 **Hardware Components** | 10 |
| ⚙️ **DC Motors** | 6 |
| 🦾 **Servo Channels** | 2 (Camera + Gripper) |
| 📡 **WebSocket Commands** | 15 |
| 🛡️ **Safety Layers** | 6 |
| 🖥️ **OLED Panels** | 2 |
| 📊 **GUI Panels** | 10 |
| 📈 **Telemetry Streams** | 4 |
| 🌐 **Comm Protocol** | WebSocket Port 81 |
| ⚡ **Watchdog Timeout (ESP32)** | 500 ms |
| ⏱️ **Watchdog Timeout (GUI)** | 3 s |
| 🔄 **Reconnect Interval** | 2 s |

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

<a id="system-architecture"></a>
## 🗺️ System Architecture

```
┌──────────────────────────────────────────┐         ┌──────────────────────────────────────────┐
│         🖥️  MISSION CONTROL              │         │           ⚡ ESP32 FIRMWARE               │
│             Python PyQt5                 │         │            Arduino C++                   │
│                                          │         │                                          │
│  ┌────────────────────────────────────┐  │         │  ┌────────────────────────────────────┐  │
│  │ 🎮 PyQt5 GUI v5.1                  │  │         │  │ 🔧 Motor Driver (L298D × 2)        │  │
│  │  Boot Sequence · Key Overlay       │  │         │  │  CH1: IN1(27) IN2(26) ◀ Left       │  │
│  │  Startup Config · Watchdog Timer   │  │         │  │  CH2: IN3(25) IN4(33)  Right ▶     │  │
│  └────────────────────────────────────┘  │         │  └────────────────────────────────────┘  │
│                                          │         │                                          │
│  ┌─────────────────┐ ┌─────────────────┐ │         │  ┌─────────────────┐ ┌─────────────────┐ │
│  │ 📊 Arc Gauges   │ │ 📈 Telemetry    │ │         │  │ 📷 Camera Servo  │ │ 🦾 Gripper      │ │
│  │  Temp · Press   │ │  4 Streams      │ │         │  │  GPIO 19         │ │  GPIO 18        │ │
│  │  Alt  · Dist    │ │  80-pt History  │ │         │  │  0° to 180°      │ │  10° / 90°      │ │
│  └─────────────────┘ └─────────────────┘ │         │  └─────────────────┘ └─────────────────┘ │
│                                          │         │                                          │
│  ┌─────────────────┐ ┌─────────────────┐ │         │  ┌─────────────────┐ ┌─────────────────┐ │
│  │ 🔴 Proximity    │ │ 📶 Latency      │ │         │  │ 🌡️ BMP280        │ │ 🖥️ Dual OLED    │ │
│  │  WARN  @ 80 cm  │ │  Ping Graph     │ │         │  │  I²C · SDA/SCL  │ │  0x3C  · 0x3D  │ │
│  │  CRIT  @ 30 cm  │ │  Auto-Reconnect │ │         │  │  📡 HC-SR04      │ │  Left  · Right  │ │
│  └─────────────────┘ └─────────────────┘ │         │  │  Trig:17 Echo:16│ │                 │ │
└──────────────────────────────────────────┘         │  └─────────────────┘ └─────────────────┘ │
                       │                             └──────────────────────────────────────────┘
                       │                                              │
             ┌─────────▼──────────────────────────────────────────── ▼──────────┐
             │                  📡  WebSocket  ·  ws://ESP32_IP:81               │
             │                                                                    │
             │   GUI  ──► ESP32 :  F · B · L · R · S · A · D · O · C · PING    │
             │   ESP32 ──► GUI  :  t,p,alt,d · <angle> · GRIPPER_STATE           │
             └────────────────────────────────────────────────────────────────────┘
```

---

<a id="wiring-diagram"></a>
## 🔌 Wiring Diagram

```
                        ┌─────────────────────┐
                        │       ESP32          │
                        │                      │
          GPIO 27 ──────┤ IN1   ┌──────────┐   │
          GPIO 26 ──────┤ IN2   │  L298D   │───┼──── Left Motors  (×3 parallel)
                        │       │  Driver  │   │
          GPIO 25 ──────┤ IN3   │    #1    │───┼──── Right Motors (×3 parallel)
          GPIO 33 ──────┤ IN4   └──────────┘   │
                        │                      │
          GPIO 19 ──────┤─────── Camera Servo ─┼──── ESP32-CAM Pan (0°–180°)
          GPIO 18 ──────┤─────── Gripper Servo ┼──── Gripper (10°=close / 90°=open)
                        │                      │
          GPIO 17 ──────┤ TRIG ┌────────────┐  │
          GPIO 16 ──────┤ ECHO │  HC-SR04   │  │     Proximity Radar
                        │      └────────────┘  │
                        │                      │
            SDA ────────┤──┬── BMP280 ─────────┼──── Temp · Press · Alt
            SCL ────────┤  ├── OLED 0x3C ──────┼──── Left Panel  (Drive State)
                        │  └── OLED 0x3D ──────┼──── Right Panel (Sensors + Cam)
                        │                      │
                     3.3V / GND ───────────────┼──── All peripherals
                        └─────────────────────┘
```

---

## 🔩 Hardware Components

<details>
<summary><strong>📦 Click to expand full component list</strong></summary>

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

</details>

### ⚡ Motor Channel Wiring

| Channel | IN+ | IN− | Side | Motors |
|:-------:|:---:|:---:|:----:|:------:|
| **CH 1** | GPIO **27** | GPIO **26** | ◀ Left | 3 × DC motor (parallel) |
| **CH 2** | GPIO **25** | GPIO **33** | Right ▶ | 3 × DC motor (parallel) |

> Each channel drives **3 motors wired in parallel** — all spin together as one unit. No PWM / Enable pin needed.

---

<a id="pin-mapping"></a>
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

## 📍 ESP32 Pinout Visual

```
                    ┌──────────────────────────┐
               EN ──┤                          ├── GPIO 23
           GPIO 36 ──┤                          ├── GPIO 22  (SCL → BMP280 + OLEDs)
           GPIO 39 ──┤                          ├── GPIO 21  (SDA → BMP280 + OLEDs)
           GPIO 34 ──┤        ESP32             ├── GPIO 19  ◄── Camera Servo PWM
           GPIO 35 ──┤       WROOM              ├── GPIO 18  ◄── Gripper Servo PWM
           GPIO 32 ──┤                          ├── GPIO  5
           GPIO 33 ──┤ ◄── IN4 Right REV        ├── GPIO 17  ◄── HC-SR04 TRIG
           GPIO 25 ──┤ ◄── IN3 Right FWD        ├── GPIO 16  ◄── HC-SR04 ECHO
           GPIO 26 ──┤ ◄── IN2 Left  REV        ├── GPIO  4
           GPIO 27 ──┤ ◄── IN1 Left  FWD        ├── GPIO  2
           GPIO 14 ──┤                          ├── GPIO 15
           GPIO 12 ──┤                          ├── GND
              GND ──┤                          ├── VIN (5V)
                    └──────────────────────────┘

  Legend:  ◄── = used pin     (blank) = available
```

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

<details>
<summary><strong>🖥️ Click to expand all GUI panel details</strong></summary>

| Panel | What It Shows | Details |
|:-----:|:-------------|:--------|
| 📊 **Arc Gauges** | 4 animated dials | Temperature · Pressure · Altitude · Distance |
| 📈 **Telemetry Charts** | Scrolling line charts | 80-point history · 4 live data streams |
| 🔴 **Proximity Radar** | Concentric ring display | ⚠️ WARN @ **80 cm** · 🚫 CRIT @ **30 cm** |
| 📶 **Latency Monitor** | Bar graph ping history | Color-coded green / amber / red by latency |
| 📷 **Camera Panel** | Servo arc gauge | `A` ← pan left · pan right → `D` |
| 🦾 **Gripper Panel** | Position indicator | `O` → Open · `C` → Close |
| 🤖 **Rover Visualizer** | State renderer | IDLE · FORWARD · BACKWARD · TURN L/R |
| 🕹️ **D-Pad Widget** | On-screen controller | Highlights active direction in real time |
| 📋 **Mission Log** | Timestamped event log | Auto-scrolling · last 50 events |
| 📡 **Status Bar** | Connection indicator | Signal bars · Ping ms · Clock |

</details>

### ✨ Special Features

| Feature | Description |
|:--------|:------------|
| 🚀 **Boot Sequence** | 17-stage POST initialization with progress bar |
| 🔗 **Startup Config Dialog** | Enter ESP32 IP at launch — no code editing needed |
| ⌨️ **Keyboard Shortcut Overlay** | Press `?` to toggle semi-transparent full-screen help panel |
| 🛡️ **Safety Watchdog** | Auto-stop motors after **3 s** of no key input |
| 🛑 **Instant Stop** | `S` sent on key release — bypasses all async queues |
| 🌐 **Hex-Grid Background** | Sci-fi background with depth-layered vignette |

---

<a id="keyboard-controls"></a>
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

<a id="safety-features"></a>
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

<a id="oled-display-panels"></a>
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

<a id="roadmap"></a>
## 🗺️ Roadmap

| Status | Feature | Version |
|:------:|:--------|:-------:|
| ✅ | 6-motor differential drive | v1.0 |
| ✅ | WebSocket command protocol | v2.0 |
| ✅ | BMP280 + HC-SR04 telemetry | v3.0 |
| ✅ | Dual OLED display panels | v4.0 |
| ✅ | PyQt5 sci-fi GUI + safety watchdog | v5.0 |
| ✅ | Gripper servo + camera pan | v5.1 |
| 🔄 | Gamepad / joystick controller support | v5.2 |
| 🔄 | Live video stream in GUI | v5.2 |
| 🔄 | Autonomous obstacle avoidance mode | v6.0 |
| 🔄 | GPS telemetry integration | v6.0 |
| 🔄 | Mobile app (Flutter) | v7.0 |
| 💡 | Robotic arm (multi-joint) | Future |
| 💡 | AI object detection via camera | Future |

> ✅ Done &nbsp;·&nbsp; 🔄 In Progress / Planned &nbsp;·&nbsp; 💡 Ideas

---

## ❓ FAQ

<details>
<summary><strong>Q: What Wi-Fi frequency does the ESP32 use?</strong></summary>

The ESP32 operates on **2.4 GHz Wi-Fi only**. It does not support 5 GHz networks. Make sure your router is broadcasting on 2.4 GHz and that your credentials are correctly set in the firmware.

</details>

<details>
<summary><strong>Q: How do I find the ESP32's IP address?</strong></summary>

After flashing and powering on, the ESP32 connects to Wi-Fi and displays its IP address on the **left OLED panel**. You can also check your router's device list or use a network scanner like the **Fing** app.

</details>

<details>
<summary><strong>Q: Can I control the rover from outside my home network?</strong></summary>

Not by default. The WebSocket server runs on a local IP inside your LAN. To control the rover remotely you would need to set up **port forwarding** on your router or use a tunneling service like **ngrok**.

</details>

<details>
<summary><strong>Q: Can I add speed control (PWM) to the motors?</strong></summary>

Yes. The current firmware uses direction-only control. To add speed control, connect the **EN pins** of the L298D to ESP32 PWM-capable GPIOs and use `ledcWrite()` in the firmware.

</details>

<details>
<summary><strong>Q: Why does the GUI lose connection after a few minutes?</strong></summary>

This is usually a Wi-Fi power-saving issue on the router. Increasing the PING frequency in the GUI will keep the connection alive. You can also disable client idle timeout on your router.

</details>

<details>
<summary><strong>Q: What Python version is required?</strong></summary>

**Python 3.7 or higher** is recommended. Python 3.10 / 3.11 is the most stable combination with PyQt5.

</details>

---

## 🔧 Troubleshooting

<details>
<summary><strong>🔴 GUI cannot connect to rover</strong></summary>

| Check | Solution |
|:------|:---------|
| ESP32 IP address | Verify IP shown on left OLED matches what you entered in the dialog |
| Same network | Ensure PC and ESP32 are on the same 2.4 GHz Wi-Fi network |
| Port blocked | Check firewall — port **81** must be open |
| Firmware running | Re-flash if the OLED shows no IP or stays blank |
| WebSocket URL format | Must be exactly `ws://192.168.x.x:81` — no trailing slash |

</details>

<details>
<summary><strong>🔴 Motors not responding</strong></summary>

| Check | Solution |
|:------|:---------|
| Power supply | Motor driver needs separate **5–12V** supply — not USB alone |
| GPIO wiring | Verify IN1/IN2/IN3/IN4 match GPIOs 27/26/25/33 |
| L298D power LED | Should be lit when driver is powered |
| Motor wiring | Check each motor group is correctly wired in parallel |

</details>

<details>
<summary><strong>🔴 BMP280 not detected</strong></summary>

| Check | Solution |
|:------|:---------|
| I²C address | Try both `0x76` and `0x77` — depends on the SDO pin state |
| SDA / SCL wiring | Confirm correct ESP32 I²C pins are used |
| Pull-up resistors | I²C lines need 4.7kΩ pull-ups to 3.3V if not on breakout board |

</details>

<details>
<summary><strong>🔴 OLEDs not displaying</strong></summary>

| Check | Solution |
|:------|:---------|
| I²C addresses | Left must be `0x3C`, Right must be `0x3D` |
| Shared bus | All I²C devices (BMP280 + 2× OLED) share the same SDA/SCL |
| Power | OLEDs run on **3.3V** — do not connect to 5V |

</details>

<details>
<summary><strong>🔴 Servo jitter or not moving</strong></summary>

| Check | Solution |
|:------|:---------|
| PWM GPIO | Camera = GPIO 19, Gripper = GPIO 18 — verify correct pins |
| Power | Servos draw peak current — use a dedicated **5V 2A** supply |
| Library | Ensure `ESP32Servo` is installed, not the standard `Servo` library |

</details>

---

## 📋 Changelog

| Version | Date | Changes |
|:-------:|:----:|:--------|
| **v5.1** | 2024 | Added gripper servo · camera pan · dual OLED boot animation · auto-reconnect |
| **v5.0** | 2024 | Full PyQt5 GUI rewrite · safety watchdog · proximity radar · telemetry charts |
| **v4.0** | 2023 | Dual OLED display panels · drive state animations |
| **v3.0** | 2023 | BMP280 sensor integration · HC-SR04 ultrasonic · telemetry streaming |
| **v2.0** | 2023 | WebSocket protocol · Python GUI v1 · motor control |
| **v1.0** | 2023 | Basic ESP32 motor control · serial commands |

---

## ⚠️ Known Limitations

| # | Limitation | Details |
|:--:|:-----------|:--------|
| 1 | **No speed control** | Motors run at full voltage — no PWM speed adjustment in current firmware |
| 2 | **2.4 GHz Wi-Fi only** | ESP32 does not support 5 GHz networks |
| 3 | **Single client** | WebSocket server handles one GUI client at a time |
| 4 | **No video stream in GUI** | ESP32-CAM stream must be viewed separately via browser |
| 5 | **No encryption** | WebSocket communication is unencrypted (ws://, not wss://) |
| 6 | **Fixed sensor poll rate** | Sensor data is polled on `SENSOR` command only — no push mode |
| 7 | **Windows / Linux tested** | GUI may need adjustments for macOS PyQt5 rendering |

---

## 🤝 Contributing

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/my-feature

# 3. Commit your changes
git commit -m "feat: add my feature"

# 4. Push and open a Pull Request
git push origin feature/my-feature
```

**Contribution areas welcome:**
- 🎮 GUI improvements and new panels
- ⚡ Firmware optimizations
- 📡 New sensor integrations
- 🌐 Mobile app development
- 📖 Documentation improvements

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**🚀 MARS ROVER MISSION CONTROL v5.1**

*ESP32 · Python · WebSocket · Real-Time Telemetry*

`Built for Exploration`

</div>
