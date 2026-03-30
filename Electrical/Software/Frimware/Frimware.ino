/*
  ESP32 Motor + Servo (Camera & Gripper) + Dual OLED WebSocket Controller
  ─────────────────────────────────────────────────────────────────────────────
  FIXED VERSION WITH CORRECT DIRECTION MAPPING:
  - UP arrow → FORWARD
  - DOWN arrow → BACKWARD  
  - LEFT arrow → TURN LEFT
  - RIGHT arrow → TURN RIGHT
  - A key → CAMERA LEFT
  - D key → CAMERA RIGHT
  
  INSTANT STOP FEATURE:
  - Immediate motor stop on 'S' command
  - Watchdog timer stops motors if no command received for 500ms
*/

#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ESP32Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BMP280.h>

// ── Wi-Fi ─────────────────────────────────────────────────────────────────────
const char* ssid     = "faridas iphone";
const char* password = "didaabdelaziz";

// ── Motor pins ────────────────────────────────────────────────────────────────
#define IN1 27
#define IN2 26
#define IN3 25
#define IN4 33

// ── Servo pins ────────────────────────────────────────────────────────────────
#define CAMERA_SERVO_PIN  19
#define GRIPPER_SERVO_PIN 18

// ── Camera Servo Settings ────────────────────────────────────────────────────
#define CAM_SERVO_STEP   10
#define CAM_SERVO_MIN     0
#define CAM_SERVO_MAX   180
#define CAM_SERVO_CENTER 90

// ── Gripper Servo Settings ───────────────────────────────────────────────────
#define GRIPPER_OPEN_ANGLE  90
#define GRIPPER_CLOSE_ANGLE 10

// ── OLED ──────────────────────────────────────────────────────────────────────
#define OLED_WIDTH  128
#define OLED_HEIGHT  64
#define OLED_RESET   -1

Adafruit_SSD1306 oledL(OLED_WIDTH, OLED_HEIGHT, &Wire, OLED_RESET);
Adafruit_SSD1306 oledR(OLED_WIDTH, OLED_HEIGHT, &Wire, OLED_RESET);

// ── SENSOR PINS ───────────────────────────────────────────────────────────────
#define TRIG_PIN 17
#define ECHO_PIN 16

// ── Sensor objects ────────────────────────────────────────────────────────────
Adafruit_BMP280 bmp;

// ── Motor / rover state ───────────────────────────────────────────────────────
enum RoverState { IDLE, FORWARD, BACKWARD, TURN_LEFT, TURN_RIGHT };
RoverState roverState = IDLE;

// ── Sensor readings ───────────────────────────────────────────────────────────
float temperature = 0;
float pressure = 0;
float altitude = 0;
float distance_cm = 0;
unsigned long lastSensorRead = 0;
const unsigned long SENSOR_INTERVAL = 500;

// ── Animation tick ────────────────────────────────────────────────────────────
uint32_t animTick = 0;
uint32_t lastAnimMs = 0;
#define ANIM_INTERVAL_MS 80

// ── Servo objects ─────────────────────────────────────────────────────────────
Servo cameraServo;
Servo gripperServo;

int cameraPos = CAM_SERVO_CENTER;
int gripperPos = GRIPPER_CLOSE_ANGLE;

// ── Watchdog timer for instant stop ──────────────────────────────────────────
unsigned long lastCommandTime = 0;
const unsigned long COMMAND_TIMEOUT_MS = 500;  // Stop after 500ms of no commands

WebSocketsServer webSocket = WebSocketsServer(81);

// ── Functions declarations ──────────────────────────────────────────────────────
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void stopMotors();
void moveCameraLeft(uint8_t clientNum);
void moveCameraRight(uint8_t clientNum);
void openGripper(uint8_t clientNum);
void closeGripper(uint8_t clientNum);
void setGripperAngle(uint8_t clientNum, int angle);
void moveServoSmooth(Servo &servo, int &current, int target);
void sendSensorData(uint8_t clientNum);
void readSensors();

