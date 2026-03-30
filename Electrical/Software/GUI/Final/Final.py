"""
Mars Rover Mission Control GUI v5.1 — ENHANCED EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
★ NEW: Configurable ESP32 IP at launch — styled startup dialog
★ NEW: Keyboard shortcut overlay — press ? to toggle (semi-transparent)
★ Animated Boot Sequence with multi-stage initialization
★ Live Telemetry Charts (scrolling history for all 4 sensors)
★ Obstacle Warning System with proximity alerts & visual hazard indicators
★ Ping / Latency Display with live graph
★ Fullscreen / Windowed Mode toggle (F11 or button)
★ Enhanced Design — new color language, animated panels, glow layers
★ Battery level panel (simulated / expandable)
★ Enhanced status bar with signal strength bars
★ Instant Stop preserved from v4.1
★ Safety watchdog timer preserved from v4.1
"""

import sys
import threading
import time
import math
import random
import csv
import os
from datetime import datetime
from collections import deque

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QGraphicsDropShadowEffect, QSizePolicy, QGridLayout,
    QStackedWidget, QPushButton, QSplitter, QLineEdit, QDialog,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt, QTimer, QRect, QPointF, QRectF, pyqtSignal, QEasingCurve, QPropertyAnimation, QObject
from PyQt5.QtGui import (
    QPainter, QLinearGradient, QRadialGradient, QColor, QFont,
    QPen, QBrush, QPainterPath, QConicalGradient, QFontDatabase,
    QPolygonF, QTransform, QPalette, QPixmap
)

try:
    from websocket import create_connection
except ImportError:
    print("Install websocket-client: pip install websocket-client")
    sys.exit(1)

# ── Enhanced Color Palette v5 ──────────────────────────────────────────────────
C_BG         = QColor(2, 4, 10)
C_BG2        = QColor(5, 9, 20)
C_PANEL      = QColor(8, 14, 28, 210)
C_BORDER     = QColor(0, 200, 255, 70)
C_CYAN       = QColor(0, 230, 255)
C_CYAN_DIM   = QColor(0, 130, 170)
C_AMBER      = QColor(255, 185, 0)
C_AMBER_DIM  = QColor(150, 100, 0)
C_RED        = QColor(255, 45, 55)
C_RED_DIM    = QColor(160, 25, 30)
C_GREEN      = QColor(0, 255, 145)
C_GREEN_DIM  = QColor(0, 150, 85)
C_PURPLE     = QColor(180, 80, 255)
C_WHITE      = QColor(210, 235, 255)
C_DIM        = QColor(50, 75, 100)
C_ORANGE     = QColor(255, 130, 0)
C_TEAL       = QColor(0, 210, 190)

# Obstacle warning thresholds (cm)
OBSTACLE_WARN = 80
OBSTACLE_CRIT = 30

# Default WebSocket URL (overridden by startup dialog)
DEFAULT_ESP32_WS_URL = "ws://192.168.137.174:81"


def glow_effect(color, radius=20):
    fx = QGraphicsDropShadowEffect()
    fx.setColor(color)
    fx.setBlurRadius(radius)
    fx.setOffset(0, 0)
    return fx


def make_label(text, size=10, color=None, bold=True, align=Qt.AlignLeft):
    if color is None:
        color = C_CYAN
    lbl = QLabel(text)
    weight = QFont.Bold if bold else QFont.Normal
    lbl.setFont(QFont("Courier New", size, weight))
    lbl.setStyleSheet(f"color: {color.name()}; background: transparent;")
    lbl.setAlignment(align)
    return lbl


