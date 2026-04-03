<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:02040A,30:001822,70:003344,100:00E6FF&height=200&section=header&text=🚀%20MARS%20ROVER&fontSize=52&fontColor=00E6FF&fontAlignY=45&desc=MISSION%20CONTROL%20v5.1%20%7C%20ESP32%20%7C%20Python%20GUI%20%7C%20WebSocket&descAlignY=68&descSize=16&descColor=00B8CC&animation=fadeIn" width="100%"/>

<br/>

<!-- Animated typing SVG — renders on GitHub.com -->
<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&weight=700&size=22&duration=2800&pause=900&color=00E6FF&background=00000000&center=true&vCenter=true&multiline=false&width=700&height=50&lines=◈+DRIVE+·+CAMERA+·+GRIPPER+·+TELEMETRY+◈;◈+BMP280+·+ULTRASONIC+·+OLED+·+WebSocket+◈;◈+Safety+Watchdog+·+Instant+Stop+·+Live+Charts+◈" alt="Mission capabilities" />

<br/><br/>

<!-- Shields with pulse animation via reloadable URL -->
<img src="https://img.shields.io/badge/🟢%20STATUS-OPERATIONAL-00ff91?style=for-the-badge&labelColor=001a0e" />
&nbsp;
<img src="https://img.shields.io/badge/📡%20VERSION-v5.1-00e6ff?style=for-the-badge&labelColor=001822" />
&nbsp;
<img src="https://img.shields.io/badge/⚖️%20LICENSE-MIT-ffb900?style=for-the-badge&labelColor=1a1100" />
&nbsp;
<img src="https://img.shields.io/badge/🔧%20PLATFORM-ESP32-ff2d37?style=for-the-badge&logo=espressif&logoColor=white&labelColor=1a0003" />
&nbsp;
<img src="https://img.shields.io/badge/🐍%20GUI-PyQt5-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0a0f1a" />
&nbsp;
<img src="https://img.shields.io/badge/📶%20PROTOCOL-WebSocket-ff8800?style=for-the-badge&labelColor=1a0d00" />

<br/><br/>

<!-- Animated skill icons -->
<img src="https://skillicons.dev/icons?i=python,cpp,arduino,github,vscode&theme=dark&perline=5" />

</div>

---

<div align="center">

## ◈ &nbsp; MISSION OVERVIEW &nbsp; ◈

</div>

> **Mars Rover Mission Control** is a full-stack robotics project combining a custom ESP32-powered 6-wheel rover chassis with a Python PyQt5 GUI for real-time telemetry, remote driving, camera panning, and gripper control — all over Wi-Fi via WebSocket.

The rover features:
- **6 DC motors** (paired as 3 channels) for tank-style differential drive
- **ESP32-CAM** on a servo for live camera panning
- **BMP280** environmental sensor (temperature, pressure, altitude)
- **HC-SR04** ultrasonic proximity radar
- **Servo gripper** for object manipulation
- **Custom PCB** designed around the ESP32 pinout
- **Sci-fi PyQt5 GUI** with live charts, arc gauges, OLED feedback & safety watchdog

---

## ◈ &nbsp; ROVER 3D MODEL

<div align="center">

| SolidWorks Assembly | Custom PCB Layout |
|:-------------------:|:-----------------:|
| *(4-wheel rocker chassis with front gripper & servo camera mount)* | *(ESP32 breakout with motor driver headers, servo ports, I²C bus)* |

> *See `/hardware/` for SolidWorks `.SLDPRT` / `.SLDASM` files and KiCad PCB sources.*

</div>

---