void oledWelcome();
void updateLeftOLED();
void updateRightOLED();

void drawRoverIdle(Adafruit_SSD1306& d, uint32_t t);
void drawRoverForward(Adafruit_SSD1306& d, uint32_t t);
void drawRoverBackward(Adafruit_SSD1306& d, uint32_t t);
void drawRoverTurnLeft(Adafruit_SSD1306& d, uint32_t t);
void drawRoverTurnRight(Adafruit_SSD1306& d, uint32_t t);
void drawCameraPanel(Adafruit_SSD1306& d, uint32_t t);
void drawSensorData(Adafruit_SSD1306& d);
void drawGripperStatus(Adafruit_SSD1306& d);

// ─────────────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println("Mars Rover ESP32 Starting...");
  Serial.println("DIRECTION MAPPING:");
  Serial.println("  UP → FORWARD");
  Serial.println("  DOWN → BACKWARD");
  Serial.println("  LEFT → TURN LEFT");
  Serial.println("  RIGHT → TURN RIGHT");
  Serial.println("  A → CAMERA LEFT");
  Serial.println("  D → CAMERA RIGHT");

  // Motor pins
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  stopMotors();

  // Ultrasonic pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Servos
  cameraServo.attach(CAMERA_SERVO_PIN);
  cameraServo.write(cameraPos);
  
  gripperServo.attach(GRIPPER_SERVO_PIN);
  gripperServo.write(gripperPos);

  // ── OLED init
  Wire.begin();
  oledL.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  oledR.begin(SSD1306_SWITCHCAPVCC, 0x3D);

  // ── BMP280 init
  if (!bmp.begin(0x76)) {
    if (!bmp.begin(0x77)) {
      Serial.println("BMP280 not found!");
    } else {
      Serial.println("BMP280 found at 0x77");
    }
  } else {
    Serial.println("BMP280 found at 0x76");
  }
  
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);

  oledWelcome();

  // ── Wi-Fi
  WiFi.begin(ssid, password);

  oledL.clearDisplay();
  oledR.clearDisplay();
  for (auto* d : {&oledL, &oledR}) {
    d->setTextColor(SSD1306_WHITE);
    d->setTextSize(1);
    d->setCursor(16, 20);
    d->print("Connecting WiFi");
    d->setCursor(40, 38);
    d->print("please wait");
    d->display();
  }

  while (WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  
  Serial.println();
  Serial.println(WiFi.localIP());

  // Show IP on left OLED
  oledL.clearDisplay();
  oledL.setTextSize(1);
  oledL.setTextColor(SSD1306_WHITE);
  oledL.setCursor(4, 10);
  oledL.print("WiFi Connected!");
  oledL.setCursor(4, 28);
  oledL.print("IP:");
  oledL.setCursor(4, 40);
  oledL.print(WiFi.localIP());
  oledL.display();

  oledR.clearDisplay();
  oledR.setTextSize(1);
  oledR.setTextColor(SSD1306_WHITE);
  oledR.setCursor(20, 24);
  oledR.print("WS Port: 81");
  oledR.setCursor(12, 40);
  oledR.print("Awaiting client");
  oledR.display();

  delay(1500);

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  
  readSensors();
  lastCommandTime = millis();
  
  Serial.println("ESP32 Ready - Instant Stop Enabled");
}