# ─────────────────────────────────────────────────────────────────────────────
#  STARTUP CONFIG DIALOG  (NEW in v5.1)
# ─────────────────────────────────────────────────────────────────────────────
class StartupDialog(QDialog):
    """
    Styled launch dialog for configuring the ESP32 WebSocket URL.
    Painted entirely in the same dark sci-fi aesthetic as the main GUI.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MARS ROVER — CONNECTION SETUP")
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(480, 310)

        self._tick = 0
        self._result_url = DEFAULT_ESP32_WS_URL

        # Animation timer
        self._anim = QTimer(self)
        self._anim.timeout.connect(self._step)
        self._anim.start(35)

        # ── Layout ────────────────────────────────────────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 22, 24, 22)
        outer.setSpacing(0)

        # Title row
        title_lbl = QLabel("◈  UPLINK CONFIGURATION")
        title_lbl.setFont(QFont("Courier New", 13, QFont.Bold))
        title_lbl.setStyleSheet("color: #00e6ff; background: transparent;")
        title_lbl.setAlignment(Qt.AlignCenter)
        outer.addWidget(title_lbl)

        sub_lbl = QLabel("Enter the ESP32 WebSocket address before launch")
        sub_lbl.setFont(QFont("Courier New", 8))
        sub_lbl.setStyleSheet("color: #006880; background: transparent;")
        sub_lbl.setAlignment(Qt.AlignCenter)
        outer.addWidget(sub_lbl)

        outer.addSpacing(22)

        # URL field label
        url_lbl = QLabel("WEBSOCKET URL")
        url_lbl.setFont(QFont("Courier New", 8, QFont.Bold))
        url_lbl.setStyleSheet("color: #0099b8; background: transparent; letter-spacing: 2px;")
        outer.addWidget(url_lbl)

        outer.addSpacing(6)

        # URL input
        self.url_input = QLineEdit(DEFAULT_ESP32_WS_URL)
        self.url_input.setFont(QFont("Courier New", 11, QFont.Bold))
        self.url_input.setStyleSheet("""
            QLineEdit {
                background: rgba(0, 18, 32, 210);
                color: #00e6ff;
                border: 1px solid rgba(0, 180, 255, 120);
                border-radius: 5px;
                padding: 8px 12px;
                selection-background-color: rgba(0, 180, 255, 80);
            }
            QLineEdit:focus {
                border: 1px solid rgba(0, 230, 255, 200);
                background: rgba(0, 24, 42, 220);
            }
        """)
        self.url_input.returnPressed.connect(self._accept)
        outer.addWidget(self.url_input)

        outer.addSpacing(8)

        # Hint row
        hint_lbl = QLabel("Examples:  ws://192.168.1.100:81   ·   ws://rover.local:81")
        hint_lbl.setFont(QFont("Courier New", 7))
        hint_lbl.setStyleSheet("color: rgba(0, 120, 160, 160); background: transparent;")
        hint_lbl.setAlignment(Qt.AlignCenter)
        outer.addWidget(hint_lbl)

        outer.addSpacing(26)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(14)

        self._btn_cancel = self._make_button("✕  ABORT LAUNCH", C_RED)
        self._btn_cancel.clicked.connect(self.reject)

        self._btn_connect = self._make_button("▶  INITIATE UPLINK", C_GREEN)
        self._btn_connect.clicked.connect(self._accept)

        btn_row.addWidget(self._btn_cancel)
        btn_row.addWidget(self._btn_connect)
        outer.addLayout(btn_row)

        outer.addSpacing(12)

        # Footer
        footer = QLabel("PRESS ENTER TO CONFIRM  ·  ESC TO ABORT")
        footer.setFont(QFont("Courier New", 7))
        footer.setStyleSheet("color: rgba(0,100,130,140); background: transparent;")
        footer.setAlignment(Qt.AlignCenter)
        outer.addWidget(footer)

        # Allow dragging
        self._drag_pos = None

    def _make_button(self, text, color):
        btn = QPushButton(text)
        btn.setFont(QFont("Courier New", 9, QFont.Bold))
        btn.setFixedHeight(36)
        c = color.name()
        c_dim = QColor(color.red() // 3, color.green() // 3, color.blue() // 3).name()
        btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba({color.red()},{color.green()},{color.blue()},28);
                color: {c};
                border: 1px solid rgba({color.red()},{color.green()},{color.blue()},130);
                border-radius: 5px;
                padding: 4px 16px;
            }}
            QPushButton:hover {{
                background: rgba({color.red()},{color.green()},{color.blue()},55);
                border: 1px solid rgba({color.red()},{color.green()},{color.blue()},210);
            }}
            QPushButton:pressed {{
                background: rgba({color.red()},{color.green()},{color.blue()},80);
            }}
        """)
        return btn

    def _accept(self):
        url = self.url_input.text().strip()
        if url:
            self._result_url = url
        self.accept()

    def get_url(self):
        return self._result_url

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    # Draggable frameless dialog
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Background
        bg = QLinearGradient(0, 0, w, h)
        bg.setColorAt(0.0, QColor(3, 8, 18, 242))
        bg.setColorAt(1.0, QColor(2, 5, 14, 248))
        p.setBrush(QBrush(bg))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, w, h, 10, 10)

        # Animated border glow
        pulse = 0.5 + 0.5 * math.sin(self._tick * 0.07)
        border_alpha = int(100 + 80 * pulse)
        border_g = QLinearGradient(0, 0, w, h)
        border_g.setColorAt(0.0, QColor(0, 200, 255, border_alpha))
        border_g.setColorAt(0.5, QColor(0, 100, 160, border_alpha // 2))
        border_g.setColorAt(1.0, QColor(0, 200, 255, border_alpha))
        p.setPen(QPen(QBrush(border_g), 1.4))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(0.7, 0.7, w - 1.4, h - 1.4), 10, 10)

        # Corner accents
        corner_len = 16
        p.setPen(QPen(QColor(0, 230, 255, 200), 2))
        for (cx, cy, sx, sy) in [(0, 0, 1, 1), (w, 0, -1, 1), (0, h, 1, -1), (w, h, -1, -1)]:
            p.drawLine(cx, cy, cx + sx * corner_len, cy)
            p.drawLine(cx, cy, cx, cy + sy * corner_len)

        # Subtle scan lines
        for y in range(0, h, 3):
            p.setPen(QPen(QColor(0, 0, 0, 14), 1))
            p.drawLine(0, y, w, y)

        # Top glow strip
        strip_g = QLinearGradient(0, 0, w, 0)
        strip_g.setColorAt(0, QColor(0, 0, 0, 0))
        strip_g.setColorAt(0.3, QColor(0, 180, 255, int(35 + 20 * pulse)))
        strip_g.setColorAt(0.7, QColor(0, 180, 255, int(35 + 20 * pulse)))
        strip_g.setColorAt(1, QColor(0, 0, 0, 0))
        p.fillRect(0, 0, w, 2, strip_g)

        p.end()
        super().paintEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
#  KEYBOARD SHORTCUT OVERLAY  (NEW in v5.1)
# ─────────────────────────────────────────────────────────────────────────────
class KeyboardOverlay(QWidget):
    """
    Semi-transparent fullscreen help overlay showing all key bindings.
    Toggle with the ? key. Paints over the main UI without blocking events
    when hidden.
    """

    # Columns: (category_label, [(key_label, description), ...])
    BINDINGS = [
        ("▸ MOVEMENT", [
            ("↑  Arrow Up",    "Drive Forward"),
            ("↓  Arrow Down",  "Drive Backward"),
            ("←  Arrow Left",  "Turn Left"),
            ("→  Arrow Right", "Turn Right"),
            ("(release)",      "Instant Stop"),
        ]),
        ("▸ CAMERA", [
            ("A",  "Pan Camera Right"),
            ("D",  "Pan Camera Left"),
        ]),
        ("▸ GRIPPER", [
            ("O",  "Open Gripper"),
            ("C",  "Close Gripper"),
        ]),
        ("▸ APPLICATION", [
            ("?",    "Toggle This Overlay"),
            ("ESC",  "Exit Application"),
        ]),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.visible_flag = False
        self._tick = 0
        self._fade_alpha = 0   # 0–255, animated in/out
        self._fading_in = False
        self._fading_out = False
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        self._fade_timer = QTimer(self)
        self._fade_timer.timeout.connect(self._fade_step)
        self._fade_timer.start(16)  # ~60 fps fade

    def toggle(self):
        if not self.visible_flag:
            self.visible_flag = True
            self._fading_in = True
            self._fading_out = False
            self.raise_()
            self.show()
        else:
            self._fading_in = False
            self._fading_out = True

    def _fade_step(self):
        if self._fading_in:
            self._fade_alpha = min(255, self._fade_alpha + 18)
            if self._fade_alpha >= 230:
                self._fading_in = False
            self.update()
        elif self._fading_out:
            self._fade_alpha = max(0, self._fade_alpha - 18)
            if self._fade_alpha <= 0:
                self._fading_out = False
                self.visible_flag = False
                self.hide()
            self.update()

    def paintEvent(self, event):
        if self._fade_alpha <= 0:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Full-screen dim backdrop
        p.fillRect(0, 0, w, h, QColor(1, 3, 8, int(200 * self._fade_alpha / 255)))

        # Scanlines over backdrop
        for y in range(0, h, 3):
            p.setPen(QPen(QColor(0, 0, 0, 18), 1))
            p.drawLine(0, y, w, y)

        # Central card
        card_w = min(680, w - 80)
        num_cols = len(self.BINDINGS)
        card_h = 360
        card_x = (w - card_w) // 2
        card_y = (h - card_h) // 2

        a = self._fade_alpha

        # Card background
        card_bg = QLinearGradient(card_x, card_y, card_x, card_y + card_h)
        card_bg.setColorAt(0, QColor(4, 12, 26, int(240 * a / 255)))
        card_bg.setColorAt(1, QColor(2, 7, 16, int(248 * a / 255)))
        p.setBrush(QBrush(card_bg))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(card_x, card_y, card_w, card_h, 12, 12)

        # Animated border
        t = time.time()
        pulse = 0.5 + 0.5 * math.sin(t * 2.2)
        border_alpha = int((110 + 60 * pulse) * a / 255)
        border_g = QLinearGradient(card_x, card_y, card_x + card_w, card_y + card_h)
        border_g.setColorAt(0.0, QColor(0, 210, 255, border_alpha))
        border_g.setColorAt(0.5, QColor(0, 120, 180, border_alpha // 2))
        border_g.setColorAt(1.0, QColor(0, 210, 255, border_alpha))
        p.setPen(QPen(QBrush(border_g), 1.3))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(card_x + 0.65, card_y + 0.65, card_w - 1.3, card_h - 1.3), 12, 12)

        # Corner accents
        cl = 18
        p.setPen(QPen(QColor(0, 230, 255, int(200 * a / 255)), 2))
        for (cx2, cy2, sx, sy) in [
            (card_x, card_y, 1, 1),
            (card_x + card_w, card_y, -1, 1),
            (card_x, card_y + card_h, 1, -1),
            (card_x + card_w, card_y + card_h, -1, -1),
        ]:
            p.drawLine(cx2, cy2, cx2 + sx * cl, cy2)
            p.drawLine(cx2, cy2, cx2, cy2 + sy * cl)

        # Title bar
        title_h = 44
        title_bg = QLinearGradient(card_x, card_y, card_x + card_w, card_y)
        title_bg.setColorAt(0, QColor(0, 40, 65, int(180 * a / 255)))
        title_bg.setColorAt(0.5, QColor(0, 55, 85, int(200 * a / 255)))
        title_bg.setColorAt(1, QColor(0, 40, 65, int(180 * a / 255)))
        p.setBrush(QBrush(title_bg))
        p.setPen(Qt.NoPen)
        # Clip top corners
        title_path = QPainterPath()
        title_path.addRoundedRect(QRectF(card_x, card_y, card_w, title_h + 12), 12, 12)
        title_clip = QPainterPath()
        title_clip.addRect(QRectF(card_x, card_y, card_w, title_h))
        # Simple rect for title area
        p.drawRect(card_x, card_y, card_w, title_h)

        p.setFont(QFont("Courier New", 13, QFont.Bold))
        p.setPen(QColor(0, 225, 255, int(220 * a / 255)))
        p.drawText(card_x, card_y, card_w, title_h, Qt.AlignCenter,
                   "◈  KEYBOARD  REFERENCE  ◈")

        p.setPen(QPen(QColor(0, 160, 210, int(80 * a / 255)), 1))
        p.drawLine(card_x + 20, card_y + title_h, card_x + card_w - 20, card_y + title_h)

        # Columns
        col_w = card_w // num_cols
        content_y = card_y + title_h + 14

        for col_idx, (cat_label, bindings) in enumerate(self.BINDINGS):
            col_x = card_x + col_idx * col_w + 18

            # Vertical divider (between columns)
            if col_idx > 0:
                p.setPen(QPen(QColor(0, 100, 140, int(55 * a / 255)), 1, Qt.DotLine))
                p.drawLine(card_x + col_idx * col_w, card_y + title_h + 6,
                           card_x + col_idx * col_w, card_y + card_h - 10)

            # Category header
            p.setFont(QFont("Courier New", 8, QFont.Bold))
            p.setPen(QColor(0, 190, 230, int(200 * a / 255)))
            p.drawText(col_x, content_y, col_w - 18, 18, Qt.AlignLeft, cat_label)

            # Underline
            p.setPen(QPen(QColor(0, 160, 200, int(60 * a / 255)), 1))
            p.drawLine(col_x, content_y + 17, col_x + col_w - 36, content_y + 17)

            row_y = content_y + 26
            row_h = 28

            for (key_lbl, desc) in bindings:
                # Key pill background
                key_pill_w = 98
                pill_bg = QLinearGradient(col_x, row_y, col_x, row_y + 20)
                pill_bg.setColorAt(0, QColor(0, 35, 58, int(180 * a / 255)))
                pill_bg.setColorAt(1, QColor(0, 22, 38, int(185 * a / 255)))
                p.setBrush(QBrush(pill_bg))
                p.setPen(QPen(QColor(0, 130, 180, int(90 * a / 255)), 1))
                p.drawRoundedRect(col_x, row_y, key_pill_w, 20, 4, 4)

                # Key label
                p.setFont(QFont("Courier New", 8, QFont.Bold))
                p.setPen(QColor(0, 220, 255, int(210 * a / 255)))
                p.drawText(col_x + 6, row_y, key_pill_w - 8, 20, Qt.AlignVCenter, key_lbl)

                # Description
                p.setFont(QFont("Courier New", 8))
                p.setPen(QColor(100, 175, 215, int(180 * a / 255)))
                p.drawText(col_x + key_pill_w + 8, row_y, col_w - key_pill_w - 26, 20,
                           Qt.AlignVCenter, desc)

                row_y += row_h

        # Footer hint
        p.setFont(QFont("Courier New", 8))
        p.setPen(QColor(0, 130, 170, int(140 * a / 255)))
        p.drawText(card_x, card_y + card_h - 26, card_w, 20,
                   Qt.AlignCenter, "PRESS  ?  TO DISMISS  ·  CLICK ANYWHERE TO CONTINUE")

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  BOOT SEQUENCE
# ─────────────────────────────────────────────────────────────────────────────
class BootScreen(QWidget):
    """
    Full-screen animated boot sequence.
    Emits boot_done signal when complete.
    """
    boot_done = pyqtSignal()

    STAGES = [
        (0.04, "BIOS POST ........... OK"),
        (0.08, "CPU CORE CHECK ...... OK"),
        (0.13, "MEMORY SCAN ......... OK"),
        (0.18, "STORAGE MOUNT ....... OK"),
        (0.23, "SENSOR BUS INIT ..... OK"),
        (0.29, "BMP280 TEMP/PRESS ... OK"),
        (0.35, "HC-SR04 ULTRASONIC .. OK"),
        (0.41, "SERVO DRIVERS ....... OK"),
        (0.47, "MOTOR CONTROLLER .... OK"),
        (0.53, "WEBSOCKET STACK ..... OK"),
        (0.60, "TELEMETRY ENGINE .... OK"),
        (0.67, "SAFETY WATCHDOG ..... OK"),
        (0.74, "GUI SUBSYSTEM ....... OK"),
        (0.82, "CHART ENGINE ........ OK"),
        (0.89, "OBSTACLE ALERT ...... OK"),
        (0.95, "COMMS UPLINK ........ OK"),
        (1.00, "BOOT COMPLETE \u258c"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self._lines = []
        self._tick = 0
        self._stage_idx = 0
        self._done = False
        self._fade_alpha = 255

        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)

        self._stage_timer = QTimer(self)
        self._stage_timer.timeout.connect(self._advance_stage)
        self._stage_timer.start(95)

        self._anim_timer = QTimer(self)
        self._anim_timer.timeout.connect(self._tick_anim)
        self._anim_timer.start(30)

    def _advance_stage(self):
        if self._stage_idx < len(self.STAGES):
            target_p, line = self.STAGES[self._stage_idx]
            self._progress = target_p
            self._lines.append(line)
            self._stage_idx += 1
        else:
            self._stage_timer.stop()
            self._done = True
            self._fade_timer = QTimer(self)
            self._fade_timer.timeout.connect(self._fade_out)
            self._fade_timer.start(20)

    def _fade_out(self):
        self._fade_alpha -= 15
        if self._fade_alpha <= 0:
            self._fade_alpha = 0
            self._fade_timer.stop()
            self.boot_done.emit()
        self.update()

    def _tick_anim(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        p.fillRect(0, 0, w, h, QColor(2, 4, 10))

        p.setPen(QPen(QColor(0, 80, 120, 18), 1))
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        logo_y = int(h * 0.18)

        for ring_r, ring_alpha in [(80, 20), (65, 35), (52, 55), (42, 80)]:
            grad = QRadialGradient(w // 2, logo_y, ring_r)
            grad.setColorAt(0.7, QColor(0, 200, 255, ring_alpha))
            grad.setColorAt(1.0, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.NoPen)
            p.drawEllipse(w // 2 - ring_r, logo_y - ring_r, ring_r * 2, ring_r * 2)

        for i, (r, speed, color_alpha) in enumerate([(55, 0.04, 100), (72, -0.025, 60)]):
            angle = self._tick * speed
            x1 = w // 2 + r * math.cos(angle)
            y1 = logo_y + (r * 0.3) * math.sin(angle)
            p.setBrush(QBrush(QColor(0, 220, 255, color_alpha)))
            p.setPen(Qt.NoPen)
            p.drawEllipse(int(x1) - 4, int(y1) - 4, 8, 8)

        cx2 = w // 2
        mars_grad = QRadialGradient(cx2 - 10, logo_y - 10, 32)
        mars_grad.setColorAt(0, QColor(220, 80, 40))
        mars_grad.setColorAt(0.5, QColor(180, 50, 20))
        mars_grad.setColorAt(1, QColor(100, 20, 10))
        p.setBrush(QBrush(mars_grad))
        p.setPen(QPen(QColor(255, 100, 60, 120), 1.5))
        p.drawEllipse(cx2 - 30, logo_y - 30, 60, 60)

        p.setFont(QFont("Courier New", 26, QFont.Bold))
        glow_a = int(200 + 55 * math.sin(self._tick * 0.08))
        p.setPen(QColor(0, 220, 255, glow_a))
        p.drawText(0, logo_y + 55, w, 40, Qt.AlignCenter, "MARS ROVER MISSION CONTROL")

        p.setFont(QFont("Courier New", 11))
        p.setPen(QColor(0, 140, 180, 180))
        p.drawText(0, logo_y + 90, w, 22, Qt.AlignCenter, "SYSTEM v5.1  ·  ENHANCED EDITION")

        sep_y = logo_y + 120
        sep_grad = QLinearGradient(0, sep_y, w, sep_y)
        sep_grad.setColorAt(0, QColor(0, 0, 0, 0))
        sep_grad.setColorAt(0.2, QColor(0, 180, 255, 180))
        sep_grad.setColorAt(0.8, QColor(0, 180, 255, 180))
        sep_grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.setPen(QPen(QBrush(sep_grad), 1))
        p.drawLine(0, sep_y, w, sep_y)

        log_x = int(w * 0.28)
        log_y_start = sep_y + 22
        line_h = 18
        p.setFont(QFont("Courier New", 9))
        visible = min(len(self._lines), 14)
        shown = self._lines[-visible:]
        for i, line in enumerate(shown):
            age = len(shown) - i - 1
            alpha = max(50, 220 - age * 14)
            col = QColor(0, 255, 145, alpha) if "OK" in line else QColor(0, 220, 255, alpha)
            if age == 0 and not self._done:
                blink = "_" if (self._tick // 5) % 2 == 0 else " "
                p.setPen(col)
                p.drawText(log_x, log_y_start + i * line_h, line.replace("\u258c", blink))
            else:
                p.setPen(col)
                p.drawText(log_x, log_y_start + i * line_h, line.replace("\u258c", ""))

        bar_y = int(h * 0.82)
        bar_w = int(w * 0.5)
        bar_x = (w - bar_w) // 2
        bar_h = 12

        p.setBrush(QBrush(QColor(10, 25, 45)))
        p.setPen(QPen(QColor(0, 100, 150, 80), 1))
        p.drawRoundedRect(bar_x, bar_y, bar_w, bar_h, 6, 6)

        fill_w = int(bar_w * self._progress)
        if fill_w > 0:
            fill_grad = QLinearGradient(bar_x, bar_y, bar_x + bar_w, bar_y)
            fill_grad.setColorAt(0, QColor(0, 160, 220))
            fill_grad.setColorAt(0.7, QColor(0, 220, 255))
            fill_grad.setColorAt(1, QColor(0, 255, 190))
            p.setBrush(QBrush(fill_grad))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(bar_x, bar_y, fill_w, bar_h, 6, 6)

            glow_x = bar_x + fill_w - 6
            glow_g = QRadialGradient(glow_x, bar_y + bar_h // 2, 14)
            glow_g.setColorAt(0, QColor(100, 255, 255, 160))
            glow_g.setColorAt(1, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(glow_g))
            p.drawEllipse(glow_x - 14, bar_y + bar_h // 2 - 14, 28, 28)

        p.setFont(QFont("Courier New", 9, QFont.Bold))
        p.setPen(QColor(0, 180, 220, 200))
        p.drawText(0, bar_y + 18, w, 18, Qt.AlignCenter,
                   f"INITIALIZING  {int(self._progress * 100):3d}%")

        for y in range(0, h, 3):
            p.setPen(QPen(QColor(0, 0, 0, 22), 1))
            p.drawLine(0, y, w, y)

        if self._fade_alpha < 255:
            p.fillRect(0, 0, w, h, QColor(2, 4, 10, 255 - self._fade_alpha))

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  BACKGROUND
# ─────────────────────────────────────────────────────────────────────────────
class HexGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tick = 0
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(40)

    def _step(self):
        self.tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        grad = QLinearGradient(0, 0, w, h)
        grad.setColorAt(0.0, QColor(2, 4, 10))
        grad.setColorAt(0.5, QColor(4, 8, 18))
        grad.setColorAt(1.0, QColor(2, 5, 12))
        p.fillRect(0, 0, w, h, grad)
        hex_size = 30
        hex_w = hex_size * 2
        hex_h = int(hex_size * math.sqrt(3))
        cols = w // hex_w + 3
        rows = h // hex_h + 3
        for row in range(-1, rows):
            for col in range(-1, cols):
                cx = col * hex_w * 0.75
                cy = row * hex_h + (hex_h // 2 if col % 2 else 0)
                dist = math.sqrt((cx - w / 2) ** 2 + (cy - h / 2) ** 2)
                phase = (dist * 0.014 - self.tick * 0.07) % (2 * math.pi)
                alpha = int(6 + 5 * math.sin(phase))
                alpha = max(2, min(16, alpha))
                pts = [QPointF(cx + hex_size * math.cos(math.radians(60 * i - 30)),
                               cy + hex_size * math.sin(math.radians(60 * i - 30))) for i in range(6)]
                p.setPen(QPen(QColor(0, 160, 220, alpha), 1))
                p.setBrush(Qt.NoBrush)
                p.drawPolygon(QPolygonF(pts))
        vig = QRadialGradient(w // 2, h // 2, max(w, h) * 0.7)
        vig.setColorAt(0.0, QColor(0, 0, 0, 0))
        vig.setColorAt(0.6, QColor(0, 0, 0, 0))
        vig.setColorAt(1.0, QColor(0, 0, 0, 220))
        p.fillRect(0, 0, w, h, vig)
        p.setPen(QPen(QColor(0, 0, 0, 28), 1))
        for y in range(0, h, 3):
            p.drawLine(0, y, w, y)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  GLASS PANEL
# ─────────────────────────────────────────────────────────────────────────────
class GlassPanel(QFrame):
    def __init__(self, accent=None, parent=None):
        super().__init__(parent)
        self.accent = accent if accent is not None else C_CYAN
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        r = 10
        fill = QLinearGradient(0, 0, 0, h)
        fill.setColorAt(0, QColor(6, 16, 32, 215))
        fill.setColorAt(1, QColor(3, 9, 20, 225))
        p.setBrush(QBrush(fill))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, w, h, r, r)
        a = self.accent
        border_grad = QLinearGradient(0, 0, w, h)
        border_grad.setColorAt(0, QColor(a.red(), a.green(), a.blue(), 170))
        border_grad.setColorAt(0.5, QColor(a.red(), a.green(), a.blue(), 55))
        border_grad.setColorAt(1, QColor(a.red(), a.green(), a.blue(), 170))
        p.setPen(QPen(QBrush(border_grad), 1.2))
        p.setBrush(Qt.NoBrush)
        p.drawRoundedRect(QRectF(0.6, 0.6, w - 1.2, h - 1.2), r, r)
        shine = QLinearGradient(0, 0, w, 0)
        shine.setColorAt(0, QColor(255, 255, 255, 0))
        shine.setColorAt(0.3, QColor(255, 255, 255, 16))
        shine.setColorAt(0.7, QColor(255, 255, 255, 7))
        shine.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(shine))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(1, 1, w - 2, 18), r, r)
        p.end()
        super().paintEvent(event)


# ─────────────────────────────────────────────────────────────────────────────
#  TELEMETRY CHART
# ─────────────────────────────────────────────────────────────────────────────
class TelemetryChart(QWidget):
    """Scrolling multi-line telemetry chart with neon lines and grid."""

    def __init__(self, title, unit, min_val, max_val, color, history=80, parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.color = color
        self.history = history
        self.data = deque([min_val] * history, maxlen=history)
        self._tick = 0
        self.current = min_val
        self.setMinimumSize(160, 90)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(30)

    def push(self, value):
        self.current = max(self.min_val, min(self.max_val, value))
        self.data.append(self.current)

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor(3, 7, 15, 0))

        PAD_L, PAD_R, PAD_T, PAD_B = 6, 6, 18, 22
        cw = w - PAD_L - PAD_R
        ch = h - PAD_T - PAD_B

        p.setPen(QPen(QColor(0, 80, 120, 35), 1, Qt.DotLine))
        for i in range(1, 4):
            y = PAD_T + int(ch * i // 4)
            p.drawLine(PAD_L, y, PAD_L + cw, y)
        for i in range(1, 5):
            x = PAD_L + int(cw * i // 4)
            p.drawLine(x, PAD_T, x, PAD_T + ch)

        p.setPen(QPen(QColor(self.color.red(), self.color.green(), self.color.blue(), 50), 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(PAD_L, PAD_T, cw, ch)

        data_list = list(self.data)
        n = len(data_list)
        if n < 2:
            return
        rng = self.max_val - self.min_val or 1

        def to_xy(i, val):
            x = PAD_L + int(cw * i // (n - 1))
            y = PAD_T + ch - int(ch * (val - self.min_val) / rng)
            return x, y

        path_fill = QPainterPath()
        x0, y0 = to_xy(0, data_list[0])
        path_fill.moveTo(x0, PAD_T + ch)
        path_fill.lineTo(x0, y0)
        for i in range(1, n):
            xi, yi = to_xy(i, data_list[i])
            path_fill.lineTo(xi, yi)
        last_x, _ = to_xy(n - 1, data_list[-1])
        path_fill.lineTo(last_x, PAD_T + ch)
        path_fill.closeSubpath()

        fill_g = QLinearGradient(0, PAD_T, 0, PAD_T + ch)
        c = self.color
        fill_g.setColorAt(0, QColor(c.red(), c.green(), c.blue(), 50))
        fill_g.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 5))
        p.setBrush(QBrush(fill_g))
        p.setPen(Qt.NoPen)
        p.drawPath(path_fill)

        path_line = QPainterPath()
        x0, y0 = to_xy(0, data_list[0])
        path_line.moveTo(x0, y0)
        for i in range(1, n):
            xi, yi = to_xy(i, data_list[i])
            path_line.lineTo(xi, yi)
        p.setPen(QPen(self.color, 1.8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path_line)

        lx, ly = to_xy(n - 1, data_list[-1])
        pulse = 0.5 + 0.5 * math.sin(self._tick * 0.18)
        dot_r = int(3 + 2 * pulse)
        p.setBrush(QBrush(self.color))
        p.setPen(Qt.NoPen)
        p.drawEllipse(lx - dot_r, ly - dot_r, dot_r * 2, dot_r * 2)

        p.setFont(QFont("Courier New", 7, QFont.Bold))
        p.setPen(QColor(c.red(), c.green(), c.blue(), 160))
        p.drawText(PAD_L, 2, cw, 14, Qt.AlignLeft, self.title)

        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(self.color)
        p.drawText(0, h - PAD_B + 4, w - PAD_R, 16, Qt.AlignRight, f"{self.current:.1f}{self.unit}")
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  ARC GAUGE
# ─────────────────────────────────────────────────────────────────────────────
class ArcGauge(QWidget):
    def __init__(self, title, unit, min_val, max_val,
                 color_hi=None, color_lo=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.color_hi = color_hi if color_hi is not None else C_CYAN
        self.color_lo = color_lo if color_lo is not None else self.color_hi
        self.value = min_val
        self.display_value = min_val
        self._tick = 0
        self.setMinimumSize(140, 155)
        t = QTimer(self)
        t.timeout.connect(self._animate)
        t.start(30)

    def _animate(self):
        self.display_value += (self.value - self.display_value) * 0.12
        self._tick += 1
        self.update()

    def set_value(self, v):
        self.value = max(self.min_val, min(self.max_val, v))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, int(h * 0.52)
        R = int(min(w, h) * 0.37)
        ratio = (self.display_value - self.min_val) / max(0.001, self.max_val - self.min_val)
        ratio = max(0.0, min(1.0, ratio))

        for i in range(37):
            angle = math.radians(-225 + i * (270 / 36))
            is_major = i % 9 == 0
            ro = R + 7
            ri = ro - (5 if is_major else 2.5)
            p.setPen(QPen(QColor(0, 190, 240, 190 if is_major else 70), 1.4 if is_major else 1))
            p.drawLine(int(cx + ro * math.cos(angle)), int(cy - ro * math.sin(angle)),
                       int(cx + ri * math.cos(angle)), int(cy - ri * math.sin(angle)))

        rect = QRectF(cx - R, cy - R, R * 2, R * 2)
        p.setPen(QPen(QColor(15, 35, 55), 8, Qt.SolidLine, Qt.RoundCap))
        p.setBrush(Qt.NoBrush)
        p.drawArc(rect.toRect(), int(225 * 16), int(-270 * 16))

        if ratio > 0.001:
            arc_grad = QConicalGradient(cx, cy, 225)
            arc_grad.setColorAt(0.0, self.color_lo)
            arc_grad.setColorAt(1.0, self.color_hi)
            p.setPen(QPen(QBrush(arc_grad), 8, Qt.SolidLine, Qt.RoundCap))
            p.drawArc(rect.toRect(), int(225 * 16), int(-270 * ratio) * 16)

        na = math.radians(225 - ratio * 270)
        nx = cx + (R - 13) * math.cos(na)
        ny = cy - (R - 13) * math.sin(na)
        p.setPen(QPen(QColor(255, 220, 80), 2))
        p.drawLine(cx, cy, int(nx), int(ny))

        hg = QRadialGradient(cx, cy, 7)
        hg.setColorAt(0, QColor(200, 225, 255))
        hg.setColorAt(1, QColor(25, 55, 95))
        p.setBrush(QBrush(hg))
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - 6, cy - 6, 12, 12)

        p.setFont(QFont("Courier New", 7, QFont.Bold))
        p.setPen(QColor(70, 150, 190))
        p.drawText(0, 6, w, 16, Qt.AlignCenter, self.title)

        p.setFont(QFont("Courier New", 13, QFont.Bold))
        p.setPen(self.color_hi)
        p.drawText(0, cy + R - 10, w, 26, Qt.AlignCenter, f"{self.display_value:.1f}")

        p.setFont(QFont("Courier New", 7))
        p.setPen(QColor(70, 130, 170))
        p.drawText(0, cy + R + 16, w, 16, Qt.AlignCenter, self.unit)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  SERVO ARC GAUGE
# ─────────────────────────────────────────────────────────────────────────────
class ServoArcGauge(QWidget):
    def __init__(self, title, color=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.color = color if color is not None else C_AMBER
        self._angle = 90
        self._display = 90.0
        self.setMinimumSize(160, 105)
        t = QTimer(self)
        t.timeout.connect(self._anim)
        t.start(30)

    def _anim(self):
        self._display += (self._angle - self._display) * 0.14
        self.update()

    def set_angle(self, a):
        self._angle = max(0, min(180, a))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx = w // 2
        cy = h - 16
        R = min(w // 2 - 10, h - 26)
        ratio = self._display / 180.0
        p.setPen(QPen(QColor(18, 38, 58), 7, Qt.SolidLine, Qt.RoundCap))
        p.setBrush(Qt.NoBrush)
        p.drawArc(cx - R, cy - R, R * 2, R * 2, 0 * 16, 180 * 16)
        if ratio > 0.005:
            grad = QConicalGradient(cx, cy, 0)
            c = self.color
            grad.setColorAt(0.0, QColor(c.red(), c.green(), c.blue(), 75))
            grad.setColorAt(1.0, c)
            p.setPen(QPen(QBrush(grad), 7, Qt.SolidLine, Qt.RoundCap))
            p.drawArc(cx - R, cy - R, R * 2, R * 2, 0 * 16, int(180 * ratio) * 16)
        rad = math.radians(180 - self._display)
        nx = int(cx + (R - 9) * math.cos(rad))
        ny = int(cy - (R - 9) * math.sin(rad))
        p.setPen(QPen(QColor(255, 230, 100), 2))
        p.drawLine(cx, cy, nx, ny)
        p.setBrush(QBrush(self.color))
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - 5, cy - 5, 10, 10)
        p.setFont(QFont("Courier New", 7, QFont.Bold))
        p.setPen(QColor(90, 150, 190))
        p.drawText(0, 1, w, 14, Qt.AlignCenter, self.title)
        p.setFont(QFont("Courier New", 11, QFont.Bold))
        p.setPen(self.color)
        p.drawText(0, h - 14, w, 14, Qt.AlignCenter, f"{int(self._display)}°")
        for i in range(0, 181, 45):
            r2 = math.radians(180 - i)
            tx1 = cx + (R + 2) * math.cos(r2)
            ty1 = cy - (R + 2) * math.sin(r2)
            tx2 = cx + (R + 6) * math.cos(r2)
            ty2 = cy - (R + 6) * math.sin(r2)
            p.setPen(QPen(QColor(50, 110, 150), 1))
            p.drawLine(int(tx1), int(ty1), int(tx2), int(ty2))
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  OBSTACLE WARNING WIDGET
# ─────────────────────────────────────────────────────────────────────────────
class ObstacleWarning(QWidget):
    """Proximity radar with concentric rings and hazard level indicator."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dist = 500
        self._tick = 0
        self._alert_level = 0
        self.setFixedSize(180, 180)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(40)

    def set_distance(self, d):
        self._dist = max(0, min(500, d))
        if d < OBSTACLE_CRIT:
            self._alert_level = 2
        elif d < OBSTACLE_WARN:
            self._alert_level = 1
        else:
            self._alert_level = 0
        self.update()

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2

        rings = [75, 55, 38, 22]
        ring_labels = ["500", "200", "80", "30"]
        for i, r in enumerate(rings):
            alpha = 40 + i * 15
            p.setPen(QPen(QColor(0, 160, 200, alpha), 1, Qt.DotLine))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        p.setFont(QFont("Courier New", 6))
        p.setPen(QColor(0, 120, 160, 100))
        for i, (r, lbl) in enumerate(zip(rings, ring_labels)):
            p.drawText(cx + r - 20, cy - 4, 20, 10, Qt.AlignRight, lbl)

        p.setPen(QPen(QColor(0, 100, 140, 40), 1))
        p.drawLine(cx - rings[0], cy, cx + rings[0], cy)
        p.drawLine(cx, cy - rings[0], cx, cy + rings[0])

        sweep_angle = math.radians((self._tick * 4) % 360)
        sx = cx + rings[0] * math.cos(sweep_angle)
        sy = cy - rings[0] * math.sin(sweep_angle)
        sweep_grad = QLinearGradient(cx, cy, int(sx), int(sy))
        sweep_grad.setColorAt(0, QColor(0, 220, 180, 0))
        sweep_grad.setColorAt(1, QColor(0, 220, 180, 90))
        p.setPen(QPen(QBrush(sweep_grad), 1.5))
        p.drawLine(cx, cy, int(sx), int(sy))

        max_dist = 500.0
        norm = min(self._dist / max_dist, 1.0)
        blip_r = int(rings[0] * norm)
        blip_x = cx
        blip_y = cy - blip_r

        colors = {0: C_GREEN, 1: C_AMBER, 2: C_RED}
        bc = colors[self._alert_level]

        if self._alert_level > 0:
            pulse = 0.5 + 0.5 * math.sin(self._tick * (0.2 if self._alert_level == 1 else 0.4))
            glow_r = int(10 + 6 * pulse)
            gg = QRadialGradient(blip_x, blip_y, glow_r)
            gg.setColorAt(0, QColor(bc.red(), bc.green(), bc.blue(), int(160 * pulse)))
            gg.setColorAt(1, QColor(0, 0, 0, 0))
            p.setBrush(QBrush(gg))
            p.setPen(Qt.NoPen)
            p.drawEllipse(blip_x - glow_r, blip_y - glow_r, glow_r * 2, glow_r * 2)

        p.setBrush(QBrush(bc))
        p.setPen(Qt.NoPen)
        p.drawEllipse(blip_x - 5, blip_y - 5, 10, 10)

        p.setBrush(QBrush(C_CYAN))
        p.setPen(Qt.NoPen)
        p.drawEllipse(cx - 4, cy - 4, 8, 8)

        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(QColor(0, 190, 220, 180))
        p.drawText(0, 2, w, 14, Qt.AlignCenter, "◈ PROXIMITY RADAR")

        if self._alert_level > 0:
            pulse = 0.5 + 0.5 * math.sin(self._tick * (0.18 if self._alert_level == 1 else 0.35))
            alert_alpha = int(180 + 75 * pulse)
            alert_text = "⚠  CAUTION" if self._alert_level == 1 else "⛔  OBSTACLE!"
            p.setFont(QFont("Courier New", 8, QFont.Bold))
            p.setPen(QColor(bc.red(), bc.green(), bc.blue(), alert_alpha))
            p.drawText(0, h - 16, w, 14, Qt.AlignCenter, alert_text)
        else:
            p.setFont(QFont("Courier New", 8))
            p.setPen(QColor(0, 180, 120, 130))
            p.drawText(0, h - 16, w, 14, Qt.AlignCenter, "CLEAR")

        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  PING / LATENCY WIDGET
# ─────────────────────────────────────────────────────────────────────────────
class PingDisplay(QWidget):
    """Scrolling ping latency bar chart."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pings = deque([0] * 30, maxlen=30)
        self._current = 0
        self._tick = 0
        self.setFixedHeight(70)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(30)

    def push_ping(self, ms):
        self._current = ms
        self._pings.append(ms)

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        PAD_L, PAD_T, PAD_B = 4, 18, 4
        cw = w - PAD_L * 2
        ch = h - PAD_T - PAD_B

        pings = list(self._pings)
        max_p = max(max(pings), 100)

        bar_w = cw / len(pings)
        for i, ping in enumerate(pings):
            bar_h = max(1, int(ch * ping / max_p))
            bx = PAD_L + int(i * bar_w)
            by = PAD_T + ch - bar_h
            age = len(pings) - i - 1
            alpha = max(50, 200 - age * 5)
            color_val = min(ping / 150.0, 1.0)
            r = int(0 + 255 * color_val)
            g = int(255 - 200 * color_val)
            b = int(150 - 100 * color_val)
            p.fillRect(bx, by, max(1, int(bar_w) - 1), bar_h, QColor(r, g, b, alpha))

        p.setFont(QFont("Courier New", 7, QFont.Bold))
        p.setPen(QColor(70, 150, 190, 180))
        p.drawText(PAD_L, 2, cw // 2, 14, Qt.AlignLeft, "PING")

        col = C_GREEN if self._current < 50 else (C_AMBER if self._current < 150 else C_RED)
        if self._current == 0:
            col = C_DIM
        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(col)
        val_str = f"{self._current} ms" if self._current > 0 else "-- ms"
        p.drawText(0, 2, w - PAD_L, 14, Qt.AlignRight, val_str)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  SIGNAL STRENGTH
# ─────────────────────────────────────────────────────────────────────────────
class SignalBars(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._level = 0
        self._tick = 0
        self.setFixedSize(38, 24)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(80)

    def set_level(self, lvl):
        self._level = max(0, min(5, lvl))
        self.update()

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        n = 5
        bar_w = 5
        gap = 2
        total_w = n * bar_w + (n - 1) * gap
        start_x = (w - total_w) // 2
        for i in range(n):
            bh = int((i + 1) * h / n)
            bx = start_x + i * (bar_w + gap)
            by = h - bh
            active = i < self._level
            if active:
                col = C_GREEN if self._level >= 4 else (C_AMBER if self._level >= 2 else C_RED)
                p.fillRect(bx, by, bar_w, bh, col)
            else:
                p.fillRect(bx, by, bar_w, bh, QColor(30, 50, 70))
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  D-PAD
# ─────────────────────────────────────────────────────────────────────────────
class DPadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = None
        self.setFixedSize(150, 150)

    def set_active(self, direction):
        self.active = direction
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        arm = 28
        thick = 26
        dirs = {
            'F': QRect(cx - thick // 2, cy - arm - thick, thick, arm),
            'B': QRect(cx - thick // 2, cy + arm, thick, arm),
            'L': QRect(cx - arm - thick, cy - thick // 2, arm, thick),
            'R': QRect(cx + arm, cy - thick // 2, arm, thick),
        }
        icons = {'F': '▲', 'B': '▼', 'L': '◀', 'R': '▶'}
        for key, rect in dirs.items():
            is_active = self.active == key
            if is_active:
                fill = QLinearGradient(rect.topLeft(), rect.bottomRight())
                fill.setColorAt(0, QColor(0, 225, 255, 230))
                fill.setColorAt(1, QColor(0, 145, 205, 185))
                p.setBrush(QBrush(fill))
                p.setPen(QPen(QColor(0, 255, 255), 1.5))
            else:
                p.setBrush(QBrush(QColor(12, 26, 44, 200)))
                p.setPen(QPen(QColor(0, 90, 130, 110), 1))
            p.drawRoundedRect(rect, 5, 5)
            p.setFont(QFont("Courier New", 10, QFont.Bold))
            p.setPen(QColor(0, 255, 255) if is_active else QColor(35, 90, 130))
            p.drawText(rect, Qt.AlignCenter, icons[key])
        cg = QRadialGradient(cx, cy, 20)
        cg.setColorAt(0, QColor(18, 42, 66))
        cg.setColorAt(1, QColor(8, 18, 34))
        p.setBrush(QBrush(cg))
        p.setPen(QPen(QColor(0, 90, 130, 110), 1))
        p.drawEllipse(cx - 20, cy - 20, 40, 40)
        p.setFont(QFont("Courier New", 6, QFont.Bold))
        p.setPen(QColor(35, 90, 130))
        p.drawText(cx - 20, cy - 20, 40, 40, Qt.AlignCenter, "MOVE")
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  ROVER VISUALIZER
# ─────────────────────────────────────────────────────────────────────────────
class RoverStateRenderer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = "IDLE"
        self._tick = 0
        self._wheel_rot = 0
        self.setFixedSize(190, 120)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(40)

    def set_state(self, s):
        self.state = s

    def _step(self):
        speed = {'FORWARD': 6, 'BACKWARD': 6,
                 'TURN_LEFT': 9, 'TURN_RIGHT': 9, 'IDLE': 0.5}.get(self.state, 0)
        self._wheel_rot = (self._wheel_rot + speed) % 360
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2 + 8
        STATE_COLOR = {
            'IDLE':       QColor(0, 180, 255),
            'FORWARD':    QColor(0, 255, 140),
            'BACKWARD':   QColor(255, 185, 0),
            'TURN_LEFT':  QColor(0, 225, 255),
            'TURN_RIGHT': QColor(0, 225, 255),
        }
        sc = STATE_COLOR.get(self.state, C_CYAN)
        if self.state != 'IDLE':
            for r in [48, 36, 24]:
                alpha = int(18 * (1 - r / 56))
                gg = QRadialGradient(cx, cy, r)
                gg.setColorAt(0, QColor(sc.red(), sc.green(), sc.blue(), alpha))
                gg.setColorAt(1, QColor(0, 0, 0, 0))
                p.setBrush(QBrush(gg))
                p.setPen(Qt.NoPen)
                p.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        bg = QLinearGradient(cx - 36, cy - 14, cx - 36, cy + 14)
        bg.setColorAt(0, QColor(18, 46, 75))
        bg.setColorAt(1, QColor(9, 26, 46))
        p.setBrush(QBrush(bg))
        p.setPen(QPen(sc, 1.4))
        p.drawRoundedRect(cx - 36, cy - 14, 72, 28, 5, 5)

        def draw_wheel(wx, wy):
            p.save()
            p.translate(wx, wy)
            p.rotate(self._wheel_rot if self.state in ['FORWARD', 'TURN_RIGHT'] else -self._wheel_rot)
            p.setBrush(QBrush(QColor(13, 32, 52)))
            p.setPen(QPen(sc, 1.1))
            p.drawEllipse(-8, -8, 16, 16)
            p.setPen(QPen(QColor(sc.red(), sc.green(), sc.blue(), 110), 1))
            p.drawLine(-6, 0, 6, 0)
            p.drawLine(0, -6, 0, 6)
            p.restore()

        for wx in [cx - 44, cx + 44]:
            for wy in [cy - 7, cy + 7]:
                draw_wheel(wx, wy)

        p.setPen(QPen(sc, 1.4))
        p.drawLine(cx - 9, cy - 14, cx - 9, cy - 27)
        p.setBrush(QBrush(QColor(28, 75, 125)))
        p.setPen(QPen(QColor(0, 200, 255), 1.1))
        p.drawEllipse(cx - 15, cy - 34, 11, 11)

        p.setBrush(QBrush(QColor(18, 56, 95, 175)))
        p.setPen(QPen(sc, 1))
        p.drawRect(cx + 18, cy - 20, 17, 9)
        p.drawRect(cx + 18, cy + 11, 17, 9)

        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(sc)
        p.drawText(0, h - 14, w, 14, Qt.AlignCenter, f"[ {self.state} ]")
        if self.state == 'IDLE':
            pr = 40 + 5 * math.sin(self._tick * 0.11)
            alpha = int(55 + 38 * math.sin(self._tick * 0.11))
            p.setPen(QPen(QColor(0, 180, 255, alpha), 1))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(int(cx - pr), int(cy - pr), int(pr * 2), int(pr * 2))
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  FULLSCREEN TOGGLE BUTTON
# ─────────────────────────────────────────────────────────────────────────────
class IconButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, label, accent=None, parent=None):
        super().__init__(parent)
        self._label = label
        self._accent = accent if accent is not None else C_CYAN
        self._hover = False
        self.setFixedSize(80, 28)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, e):
        self._hover = True
        self.update()

    def leaveEvent(self, e):
        self._hover = False
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        c = self._accent
        alpha = 180 if self._hover else 100
        fill = QColor(c.red(), c.green(), c.blue(), 35 if self._hover else 18)
        p.setBrush(QBrush(fill))
        p.setPen(QPen(QColor(c.red(), c.green(), c.blue(), alpha), 1))
        p.drawRoundedRect(0, 0, w, h, 5, 5)
        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(QColor(c.red(), c.green(), c.blue(), alpha + 40))
        p.drawText(0, 0, w, h, Qt.AlignCenter, self._label)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  STATUS BAR
# ─────────────────────────────────────────────────────────────────────────────
class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self._msg = "INITIALIZING UPLINK..."
        self._tick = 0
        self.signal_bars = SignalBars(self)
        self.ping_ms = 0
        self.setFixedHeight(36)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(60)

    def _step(self):
        self._tick += 1
        self.update()
        self.signal_bars.move(self.width() - 160, 6)

    def set_status(self, connected, msg, signal=0):
        self._connected = connected
        self._msg = msg
        self.signal_bars.set_level(signal)
        self.update()

    def set_ping(self, ms):
        self.ping_ms = ms
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        bg = QLinearGradient(0, 0, w, 0)
        if self._connected:
            bg.setColorAt(0, QColor(0, 28, 18, 185))
            bg.setColorAt(1, QColor(0, 18, 12, 185))
        else:
            bg.setColorAt(0, QColor(28, 8, 4, 185))
            bg.setColorAt(1, QColor(18, 4, 4, 185))
        p.fillRect(0, 0, w, h, bg)
        color = C_GREEN if self._connected else C_RED
        p.setPen(QPen(color, 1))
        p.drawLine(0, 0, w, 0)
        pulse = 0.5 + 0.5 * math.sin(self._tick * 0.18)
        dot_alpha = int(185 + 70 * pulse) if self._connected else int(115 + 75 * math.sin(self._tick * 0.28))
        p.setBrush(QBrush(QColor(color.red(), color.green(), color.blue(), dot_alpha)))
        p.setPen(Qt.NoPen)
        p.drawEllipse(14, h // 2 - 4, 9, 9)
        p.setFont(QFont("Courier New", 8, QFont.Bold))
        p.setPen(QColor(color.red(), color.green(), color.blue(), 195))
        p.drawText(32, 0, w - 200, h, Qt.AlignVCenter, self._msg)
        if self.ping_ms > 0:
            pcol = C_GREEN if self.ping_ms < 50 else (C_AMBER if self.ping_ms < 150 else C_RED)
            p.setFont(QFont("Courier New", 8, QFont.Bold))
            p.setPen(pcol)
            p.drawText(w // 2 - 40, 0, 80, h, Qt.AlignCenter | Qt.AlignVCenter,
                       f"PING {self.ping_ms}ms")
        ts = datetime.now().strftime("%H:%M:%S")
        p.setFont(QFont("Courier New", 8))
        p.setPen(QColor(45, 90, 70))
        p.drawText(0, 0, w - 200, h, Qt.AlignVCenter | Qt.AlignRight, ts)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  MISSION LOG
# ─────────────────────────────────────────────────────────────────────────────
class MissionLog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []
        self._tick = 0
        self.setMinimumHeight(85)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(80)

    def _step(self):
        self._tick += 1
        self.update()

    def append(self, text):
        ts = datetime.now().strftime("%H:%M:%S")
        self.lines.append(f"[{ts}] {text}")
        if len(self.lines) > 50:
            self.lines.pop(0)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor(2, 7, 14, 215))
        p.setPen(QPen(QColor(0, 90, 130, 55), 1))
        p.drawRect(0, 0, w - 1, h - 1)
        line_h = 15
        visible = h // line_h
        shown = self.lines[-visible:] if len(self.lines) > visible else self.lines
        p.setFont(QFont("Courier New", 7))
        for i, line in enumerate(shown):
            age = len(shown) - i - 1
            alpha = max(55, 200 - age * 25)
            if age == 0:
                blink = "_" if (self._tick // 5) % 2 == 0 else " "
                p.setPen(QColor(0, 255, 175, alpha))
                p.drawText(6, i * line_h + 11, line + blink)
            else:
                p.setPen(QColor(0, 175, 115, alpha))
                p.drawText(6, i * line_h + 11, line)
        for y in range(0, h, 3):
            p.setPen(QPen(QColor(0, 0, 0, 16), 1))
            p.drawLine(0, y, w, y)
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────
class HeaderWidget(QWidget):
    def __init__(self, ws_url="", parent=None):
        super().__init__(parent)
        self._tick = 0
        self._ws_url = ws_url
        self.setFixedHeight(68)
        t = QTimer(self)
        t.timeout.connect(self._step)
        t.start(50)

    def set_url(self, url):
        self._ws_url = url
        self.update()

    def _step(self):
        self._tick += 1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        bg = QLinearGradient(0, 0, w, 0)
        bg.setColorAt(0.0, QColor(0, 14, 28, 215))
        bg.setColorAt(0.5, QColor(0, 22, 42, 230))
        bg.setColorAt(1.0, QColor(0, 14, 28, 215))
        p.fillRect(0, 0, w, h, bg)
        for x in range(0, w, 4):
            phase = (x * 0.02 - self._tick * 0.055) % (2 * math.pi)
            alpha = int(110 + 95 * math.sin(phase))
            p.setPen(QPen(QColor(0, 185, 255, alpha), 2))
            p.drawPoint(x, h - 1)
        corner = 18
        p.setPen(QPen(QColor(0, 225, 255, 155), 2))
        for (x, y, dx, dy) in [(0, 0, 1, 1), (w, 0, -1, 1), (0, h, 1, -1), (w, h, -1, -1)]:
            p.drawLine(x, y, x + dx * corner, y)
            p.drawLine(x, y, x, y + dy * corner)
        p.setFont(QFont("Courier New", 19, QFont.Bold))
        ga = int(185 + 70 * math.sin(self._tick * 0.065))
        p.setPen(QColor(0, 225, 255, ga))
        p.drawText(0, 0, w, h - 18, Qt.AlignCenter,
                   "◈  MARS ROVER    MISSION CONTROL  v5.1  ◈")
        p.setFont(QFont("Courier New", 7))
        p.setPen(QColor(0, 115, 155, 155))
        p.drawText(0, h - 28, w, 14, Qt.AlignCenter,
                   "DRIVE · CAMERA · GRIPPER · TELEMETRY · CHARTS · OBSTACLE ALERT · INSTANT STOP")
        # Show configured URL in header
        if self._ws_url:
            p.setFont(QFont("Courier New", 7))
            p.setPen(QColor(0, 160, 120, 130))
            p.drawText(0, h - 14, w, 13, Qt.AlignCenter, f"TARGET: {self._ws_url}  ·  PRESS ? FOR KEYS")
        p.end()


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class MotorControl(QWidget):
    def __init__(self, ws_url):
        super().__init__()
        self.setWindowTitle("MARS ROVER — MISSION CONTROL v5.1")

        # Configurable URL (set from startup dialog)
        self.ESP32_WS_URL = ws_url

        # State
        self.ws = None
        self.ws_lock = threading.Lock()
        self.connecting = False
        self.camera_angle = 90
        self.gripper_angle = 10
        self.pressed_keys = set()
        self.current_state = "IDLE"
        self.last_movement_time = time.time()
        self._last_ping_time = 0
        self._ping_ms = 0

        # Stack: boot → main
        self._stack = QStackedWidget(self)
        self._boot = BootScreen()
        self._boot.boot_done.connect(self._on_boot_done)
        self._main = QWidget()
        self._main.setAttribute(Qt.WA_TranslucentBackground)

        self._stack.addWidget(self._boot)   # index 0
        self._stack.addWidget(self._main)   # index 1
        self._stack.setCurrentIndex(0)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self._stack)

        self.setStyleSheet("QWidget { background: transparent; }")
        self._build_main_ui()

        # Keyboard overlay — created after main UI, placed over everything
        self._kb_overlay = None  # initialized after showMaximized in _post_boot_init

    def _on_boot_done(self):
        self._stack.setCurrentIndex(1)
        self._post_boot_init()

    def _post_boot_init(self):
        # Create overlay now that window is shown and sized
        self._kb_overlay = KeyboardOverlay(self)
        self._kb_overlay.setGeometry(self.rect())
        self._kb_overlay.hide()

        self.connect_to_esp32()

        self.rx_timer = QTimer(self)
        self.rx_timer.timeout.connect(self.receive_data)
        self.rx_timer.start(50)

        self.sensor_timer = QTimer(self)
        self.sensor_timer.timeout.connect(lambda: self.send_command("SENSOR"))
        self.sensor_timer.start(1000)

        self.safety_timer = QTimer(self)
        self.safety_timer.timeout.connect(self.safety_check)
        self.safety_timer.start(100)

        self.ping_timer = QTimer(self)
        self.ping_timer.timeout.connect(self._do_ping)
        self.ping_timer.start(2000)

        self.log.append("SYSTEM BOOT — MARS ROVER MISSION CONTROL v5.1")
        self.log.append(f"TARGET: {self.ESP32_WS_URL}")
        self.log.append("LIVE TELEMETRY CHARTS ACTIVE")
        self.log.append("PROXIMITY RADAR ACTIVE — WARN@80cm / CRIT@30cm")
        self.log.append("INSTANT STOP ON KEY RELEASE — SAFETY WATCHDOG ON")
        self.log.append("PRESS ? FOR KEYBOARD SHORTCUT REFERENCE")

    # ── UI Construction ──────────────────────────────────────────────────────
    def _build_main_ui(self):
        self._main.setLayout(QVBoxLayout())
        self._main.layout().setContentsMargins(0, 0, 0, 0)

        container = QWidget(self._main)
        self._main.layout().addWidget(container)

        self.bg = HexGrid(container)
        self.bg.setGeometry(0, 0, container.width(), container.height())

        self._overlay = container
        root = QVBoxLayout(container)
        root.setContentsMargins(14, 10, 14, 10)
        root.setSpacing(8)

        # Header (shows configured URL)
        self.header = HeaderWidget(ws_url=self.ESP32_WS_URL)
        root.addWidget(self.header)

        # ── Row 1: Gauges + Charts ────────────────────────────────────────────
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        gauge_panel = GlassPanel(C_CYAN)
        gauge_layout = QHBoxLayout(gauge_panel)
        gauge_layout.setContentsMargins(16, 8, 16, 8)
        gauge_layout.setSpacing(14)

        self.temp_gauge  = ArcGauge("TEMPERATURE", "°C",  -10, 60,   QColor(0, 205, 255),  QColor(0, 100, 200))
        self.press_gauge = ArcGauge("PRESSURE",    "hPa", 950, 1060, QColor(0, 255, 140),  QColor(0, 180, 80))
        self.alt_gauge   = ArcGauge("ALTITUDE",    "m",   0,   500,  QColor(255, 200, 0),  QColor(175, 115, 0))
        self.dist_gauge  = ArcGauge("DISTANCE",    "cm",  0,   500,  QColor(255, 55, 75),  QColor(175, 28, 38))
        for g in [self.temp_gauge, self.press_gauge, self.alt_gauge, self.dist_gauge]:
            gauge_layout.addWidget(g)
        top_row.addWidget(gauge_panel, 2)

        chart_panel = GlassPanel(C_TEAL)
        chart_grid = QGridLayout(chart_panel)
        chart_grid.setContentsMargins(10, 8, 10, 8)
        chart_grid.setSpacing(6)
        chart_lbl = make_label("◈  LIVE TELEMETRY CHARTS", 8, C_TEAL, align=Qt.AlignCenter)
        chart_grid.addWidget(chart_lbl, 0, 0, 1, 2)

        self.temp_chart  = TelemetryChart("TEMP",  "°C",  -10, 60,   QColor(0, 205, 255))
        self.press_chart = TelemetryChart("PRESS", "hPa", 950, 1060, QColor(0, 255, 140))
        self.alt_chart   = TelemetryChart("ALT",   "m",   0,   500,  QColor(255, 200, 0))
        self.dist_chart  = TelemetryChart("DIST",  "cm",  0,   500,  QColor(255, 55, 75))

        chart_grid.addWidget(self.temp_chart, 1, 0)
        chart_grid.addWidget(self.press_chart, 1, 1)
        chart_grid.addWidget(self.alt_chart, 2, 0)
        chart_grid.addWidget(self.dist_chart, 2, 1)
        top_row.addWidget(chart_panel, 1)

        root.addLayout(top_row)

        # ── Row 2: Controls ───────────────────────────────────────────────────
        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(10)

        cam_panel = GlassPanel(C_AMBER)
        cam_panel.setFixedWidth(200)
        cam_l = QVBoxLayout(cam_panel)
        cam_l.setContentsMargins(10, 7, 10, 7)
        cam_l.addWidget(make_label("◈  CAMERA PAN", 8, C_AMBER, align=Qt.AlignCenter))
        self.camera_gauge = ServoArcGauge("PAN ANGLE", C_AMBER)
        cam_l.addWidget(self.camera_gauge)
        cam_l.addWidget(make_label("  ← A    D →", 7, C_AMBER_DIM, align=Qt.AlignCenter))
        ctrl_row.addWidget(cam_panel)

        grip_panel = GlassPanel(C_GREEN)
        grip_panel.setFixedWidth(200)
        grip_l = QVBoxLayout(grip_panel)
        grip_l.setContentsMargins(10, 7, 10, 7)
        grip_l.addWidget(make_label("◈  GRIPPER", 8, C_GREEN, align=Qt.AlignCenter))
        self.gripper_gauge = ServoArcGauge("POSITION", C_GREEN)
        self.gripper_gauge.set_angle(10)
        grip_l.addWidget(self.gripper_gauge)
        grip_l.addWidget(make_label("  O→ Open  C→ Close", 7, C_GREEN_DIM, align=Qt.AlignCenter))
        ctrl_row.addWidget(grip_panel)

        rover_panel = GlassPanel(C_CYAN)
        rover_l = QVBoxLayout(rover_panel)
        rover_l.setContentsMargins(14, 7, 14, 7)
        rover_l.setAlignment(Qt.AlignCenter)
        rover_l.addWidget(make_label("◈  ROVER STATE", 8, C_CYAN, align=Qt.AlignCenter))
        rover_inner = QHBoxLayout()
        rover_inner.setSpacing(16)
        self.rover_viz = RoverStateRenderer()
        rover_inner.addWidget(self.rover_viz, alignment=Qt.AlignCenter)
        self.dpad = DPadWidget()
        rover_inner.addWidget(self.dpad, alignment=Qt.AlignCenter)
        rover_l.addLayout(rover_inner)
        ctrl_row.addWidget(rover_panel, 1)

        obs_panel = GlassPanel(C_RED)
        obs_panel.setFixedWidth(200)
        obs_l = QVBoxLayout(obs_panel)
        obs_l.setContentsMargins(10, 7, 10, 7)
        obs_l.setAlignment(Qt.AlignCenter)
        self.obstacle_widget = ObstacleWarning()
        obs_l.addWidget(self.obstacle_widget, alignment=Qt.AlignCenter)
        ctrl_row.addWidget(obs_panel)

        root.addLayout(ctrl_row)

        # ── Row 3: Bottom bar ─────────────────────────────────────────────────
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)

        legend_panel = GlassPanel(C_DIM)
        legend_panel.setFixedWidth(190)
        leg_l = QVBoxLayout(legend_panel)
        leg_l.setContentsMargins(12, 8, 12, 8)
        leg_l.addWidget(make_label("◈  KEY BINDINGS", 7, C_DIM, align=Qt.AlignCenter))
        for line in ["↑↓←→   Drive", "A / D    Camera",
                     "O / C    Gripper", "?        Key overlay",
                     "STOP ON KEY RELEASE"]:
            leg_l.addWidget(make_label(line, 7, QColor(55, 110, 155), bold=False))

        ping_panel = GlassPanel(C_PURPLE)
        ping_panel.setFixedWidth(190)
        ping_l = QVBoxLayout(ping_panel)
        ping_l.setContentsMargins(10, 7, 10, 7)
        ping_l.addWidget(make_label("◈  LATENCY", 7, C_PURPLE, align=Qt.AlignCenter))
        self.ping_display = PingDisplay()
        ping_l.addWidget(self.ping_display)

        bottom_row.addWidget(legend_panel)
        bottom_row.addWidget(ping_panel)

        log_panel = GlassPanel(QColor(0, 135, 95))
        log_l = QVBoxLayout(log_panel)
        log_l.setContentsMargins(0, 4, 0, 0)
        log_l.addWidget(make_label("◈  MISSION LOG", 7, C_GREEN, align=Qt.AlignCenter))
        self.log = MissionLog()
        log_l.addWidget(self.log)
        bottom_row.addWidget(log_panel, 1)

        root.addLayout(bottom_row)

        # Status bar
        self.status_bar = StatusBar()
        root.addWidget(self.status_bar)

    # ── Resize: keep background and overlay in sync ───────────────────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._stack.currentIndex() == 1:
            w = self._overlay.width()
            h = self._overlay.height()
            self.bg.setGeometry(0, 0, w, h)
        # Keep keyboard overlay filling the window
        if self._kb_overlay is not None:
            self._kb_overlay.setGeometry(self.rect())

    # ── WebSocket ─────────────────────────────────────────────────────────────
    def connect_to_esp32(self):
        if self.connecting:
            return
        self.connecting = True
        self.log.append(f"ATTEMPTING UPLINK → {self.ESP32_WS_URL}")

        def _connect():
            while True:
                try:
                    ws = create_connection(self.ESP32_WS_URL, timeout=5)
                    with self.ws_lock:
                        self.ws = ws
                    self.status_bar.set_status(True, f"UPLINK OK  ·  {self.ESP32_WS_URL}", signal=4)
                    self.log.append("UPLINK ESTABLISHED — TELEMETRY ACTIVE")
                    self.connecting = False
                    break
                except Exception as e:
                    self.log.append(f"LINK FAILED: {str(e)[:50]}")
                    self.status_bar.set_status(False, f"RETRYING... ({str(e)[:30]})", signal=0)
                    time.sleep(2)

        threading.Thread(target=_connect, daemon=True).start()

    def send_command(self, cmd, urgent=False):
        if urgent:
            self._send_immediate(cmd)
        else:
            self._send_async(cmd)

    def _send_immediate(self, cmd):
        with self.ws_lock:
            ws = self.ws
        if ws is None:
            self.connect_to_esp32()
            return
        try:
            ws.send(cmd)
            if cmd == "S":
                self.log.append("🛑 INSTANT STOP sent")
        except Exception as e:
            with self.ws_lock:
                self.ws = None
            self.log.append(f"LINK ERROR: {str(e)[:40]}")
            self.connect_to_esp32()

    def _send_async(self, cmd):
        def _send():
            with self.ws_lock:
                ws = self.ws
            if ws is None:
                self.connect_to_esp32()
                return
            try:
                ws.send(cmd)
                if cmd in ["F", "B", "L", "R"]:
                    self.last_movement_time = time.time()
            except Exception as e:
                with self.ws_lock:
                    self.ws = None
                self.log.append(f"LINK ERROR: {str(e)[:40]}")
                self.connect_to_esp32()

        threading.Thread(target=_send, daemon=True).start()

    def _do_ping(self):
        def _ping():
            with self.ws_lock:
                ws = self.ws
            if ws is None:
                self.ping_display.push_ping(0)
                return
            try:
                t0 = time.time()
                ws.send("PING")
                ms = int((time.time() - t0) * 1000)
                self._ping_ms = ms
                self.ping_display.push_ping(ms)
                self.status_bar.set_ping(ms)
            except Exception:
                self.ping_display.push_ping(0)

        threading.Thread(target=_ping, daemon=True).start()

    def receive_data(self):
        import select
        with self.ws_lock:
            ws = self.ws
        if ws is None:
            return
        try:
            rlist, _, _ = select.select([ws.sock], [], [], 0)
            if rlist:
                msg = ws.recv().strip()
                if ',' in msg and len(msg.split(',')) == 4:
                    try:
                        t, pr, al, d = [float(x) for x in msg.split(',')]
                        self.temp_gauge.set_value(t)
                        self.press_gauge.set_value(pr)
                        self.alt_gauge.set_value(al)
                        self.dist_gauge.set_value(d)
                        self.temp_chart.push(t)
                        self.press_chart.push(pr)
                        self.alt_chart.push(al)
                        self.dist_chart.push(d)
                        self.obstacle_widget.set_distance(d)
                        if d < OBSTACLE_CRIT:
                            self.log.append(f"⛔ OBSTACLE CRITICAL {d:.0f}cm")
                        elif d < OBSTACLE_WARN:
                            self.log.append(f"⚠ OBSTACLE WARNING {d:.0f}cm")
                    except ValueError:
                        pass
                elif msg.isdigit():
                    self.camera_angle = int(msg)
                    self.camera_gauge.set_angle(self.camera_angle)
                elif msg.startswith("GRIPPER_ANGLE"):
                    self.gripper_gauge.set_angle(int(msg.split()[1]))
                elif msg == "GRIPPER_OPEN":
                    self.gripper_gauge.set_angle(90)
                elif msg == "GRIPPER_CLOSE":
                    self.gripper_gauge.set_angle(10)
        except Exception as e:
            with self.ws_lock:
                self.ws = None
            self.log.append(f"RX ERROR: {str(e)[:40]}")
            self.connect_to_esp32()

    # ── Safety ────────────────────────────────────────────────────────────────
    def safety_check(self):
        if self.current_state != "IDLE":
            if time.time() - self.last_movement_time > 3.0:
                self._send_immediate("S")
                self.current_state = "IDLE"
                self.rover_viz.set_state("IDLE")
                self.dpad.set_active(None)
                self.log.append("⚠️ SAFETY AUTO-STOP triggered")
        if not self.pressed_keys and self.current_state != "IDLE":
            self._send_immediate("S")
            self.current_state = "IDLE"
            self.rover_viz.set_state("IDLE")
            self.dpad.set_active(None)

    # ── Key Controls ──────────────────────────────────────────────────────────
    def update_rover_state(self):
        movement_keys = {Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right}
        active = self.pressed_keys & movement_keys
        if not active:
            return
        if Qt.Key_Up in active:
            self.send_command("F"); self.current_state = "FORWARD"
            self.rover_viz.set_state("FORWARD"); self.dpad.set_active("F")
        elif Qt.Key_Down in active:
            self.send_command("B"); self.current_state = "BACKWARD"
            self.rover_viz.set_state("BACKWARD"); self.dpad.set_active("B")
        elif Qt.Key_Left in active:
            self.send_command("L"); self.current_state = "TURN_LEFT"
            self.rover_viz.set_state("TURN_LEFT"); self.dpad.set_active("L")
        elif Qt.Key_Right in active:
            self.send_command("R"); self.current_state = "TURN_RIGHT"
            self.rover_viz.set_state("TURN_RIGHT"); self.dpad.set_active("R")

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()

        # Keyboard overlay toggle — ? key (Slash + Shift or dedicated Key_Question)
        if key in (Qt.Key_Question, Qt.Key_Slash) or \
           (key == Qt.Key_Slash and event.modifiers() & Qt.ShiftModifier):
            if self._kb_overlay is not None:
                self._kb_overlay.toggle()
                if self._kb_overlay.visible_flag:
                    self.log.append("◈ KEYBOARD REFERENCE OPENED  (? to close)")
                else:
                    self.log.append("◈ KEYBOARD REFERENCE CLOSED")
            return

        if key in self.pressed_keys:
            return
        self.pressed_keys.add(key)
        if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            self.update_rover_state()
        elif key == Qt.Key_A:
            self.send_command("D"); self.log.append("CAMERA → RIGHT")
        elif key == Qt.Key_D:
            self.send_command("A"); self.log.append("CAMERA ← LEFT")
        elif key == Qt.Key_O:
            self.send_command("O"); self.log.append("GRIPPER → OPENING")
        elif key == Qt.Key_C:
            self.send_command("C"); self.log.append("GRIPPER → CLOSING")

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key not in self.pressed_keys:
            return
        self.pressed_keys.remove(key)
        if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            self._send_immediate("S")
            self.current_state = "IDLE"
            self.rover_viz.set_state("IDLE")
            self.dpad.set_active(None)
            self.log.append("🛑 INSTANT STOP (key released)")
            self.update_rover_state()

    def closeEvent(self, event):
        self._send_immediate("S")
        time.sleep(0.1)
        with self.ws_lock:
            if self.ws:
                try:
                    self.ws.close()
                except Exception:
                    pass
        event.accept()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(2, 4, 10))
    pal.setColor(QPalette.WindowText, QColor(185, 225, 255))
    pal.setColor(QPalette.Base, QColor(5, 9, 20))
    pal.setColor(QPalette.Text, QColor(185, 225, 255))
    app.setPalette(pal)
    app.setFont(QFont("Courier New", 9))

    # ── Launch startup dialog ─────────────────────────────────────────────────
    dlg = StartupDialog()
    dlg.move(
        app.primaryScreen().geometry().center().x() - dlg.width() // 2,
        app.primaryScreen().geometry().center().y() - dlg.height() // 2,
    )
    result = dlg.exec_()

    if result != QDialog.Accepted:
        # User aborted — exit cleanly
        sys.exit(0)

    configured_url = dlg.get_url()

    # ── Launch main window ────────────────────────────────────────────────────
    window = MotorControl(ws_url=configured_url)
    window.showMaximized()
    sys.exit(app.exec_())