## ◈ &nbsp; SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────┐
│                     MISSION CONTROL  (Python)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐ │
│  │  PyQt5 GUI   │  │  Arc Gauges  │  │  Telem.    │  │ Obstacle │ │
│  │  v5.1        │  │  Temp/Press  │  │  Charts    │  │  Radar   │ │
│  │  Boot Anim   │  │  Alt/Dist    │  │  4 streams │  │  WARN/   │ │
│  │  Key Overlay │  │  Servo Pos   │  │  Scrolling │  │  CRIT    │ │
│  └──────┬───────┘  └──────────────┘  └────────────┘  └──────────┘ │
│         │  WebSocket (ws://ESP32_IP:81)                             │
└─────────┼───────────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────────────┐
│                          ESP32  (Arduino)                           │
│  ┌────────────┐  ┌───────────┐  ┌──────────┐  ┌────────────────┐  │
│  │  Motor     │  │  Camera   │  │  Gripper │  │  Sensors       │  │
│  │  Driver    │  │  Servo    │  │  Servo   │  │  BMP280 (I²C)  │  │
│  │  L298D ×2  │  │  GPIO 19  │  │  GPIO 18 │  │  HC-SR04       │  │
│  │  6 DC Mot. │  │  0–180°   │  │  10–90°  │  │  Trig:17/Echo:16│  │
│  └────────────┘  └───────────┘  └──────────┘  └────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Dual SSD1306 OLEDs (0x3C / 0x3D)  — Animated status panels │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ◈ &nbsp; HARDWARE COMPONENTS

| # | Component | Qty | Notes |
|---|-----------|:---:|-------|
| 1 | **ESP32** (DevKit / WROOM) | 1 | Wi-Fi + WebSocket server on port 81 |
| 2 | **ESP32-CAM** | 1 | Mounted on camera servo for pan control |
| 3 | **DC Gear Motors** | 6 | Paired 3+3 — each pair wired as one channel |
| 4 | **L298D Motor Driver** | 2 | No Enable pin used — full speed only |
| 5 | **Servo Motor (Camera)** | 1 | GPIO 19 · 0°–180° range |
| 6 | **Servo Motor (Gripper)** | 1 | GPIO 18 · Open: 90° · Close: 10° |
| 7 | **HC-SR04 Ultrasonic** | 1 | Trig: GPIO 17 · Echo: GPIO 16 |
| 8 | **BMP280** | 1 | I²C · Address 0x76 or 0x77 |
| 9 | **SSD1306 OLED 128×64** | 2 | I²C · 0x3C (Left) · 0x3D (Right) |
| 10 | **Custom PCB** | 1 | ESP32 breakout with all headers |

### Motor Wiring (L298D, no Enable)

```
Motor Channel 1  →  IN1 (GPIO 27)  /  IN2 (GPIO 26)   [ Left Side  × 3 motors ]
Motor Channel 2  →  IN3 (GPIO 25)  /  IN4 (GPIO 33)   [ Right Side × 3 motors ]
```

> Each channel drives **3 motors wired in parallel** — all three spin together as one unit.  
> No PWM / Enable pin required; direction only.

---

## ◈ &nbsp; PIN MAPPING

```
┌────────────────┬──────────┬─────────────────────────────┐
│  Function      │  GPIO    │  Notes                      │
├────────────────┼──────────┼─────────────────────────────┤
│  IN1 (L-Fwd)   │  27      │  Left motor group           │
│  IN2 (L-Rev)   │  26      │  Left motor group           │
│  IN3 (R-Fwd)   │  25      │  Right motor group          │
│  IN4 (R-Rev)   │  33      │  Right motor group          │
├────────────────┼──────────┼─────────────────────────────┤
│  Camera Servo  │  19      │  0–180°, step 10°           │
│  Gripper Servo │  18      │  10° closed / 90° open      │
├────────────────┼──────────┼─────────────────────────────┤
│  Ultrasonic    │  17 / 16 │  Trig / Echo                │
│  BMP280        │  SDA/SCL │  I²C shared bus             │
│  OLED Left     │  SDA/SCL │  I²C address 0x3C           │
│  OLED Right    │  SDA/SCL │  I²C address 0x3D           │
└────────────────┴──────────┴─────────────────────────────┘
```

---

## ◈ &nbsp; SOFTWARE STACK

<div align="center">

<img src="https://skillicons.dev/icons?i=python,cpp,arduino,github&theme=dark" />

</div>

<br/>

| Layer | Technology | Details |
|-------|-----------|---------|
| **GUI** | Python 3 + PyQt5 | Sci-fi themed Mission Control (v5.1) |
| **Communication** | WebSocket | `websocket-client` ↔ `WebSocketsServer` |
| **Firmware** | Arduino C++ (ESP32) | Motor + servo + sensor control |
| **Sensors** | Adafruit BMP280 | Temperature / pressure / altitude |
| **Display** | Adafruit SSD1306 | Dual OLED animated panels |

---

## ◈ &nbsp; GUI FEATURES

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║         MARS ROVER  MISSION CONTROL  v5.1  ◈                ║
╠══════════════════════════════════════════════════════════════╣
║  ARC GAUGES         ║  LIVE TELEMETRY CHARTS                 ║
║  • Temperature °C   ║  Scrolling history (80 pts)            ║
║  • Pressure hPa     ║  Temp / Pressure / Altitude / Distance ║
║  • Altitude m       ╠══════════════════════════════════════  ║
║  • Distance cm      ║  PROXIMITY RADAR                       ║
╠═════════════════════║  Concentric ring display               ║
║  CAMERA PAN         ║  WARN @ 80 cm  ·  CRIT @ 30 cm        ║
║  Servo arc gauge    ╠══════════════════════════════════════  ║
║  A ←  / → D         ║  LATENCY CHART                         ║
╠═════════════════════║  Bar graph ping history                 ║
║  GRIPPER            ╚══════════════════════════════════════  ║
║  O → Open           ║  MISSION LOG    ROVER STATE D-PAD      ║
║  C → Close          ║  Timestamped    Animated viz           ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

### GUI Highlights
- **Animated boot sequence** — 17-stage POST initialization with progress bar
- **Startup config dialog** — Enter ESP32 IP at launch (no code edit needed)
- **Keyboard shortcut overlay** — Press `?` to show/hide semi-transparent help panel
- **Safety watchdog** — Auto-stop motors after 3 s of no key input
- **Instant stop** — `S` command sent on key release with top priority
- **Fullscreen support** — `F11` toggle
- **Sci-fi hex-grid background** — Animated, depth-layered

---

## ◈ &nbsp; KEYBOARD CONTROLS

| Key | Action |
|-----|--------|
| `↑` Arrow Up | Drive **Forward** |
| `↓` Arrow Down | Drive **Backward** |
| `←` Arrow Left | **Turn Left** |
| `→` Arrow Right | **Turn Right** |
| *(release any arrow)* | **Instant Stop** |
| `A` | Camera pan **Right** |
| `D` | Camera pan **Left** |
| `O` | **Open** gripper |
| `C` | **Close** gripper |
| `?` | Toggle keyboard overlay |
| `ESC` | Exit application |

---

## ◈ &nbsp; WebSocket COMMAND PROTOCOL

| Command | Direction | ESP32 Action |
|---------|-----------|-------------|
| `F` | GUI → ESP32 | Move forward |
| `B` | GUI → ESP32 | Move backward |
| `L` | GUI → ESP32 | Turn left |
| `R` | GUI → ESP32 | Turn right |
| `S` | GUI → ESP32 | **STOP** (instant) |
| `A` | GUI → ESP32 | Camera pan left |
| `D` | GUI → ESP32 | Camera pan right |
| `O` | GUI → ESP32 | Open gripper |
| `C` | GUI → ESP32 | Close gripper |
| `SENSOR` | GUI → ESP32 | Request sensor reading |
| `PING` | GUI → ESP32 | Latency measurement |
| `t,p,alt,d` | ESP32 → GUI | Sensor telemetry CSV |
| `<angle>` | ESP32 → GUI | Camera position (int) |
| `GRIPPER_OPEN` | ESP32 → GUI | Gripper state confirm |
| `GRIPPER_CLOSE` | ESP32 → GUI | Gripper state confirm |

---

## ◈ &nbsp; GETTING STARTED

### 1. Flash the ESP32

**Install Arduino libraries:**
```
ESP32Servo
WebSockets (Markus Sattler)
Adafruit BMP280
Adafruit SSD1306
Adafruit GFX
```

**Update Wi-Fi credentials** in `firmware/mars_rover_esp32.ino`:
```cpp
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
```

Flash to your ESP32 via Arduino IDE. The IP address will display on the left OLED after connection.

---

### 2. Run the Python GUI

**Install dependencies:**
```bash
pip install PyQt5 websocket-client
```

**Launch:**
```bash
python mars_rover_gui.py
```

The startup dialog will appear — enter your ESP32's IP in the format:
```
ws://192.168.x.x:81
```

---

## ◈ &nbsp; PROJECT STRUCTURE

```
mars-rover/
├── firmware/
│   └── mars_rover_esp32.ino      # ESP32 Arduino firmware
├── gui/
│   └── mars_rover_gui.py         # Python PyQt5 Mission Control
├── hardware/
│   ├── pcb/                      # KiCad PCB files
│   └── cad/                      # SolidWorks 3D model files
├── docs/
│   ├── pcb_layout.png            # PCB render
│   └── rover_3d.png              # SolidWorks render
└── README.md
```

---

## ◈ &nbsp; SAFETY FEATURES

| Feature | Behavior |
|---------|----------|
| **Instant Stop** | `S` sent immediately on key release — bypasses async queue |
| **Safety Watchdog (GUI)** | Auto-stop if no movement command for **3 seconds** |
| **Safety Watchdog (ESP32)** | Auto-stop if no WebSocket command for **500 ms** |
| **Reconnection Loop** | GUI auto-reconnects on link failure every 2 s |
| **Obstacle Warning** | Visual + log alert at < 80 cm |
| **Obstacle Critical** | Pulsing red alert at < 30 cm |

---

## ◈ &nbsp; OLED DISPLAY PANELS

| OLED | Address | Content |
|------|---------|---------|
| **Left** | `0x3C` | Animated rover state (IDLE / FORWARD / BACKWARD / TURN LEFT / TURN RIGHT) |
| **Right** | `0x3D` | Camera servo arc gauge + sensor readout + gripper status |

Both OLEDs play a **welcome animation** on boot (countdown, particle burst, "GO!" splash).

---

## ◈ &nbsp; CONTRIBUTING

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## ◈ &nbsp; LICENSE

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

---

## ◈ &nbsp; REPO STATS

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=YOUR_USERNAME&repo=mars-rover&theme=react-dark&bg_color=02040A&color=00E6FF&line=00B8CC&point=00FF91&area=true&hide_border=true" width="100%" alt="Activity Graph"/>

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00E6FF,30:007799,70:001822,100:02040A&height=140&section=footer&text=Built%20for%20Exploration&fontSize=20&fontColor=00E6FF&fontAlignY=65&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=14&duration=4000&pause=2000&color=005566&center=true&vCenter=true&width=600&lines=◈+Mars+Rover+Mission+Control+v5.1+—+Enhanced+Edition+◈;◈+ESP32+·+Python+·+WebSocket+·+Real-Time+Telemetry+◈" alt="footer typing" />

<br/><br/>

<img src="https://img.shields.io/github/stars/YOUR_USERNAME/mars-rover?style=for-the-badge&color=ffb900&labelColor=1a1100&label=⭐%20STARS" />
&nbsp;
<img src="https://img.shields.io/github/forks/YOUR_USERNAME/mars-rover?style=for-the-badge&color=00ff91&labelColor=001a0e&label=🍴%20FORKS" />
&nbsp;
<img src="https://img.shields.io/github/issues/YOUR_USERNAME/mars-rover?style=for-the-badge&color=ff2d37&labelColor=1a0003&label=🐛%20ISSUES" />

</div>