// ─────────────────────────────────────────────────────────────────────────────
void loop() {
  // Process WebSocket commands immediately (highest priority)
  webSocket.loop();
  
  // Watchdog timer - auto stop if no commands received
  if (roverState != IDLE && (millis() - lastCommandTime > COMMAND_TIMEOUT_MS)) {
    stopMotors();
    roverState = IDLE;
    Serial.println("WATCHDOG: Auto-stop triggered (command timeout)");
  }

  // Read sensors periodically
  unsigned long now = millis();
  if (now - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = now;
    readSensors();
  }

  // Update OLED animations (lowest priority)
  if (now - lastAnimMs >= ANIM_INTERVAL_MS) {
    lastAnimMs = now;
    animTick++;
    updateLeftOLED();
    updateRightOLED();
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// SENSOR FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────
void readSensors() {
  temperature = bmp.readTemperature();
  pressure = bmp.readPressure() / 100.0F;
  altitude = bmp.readAltitude(1013.25);
  
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) {
    distance_cm = 999;
  } else {
    distance_cm = duration * 0.034 / 2;
  }
}

void sendSensorData(uint8_t clientNum) {
  String data = String(temperature, 1) + "," +
                String(pressure, 1) + "," +
                String(altitude, 1) + "," +
                String(distance_cm, 1);
  webSocket.sendTXT(clientNum, data);
}

// ─────────────────────────────────────────────────────────────────────────────
// SERVO SMOOTH MOVEMENT
// ─────────────────────────────────────────────────────────────────────────────
void moveServoSmooth(Servo &servo, int &current, int target) {
  target = constrain(target, 0, 180);
  
  if (target > current) {
    for (int i = current; i <= target; i++) {
      servo.write(i);
      delay(6);
    }
  } else if (target < current) {
    for (int i = current; i >= target; i--) {
      servo.write(i);
      delay(6);
    }
  }
  current = target;
}

// ─────────────────────────────────────────────────────────────────────────────
// GRIPPER CONTROL FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────
void openGripper(uint8_t clientNum) {
  moveServoSmooth(gripperServo, gripperPos, GRIPPER_OPEN_ANGLE);
  if (clientNum != 255) {
    webSocket.sendTXT(clientNum, "GRIPPER_OPEN");
  }
}

void closeGripper(uint8_t clientNum) {
  moveServoSmooth(gripperServo, gripperPos, GRIPPER_CLOSE_ANGLE);
  if (clientNum != 255) {
    webSocket.sendTXT(clientNum, "GRIPPER_CLOSE");
  }
}

void setGripperAngle(uint8_t clientNum, int angle) {
  angle = constrain(angle, 0, 180);
  moveServoSmooth(gripperServo, gripperPos, angle);
  if (clientNum != 255) {
    webSocket.sendTXT(clientNum, "GRIPPER_ANGLE:" + String(angle));
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// WEBSOCKET EVENT HANDLER - FIXED DIRECTION MAPPING
// ─────────────────────────────────────────────────────────────────────────────
void sendAngle(uint8_t clientNum) {
  String angleStr = String(cameraPos);
  webSocket.sendTXT(clientNum, angleStr);
}

void webSocketEvent(uint8_t clientNum, WStype_t type,
                    uint8_t* payload, size_t length) {

  if (type == WStype_CONNECTED) {
    Serial.println("Client connected");
    sendAngle(clientNum);
    sendSensorData(clientNum);
  }
  else if (type == WStype_DISCONNECTED) {
    Serial.println("Client disconnected");
    stopMotors();
    roverState = IDLE;
  }
  else if (type == WStype_TEXT) {
    String cmd = String((char*)payload);
    cmd.trim();
    
    // Update last command time for watchdog
    lastCommandTime = millis();
    
    // Log received command
    Serial.print("CMD: ");
    Serial.println(cmd);
    
    // Motor commands - CORRECTED DIRECTION MAPPING
    if      (cmd == "F") { 
      moveForward(); 
      roverState = FORWARD; 
      Serial.println("→ FORWARD");
    }
    else if (cmd == "B") { 
      moveBackward(); 
      roverState = BACKWARD; 
      Serial.println("→ BACKWARD");
    }
    else if (cmd == "L") { 
      turnRight();   // L → RIGHT
    }
    else if (cmd == "R") { 
      turnLeft();    // R → LEFT
    }
    else if (cmd == "S") { 
      stopMotors(); 
      roverState = IDLE; 
      Serial.println("→ STOP (INSTANT)");
    }
    
    // Camera servo commands - CORRECTED: A = LEFT, D = RIGHT
    else if (cmd == "A") { 
      moveCameraLeft(clientNum);
    }
    else if (cmd == "D") { 
      moveCameraRight(clientNum);
    }
    
    // Gripper commands
    else if (cmd == "O") { 
      openGripper(clientNum);
      Serial.println("→ GRIPPER OPEN");
    }
    else if (cmd == "C") { 
      closeGripper(clientNum);
      Serial.println("→ GRIPPER CLOSE");
    }
    
    // Sensor request
    else if (cmd == "SENSOR") { 
      sendSensorData(clientNum);
      Serial.println("→ SENSOR DATA SENT");
    }
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// MOTOR CONTROL FUNCTIONS - CORRECTED DIRECTION MAPPING
// ─────────────────────────────────────────────────────────────────────────────
void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void moveBackward() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  // Turn left: right wheels forward, left wheels backward
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);  // Left motor backward
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // Right motor forward
}

void turnRight() {
  // Turn right: left wheels forward, right wheels backward
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // Left motor forward
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);  // Right motor backward
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void moveCameraLeft(uint8_t clientNum) {
  cameraPos -= CAM_SERVO_STEP;
  if (cameraPos < CAM_SERVO_MIN) cameraPos = CAM_SERVO_MIN;
  cameraServo.write(cameraPos);
  sendAngle(clientNum);
}

void moveCameraRight(uint8_t clientNum) {
  cameraPos += CAM_SERVO_STEP;
  if (cameraPos > CAM_SERVO_MAX) cameraPos = CAM_SERVO_MAX;
  cameraServo.write(cameraPos);
  sendAngle(clientNum);
}

// ─────────────────────────────────────────────────────────────────────────────
// OLED DISPLAY FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────
void oledWelcome() {
  for (int step = 0; step < 64; step += 4) {
    oledL.clearDisplay();
    oledR.clearDisplay();
    for (auto* d : {&oledL, &oledR}) {
      d->drawRect(0, 0, 128, 64, SSD1306_WHITE);
      if (step > 8) d->drawRect(2, 2, 124, 60, SSD1306_WHITE);
      if (step > 20) {
        d->setTextSize(2);
        d->setTextColor(SSD1306_WHITE);
        d->setCursor(10, 10);
        d->print("MARS");
        d->setCursor(10, 32);
        d->print("ROVER");
      }
      d->display();
    }
    delay(30);
  }
  delay(400);

  for (int frame = 0; frame < 18; frame++) {
    oledL.clearDisplay();
    oledR.clearDisplay();
    for (auto* d : {&oledL, &oledR}) {
      for (int s = 0; s < 30; s++) {
        int sx = (s * 37 + frame * 4) % 128;
        int sy = (s * 23) % 64;
        d->drawPixel(sx, sy, SSD1306_WHITE);
      }
      d->setTextSize(1);
      d->setTextColor(SSD1306_WHITE);
      d->setCursor(22, 28);
      d->print("MISSION CTRL");
    }
    oledL.setCursor(22, 42);
    oledL.print(" DRIVE SYS");
    oledR.setCursor(22, 42);
    oledR.print("  CAM SYS");
    oledL.display();
    oledR.display();
    delay(60);
  }

  for (int c = 3; c >= 1; c--) {
    oledL.clearDisplay();
    oledR.clearDisplay();
    for (auto* d : {&oledL, &oledR}) {
      d->drawRect(0, 0, 128, 64, SSD1306_WHITE);
      d->setTextSize(4);
      d->setTextColor(SSD1306_WHITE);
      d->setCursor(52, 12);
      d->print(c);
      d->setTextSize(1);
      d->setCursor(28, 52);
      d->print("INITIALIZING");
      d->display();
    }
    delay(500);
  }

  oledL.clearDisplay();
  oledR.clearDisplay();
  for (auto* d : {&oledL, &oledR}) {
    d->drawRect(0, 0, 128, 64, SSD1306_WHITE);
    d->setTextSize(3);
    d->setTextColor(SSD1306_WHITE);
    d->setCursor(32, 18);
    d->print("GO!");
    d->display();
  }
  delay(600);
}

void updateLeftOLED() {
  oledL.clearDisplay();
  switch (roverState) {
    case IDLE:       drawRoverIdle(oledL, animTick);      break;
    case FORWARD:    drawRoverForward(oledL, animTick);   break;
    case BACKWARD:   drawRoverBackward(oledL, animTick);  break;
    case TURN_LEFT:  drawRoverTurnLeft(oledL, animTick);  break;
    case TURN_RIGHT: drawRoverTurnRight(oledL, animTick); break;
  }
  oledL.display();
}

void updateRightOLED() {
  oledR.clearDisplay();
  drawCameraPanel(oledR, animTick);
  drawSensorData(oledR);
  drawGripperStatus(oledR);
  oledR.display();
}

void drawGripperStatus(Adafruit_SSD1306& d) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(88, 48);
  
  if (gripperPos <= GRIPPER_CLOSE_ANGLE + 10) {
    d.print("GRIP: CLOSED");
  } else if (gripperPos >= GRIPPER_OPEN_ANGLE - 10) {
    d.print("GRIP: OPEN");
  } else {
    d.print("GRIP: " + String(gripperPos) + "°");
  }
}

void drawSensorData(Adafruit_SSD1306& d) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  
  d.setCursor(2, 48);
  d.print("T:");
  d.print(temperature, 1);
  d.print("C");
  
  d.setCursor(48, 48);
  d.print("P:");
  d.print(pressure, 0);
  d.print("hPa");
  
  d.setCursor(2, 56);
  d.print("D:");
  if (distance_cm >= 999) {
    d.print(">5m");
  } else {
    d.print(distance_cm, 0);
    d.print("cm");
  }
  
  d.setCursor(70, 56);
  d.print("A:");
  d.print(altitude, 0);
  d.print("m");
}

void drawRoverBody(Adafruit_SSD1306& d, int cx, int cy) {
  d.drawRoundRect(cx - 14, cy - 10, 28, 20, 4, SSD1306_WHITE);
  d.fillRect(cx - 18, cy - 8, 5, 16, SSD1306_WHITE);
  d.fillRect(cx + 13, cy - 8, 5, 16, SSD1306_WHITE);
  d.fillCircle(cx, cy - 4, 3, SSD1306_WHITE);
  d.drawLine(cx, cy - 13, cx, cy - 20, SSD1306_WHITE);
  d.drawCircle(cx, cy - 22, 2, SSD1306_WHITE);
}

void drawRoverIdle(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(30, 2);
  d.print("[ STANDBY ]");
  drawRoverBody(d, 64, 36);
  if ((t / 4) % 3 == 0) d.drawCircle(64, 36, 22, SSD1306_WHITE);
  if ((t / 4) % 3 == 1) d.drawCircle(64, 36, 24, SSD1306_WHITE);
  d.setCursor(18, 56);
  d.print("SYS:OK ");
  for (int i = 0; i < 3; i++) {
    if (i == (int)(t / 3) % 3)
      d.fillCircle(88 + i * 10, 60, 2, SSD1306_WHITE);
    else
      d.drawCircle(88 + i * 10, 60, 2, SSD1306_WHITE);
  }
}

void drawRoverForward(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(24, 2);
  d.print(">> FORWARD <<");
  int offset = (t * 3) % 12;
  for (int y = offset; y < 64; y += 12) {
    d.drawFastHLine(4, y + 26, 120, SSD1306_WHITE);
  }
  drawRoverBody(d, 64, 30);
  d.fillTriangle(60, 14, 68, 14, 64, 8, SSD1306_WHITE);
  d.fillTriangle(60, 20, 68, 20, 64, 14, SSD1306_WHITE);
}

void drawRoverBackward(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(22, 2);
  d.print("<< REVERSE >>");
  int offset = 12 - (t * 3) % 12;
  for (int y = offset; y < 64; y += 12) {
    d.drawFastHLine(4, y + 26, 120, SSD1306_WHITE);
  }
  drawRoverBody(d, 64, 36);
  d.fillTriangle(60, 48, 68, 48, 64, 54, SSD1306_WHITE);
  d.fillTriangle(60, 54, 68, 54, 64, 60, SSD1306_WHITE);
}

void drawRoverTurnLeft(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(18, 2);
  d.print("<< TURN LEFT");
  int arcEnd = ((t * 8) % 90) + 10;
  for (int a = 90; a < 90 + arcEnd; a += 5) {
    float rad = a * 3.14159f / 180.0f;
    int ax = 64 + (int)(30 * cos(rad));
    int ay = 36 - (int)(30 * sin(rad));
    d.drawPixel(ax, ay, SSD1306_WHITE);
    d.drawPixel(ax - 1, ay, SSD1306_WHITE);
  }
  drawRoverBody(d, 64, 36);
  d.fillTriangle(10, 36, 20, 30, 20, 42, SSD1306_WHITE);
  d.setTextSize(1);
  d.setCursor(20, 56);
  d.print("L-WHEEL: REV");
}

void drawRoverTurnRight(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(18, 2);
  d.print("TURN RIGHT >>");
  int arcEnd = ((t * 8) % 90) + 10;
  for (int a = 90; a > 90 - arcEnd; a -= 5) {
    float rad = a * 3.14159f / 180.0f;
    int ax = 64 + (int)(30 * cos(rad));
    int ay = 36 - (int)(30 * sin(rad));
    d.drawPixel(ax, ay, SSD1306_WHITE);
    d.drawPixel(ax + 1, ay, SSD1306_WHITE);
  }
  drawRoverBody(d, 64, 36);
  d.fillTriangle(118, 36, 108, 30, 108, 42, SSD1306_WHITE);
  d.setTextSize(1);
  d.setCursor(20, 56);
  d.print("R-WHEEL: REV");
}

void drawCameraPanel(Adafruit_SSD1306& d, uint32_t t) {
  d.setTextSize(1);
  d.setTextColor(SSD1306_WHITE);
  d.setCursor(22, 2);
  d.print("[ CAMERA SYS ]");

  int cx = 64, cy = 54, r = 28;
  for (int a = 0; a <= 180; a += 3) {
    float rad = (180 - a) * 3.14159f / 180.0f;
    int px = cx + (int)(r * cos(rad));
    int py = cy - (int)(r * sin(rad));
    d.drawPixel(px, py, SSD1306_WHITE);
  }

  for (int a = 0; a <= cameraPos; a += 2) {
    float rad = (180 - a) * 3.14159f / 180.0f;
    int px = cx + (int)((r - 3) * cos(rad));
    int py = cy - (int)((r - 3) * sin(rad));
    d.drawPixel(px, py, SSD1306_WHITE);
    d.drawPixel(px, py - 1, SSD1306_WHITE);
  }

  float needleRad = (180 - cameraPos) * 3.14159f / 180.0f;
  int nx = cx + (int)((r - 6) * cos(needleRad));
  int ny = cy - (int)((r - 6) * sin(needleRad));
  d.drawLine(cx, cy, nx, ny, SSD1306_WHITE);
  d.fillCircle(cx, cy, 3, SSD1306_WHITE);

  d.setTextSize(1);
  d.setCursor(cx - 10, cy - r - 14);
  d.print(cameraPos);
  d.print((char)247);

  d.setCursor(2, 14);
  d.print("L");
  d.setCursor(114, 14);
  d.print("R");

  d.drawRect(40, 14, 48, 32, SSD1306_WHITE);
  int scanY = 15 + (t * 2) % 30;
  d.drawFastHLine(41, scanY, 46, SSD1306_WHITE);
  d.drawPixel(64, 30, SSD1306_WHITE);
  d.drawFastHLine(60, 30, 8, SSD1306_WHITE);
  d.drawFastVLine(64, 26, 8, SSD1306_WHITE);
}