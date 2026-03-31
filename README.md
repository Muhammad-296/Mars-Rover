# 🤖 Robot - Full Power & Wiring Diagram Project

A comprehensive robotics control system featuring an ESP32-based microcontroller with motor control, sensor integration, and real-time monitoring through WebSocket communication.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Hardware Architecture](#hardware-architecture)
- [System Components](#system-components)
- [Programming Languages](#programming-languages)
- [Features](#features)
- [Getting Started](#getting-started)
- [Documentation](#documentation)

## 📖 Project Overview

This project implements a fully integrated robotic system with advanced power management, motor control, sensor fusion, and a web-based user interface for real-time monitoring and control.

**Main Features:**
- 12V LiPo/Lead-acid battery power system
- Multi-motor control with H-bridge drivers
- ESP32 microcontroller with WiFi connectivity
- Real-time sensor data acquisition and display
- WebSocket-based communication protocol
- Safety watchdog with auto-stop functionality

## ⚙️ Hardware Architecture

### Power System
- **Main Battery:** 12V DC (LiPo/Lead-acid)
- **Buck Converter:** 12V IN → 5V OUT (LM2596-3A rated)
- **Power Rails:** 12V, 5V, 5V Logic, 3.3V

### Motor Control
- **Driver:** L298N H-Bridge Dual Motor Controller
- **Motors:** 4x 5V DC Motors (Front-Left, Front-Right, Rear-Left, Rear-Right)
- **Logic Level:** 5V DC

### Microcontroller
- **Main CPU:** ESP32 DevKit
- **GPIO Pins:** Multiple I/O for servo and sensor control
- **Communication:** WiFi + WebSocket capability
- **Voltage:** 3.3V logic

### Sensors & Actuators
- **Distance Sensor:** HC-SR04 Ultrasonic (5V, GPIO pins 330/470)
- **Camera Servo:** G90 Servo (GPIO19, 5V)
- **Gripper Servo:** G9VO Servo (GPIO18, 5V)
- **Pressure/Temperature:** BMP280 (I²C, 3.3V)
- **OLED Displays (Left & Right):** SDA/SCL I²C interface

## 🔌 System Components

### Power Distribution
| Component | Input | Output | Rating |
|-----------|-------|--------|--------|
| Buck Converter | 12V | 5V | 3A LM2596 |
| Main Battery | - | 12V | LiPo/Lead-acid |
| 5V Rail | 12V | 5V | Distributed |
| 3.3V Rail | 5V | 3.3V | ESP32 LDO |

### Control Interfaces
- **Keyboard Handler:** Arrow keys + A, D, O, C, ?, ESC commands
- **Safety Watchdog:** Key-release stop + 3s auto-stop timer
- **WebSocket Client:** Real-time communication via ESP32 WiFi

### Display & Monitoring
- **Arc Gauges:** Temperature, Pressure, Altitude, Distance
- **Live Charts:** 80-sample scrolling buffer
- **Rover Controls:** D-pad state visualization + servo gauges
- **Alerts:** Obstacle radar, ping status, connection status

## 💻 Programming Languages

This project supports development and configuration in multiple programming languages:

### **Embedded Systems Development**
- **C** - Low-level hardware control and microcontroller programming
- **C++** - Object-oriented firmware development
- **MicroPython** - Python implementation for ESP32 firmware
- **Arduino** - Simplified C++ framework for microcontroller development

### **Web & Frontend Development**
- **JavaScript** - WebSocket client, real-time UI updates
- **TypeScript** - Type-safe web application development
- **HTML** - Web interface structure
- **CSS** - User interface styling

### **Backend & Server**
- **Python** - Data processing, sensor algorithms, testing scripts


## ✨ Features

### 🎮 User Interface
- **Startup Dialog:** WebSocket URL configuration
- **17-Stage Boot Animation:** System initialization sequence
- **Main Window - MotorControl:**
  - Arc gauges for real-time sensor readings
  - Live scrolling history charts
  - Rover control visualization
  - System alerts and status monitoring

### 🔒 Safety Systems
- **Keyboard Handler:** Responsive input with emergency stop
- **Safety Watchdog:** Automatic stop on key release + 3-second timeout
- **Obstacle Detection:** Ultrasonic radar with collision warnings

### 📊 Monitoring & Logging
- **Mission Log:** Timestamped event buffer (50 lines)
- **Keyboard Overlay:** Help display with command reference
- **Real-time Sensor Polling:** 50ms RX timer + 1000/2000ms sensor intervals
- **80-Sample Data Buffers:** Rolling history for trend analysis

### 🌐 Communication
- **WiFi Connectivity:** ESP32-based wireless communication
- **WebSocket Protocol:** Low-latency real-time data streaming
- **Dual I²C Buses:** BMP280 + dual OLED displays

## 🚀 Getting Started

### Prerequisites
- ESP32 DevKit or compatible microcontroller
- L298N Motor Driver
- 4x DC Motors (5V)
- 2x G90/G9VO Servos
- HC-SR04 Ultrasonic Sensor
- BMP280 Sensor Module
- 2x OLED Displays (I²C)
- 12V Power Supply (LiPo/Lead-acid battery recommended)
- Development environment: PlatformIO, Arduino IDE, or MicroPython

### Hardware Assembly
1. Connect main battery to buck converter
2. Distribute power to 12V, 5V, and 3.3V rails
3. Connect L298N motor driver to GPIO pins and motors
4. Configure servo pins (GPIO18, GPIO19) for camera and gripper
5. Connect HC-SR04 sensor to GPIO330/470
6. Configure I²C buses for BMP280 and OLED displays

## 📚 Documentation

### Wiring Specifications
- **12V Rail:** Main battery → Buck converter, Motor driver
- **5V Rail:** Buck converter output → Motors, HC-SR04, Servos
- **5V Logic:** Buck converter → ESP32 logic level
- **3.3V Rail:** ESP32 LDO → Sensors, OLED displays
- **I²C Communication:** SDA/SCL for BMP280 and OLED displays
- **GND:** Common ground for all components

### Pin Configuration
| Function | GPIO | Voltage | Protocol |
|----------|------|---------|----------|
| Camera Servo | 19 | 5V | PWM |
| Gripper Servo | 18 | 5V | PWM |
| Ultrasonic Trig | 330 | 5V | Digital |
| Ultrasonic Echo | 470 | 5V | Digital |
| I²C (BMP280/OLED) | SDA/SCL | 3.3V | I²C |

## 📝 License

This project is provided as-is for educational and hobbyist purposes.

## 🤝 Contributing

Contributions are welcome! Please ensure code is properly documented and tested across supported programming languages.

## 📞 Support

For technical issues, hardware questions, or feature requests, please refer to the project documentation or open an issue in the repository.

---

**Last Updated:** March 31, 2026  
**Project Status:** Active Development  
