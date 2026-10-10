# -*- coding: utf-8 -*-
"""
draw_circuits.py - generates the 20 wiring diagrams (Q01..Q20) for the
Digital Electronics practicals (Arduino UNO R3, Tinkercad Circuits).

Binding spec: PIN_MAP.md (same folder).  Output:
    Digital_Electronics_Practicals/circuits/<stem>.png

Structure
  1. geometry constants / lanes
  2. reusable part-drawing classes (Arduino UNO, LED, resistor, push button,
     RGB LED, potentiometer, piezo buzzer, HC-SR04, PIR, TMP36, LCD 16x2)
  3. layout functions (one per shared wiring) = per-question data table
  4. renderer (wires, junction dots, connections table)
  5. self-check (pins exist, one net per Arduino pin, netlist == PIN_MAP,
     no overlapping wires, no wire through a body / text, no overlapping text)

Run:  python draw_circuits.py
"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, FancyBboxPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "Digital_Electronics_Practicals", "circuits")
if os.name == "nt" and not OUT_DIR.startswith("\\\\"):
    OUT_DIR = "\\\\?\\" + OUT_DIR      # the workspace path can exceed MAX_PATH

# --------------------------------------------------------------------------
# 1. geometry (1 unit = 0.1 inch)
# --------------------------------------------------------------------------
W, H = 170.0, 104.0
DPI = 200                      # 17 in x 200 dpi = 3400 px wide
Y_LEG = 78.0                   # y where every component leg ends
Y_RB = 68.0                    # bottom lead of an in-line resistor
Y_5V = 65.0                    # 5V rail
Y_GND = 62.0                   # GND rail
TOP_Y = 41.0                   # digital header pin holes
BOT_Y = 14.0                   # power / analog header pin holes
BX0, BX1, BY0, BY1 = 10.0, 102.0, 13.0, 42.0   # Arduino board outline
TABLE_X0, TABLE_X1 = 116.0, 168.0


def TL(i):                     # routing lanes above the board
    return 59.0 - 2.0 * i


def BL(i):                     # routing lanes below the board
    return 10.0 - 2.0 * i


COL = {
    "red": "#e3120b", "black": "#111111", "orange": "#ff7f0e",
    "blue": "#1f6fd1", "green": "#22a034", "purple": "#8e44ad",
    "yellow": "#d9a400", "cyan": "#12b5c9", "brown": "#8c564b",
    "pink": "#e754b3",
}
METAL = "#8a8a8a"
FS = 9.0


def T(ax, x, y, s, **kw):
    kw.setdefault("fontsize", FS)
    kw.setdefault("ha", "center")
    kw.setdefault("va", "center")
    kw.setdefault("zorder", 8)
    kw.setdefault("color", "#111111")
    return ax.text(x, y, s, **kw)


# --------------------------------------------------------------------------
# 2. parts
# --------------------------------------------------------------------------
class Part:
    def __init__(self, name):
        self.name = name
        self.pins = {}       # pin -> (x, y) wire attachment point
        self.plabel = {}     # pin -> text used in the Connections table
        self.bodies = []     # (x0, y0, x1, y1) rectangles wires must avoid
        self.legs = []       # (x0, y0, x1, y1) leg bounding boxes
        self.attach = None   # resistors: 'PART.pin' the top lead touches

    def leg(self, ax, pts, color=METAL, lw=2.4):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt",
                solid_joinstyle="round", zorder=3)
        self.legs.append((min(xs), min(ys), max(xs), max(ys)))


class Arduino(Part):
    TOP = [("SCL", 26), ("SDA", 30), ("AREF", 34), ("GND1", 38), ("D13", 42),
           ("D12", 46), ("D11", 50), ("D10", 54), ("D9", 58), ("D8", 62),
           ("D7", 68), ("D6", 72), ("D5", 76), ("D4", 80), ("D3", 84),
           ("D2", 88), ("D1", 92), ("D0", 96)]
    BOT = [("IOREF", 44), ("RESET", 48), ("3V3", 52), ("5V", 56),
           ("GND2", 60), ("GND3", 64), ("VIN", 68), ("A0", 76), ("A1", 80),
           ("A2", 84), ("A3", 88), ("A4", 92), ("A5", 96)]
    SHOW = {"GND1": "GND", "GND2": "GND", "GND3": "GND", "3V3": "3.3V",
            "VIN": "Vin", "D11": "D11~", "D10": "D10~", "D9": "D9~",
            "D6": "D6~", "D5": "D5~", "D3": "D3~", "D1": "D1 TX",
            "D0": "D0 RX"}

    def __init__(self):
        super().__init__("UNO")
        for n, x in self.TOP:
            self.pins[n] = (float(x), TOP_Y)
        for n, x in self.BOT:
            self.pins[n] = (float(x), BOT_Y)
        for n in self.pins:
            self.plabel[n] = "Arduino " + canon(n)
        self.bodies = [(BX0, BY0 + 2.2, BX1, BY1 - 2.2)]

    def draw(self, ax, used=()):
        ax.add_patch(FancyBboxPatch((BX0, BY0), BX1 - BX0, BY1 - BY0,
                                    boxstyle="round,pad=0,rounding_size=1.5",
                                    fc="#00878f", ec="#004d52", lw=2, zorder=1))
        # USB socket, barrel jack, MCU, reset button
        ax.add_patch(Rectangle((BX0, 31), 9, 7, fc="#c9c9c9", ec="#555", lw=1.2, zorder=2))
        T(ax, BX0 + 4.5, 34.5, "USB", fontsize=8, color="#333")
        ax.add_patch(Rectangle((BX0, 16.5), 9, 7, fc="#1c1c1c", ec="#000", lw=1.2, zorder=2))
        T(ax, BX0 + 4.5, 20, "DC", fontsize=8, color="#ddd")
        ax.add_patch(Rectangle((58, 24.2), 30, 4.2, fc="#1c1c1c", ec="#000", lw=1, zorder=2))
        T(ax, 73, 26.3, "ATmega328P", fontsize=8, color="#cfcfcf")
        ax.add_patch(Circle((22.5, 36.5), 1.3, fc="#d32f2f", ec="#333", lw=1, zorder=2))
        T(ax, 38, 27.6, "ARDUINO UNO R3", fontsize=13, color="white", weight="bold")
        T(ax, 61, 32.2, "DIGITAL  (PWM ~)", fontsize=8, color="#d9f3f5")
        T(ax, 54, 22.4, "POWER", fontsize=8, color="#d9f3f5")
        T(ax, 86, 22.4, "ANALOG IN", fontsize=8, color="#d9f3f5")
        # header strips
        for x0, x1, y0 in ((24, 64, BY1 - 2), (66, 98, BY1 - 2),
                           (42, 70, BY0), (74, 98, BY0)):
            ax.add_patch(Rectangle((x0, y0), x1 - x0, 2, fc="#1a1a1a", ec="#000", lw=0.8, zorder=2))
        for n, (x, y) in self.pins.items():
            hot = n in used
            s = 1.5 if hot else 1.0
            ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s,
                                   fc="#ffe600" if hot else "#9e9e9e",
                                   ec="#000", lw=0.8, zorder=3))
            top = y == TOP_Y
            kw = dict(rotation=90, ha="center", va="top" if top else "bottom",
                      fontsize=8.5)
            ty = BY1 - 2.9 if top else BY0 + 2.9
            if hot:
                T(ax, x, ty, self.SHOW.get(n, n), color="#000", weight="bold",
                  bbox=dict(boxstyle="round,pad=0.18", fc="#ffe600", ec="#000", lw=0.8), **kw)
            else:
                T(ax, x, ty, self.SHOW.get(n, n), color="white", **kw)


def canon(pin):
    return {"GND1": "GND", "GND2": "GND", "GND3": "GND",
            "3V3": "3.3V", "VIN": "Vin"}.get(pin, pin)


class LED(Part):
    FILL = {"red": "#e53935", "green": "#43a047", "yellow": "#fdd835"}

    def __init__(self, name, xc, xa, color="red", prefix="LED"):
        super().__init__(name)
        self.xc, self.xa, self.color, self.prefix = float(xc), float(xa), color, prefix
        self.pins = {"anode": (self.xa, Y_LEG), "cathode": (self.xc, Y_LEG)}
        self.plabel = {"anode": prefix + " anode (+)", "cathode": prefix + " cathode (−)"}
        cx = (self.xa + self.xc) / 2
        self.bodies = [(cx - 4.1, 82, cx + 4.1, 91)]

    def draw(self, ax):
        cx = (self.xa + self.xc) / 2
        f = self.FILL[self.color]
        sa = 1 if self.xa > cx else -1
        # anode = long leg, drawn with the Tinkercad-style kink
        self.leg(ax, [(self.xa - sa * 0.8, 82), (self.xa - sa * 0.8, 80.9),
                      (self.xa, 80.1), (self.xa, Y_LEG)])
        self.leg(ax, [(self.xc, 82), (self.xc, Y_LEG)])
        ax.add_patch(Rectangle((cx - 4.1, 82), 8.2, 1.2, fc=f, ec="#333", lw=1.2, zorder=4))
        ax.add_patch(Rectangle((cx - 3.4, 83.2), 6.8, 4.3, fc=f, ec="none", zorder=4))
        ax.add_patch(Wedge((cx, 87.5), 3.4, 0, 180, fc=f, ec="none", zorder=4))
        ax.plot([cx - 3.4, cx - 3.4], [83.2, 87.5], color="#333", lw=1.2, zorder=5)
        ax.plot([cx + 3.4, cx + 3.4], [83.2, 87.5], color="#333", lw=1.2, zorder=5)
        ax.add_patch(Wedge((cx, 87.5), 3.4, 0, 180, fc="none", ec="#333", lw=1.2, zorder=5))
        ax.add_patch(Wedge((cx - 1.0, 88.0), 1.4, 100, 170, width=0.35, fc="white", ec="none", alpha=.8, zorder=5))
        T(ax, cx, 93.0, "%s (%s)" % ("LED", self.color), fontsize=10.5, weight="bold")
        T(ax, self.xa + sa * 1.9, 86.4, "anode (+)\nlong leg",
          ha="left" if sa > 0 else "right", color="#b00000")
        T(ax, self.xc - sa * 1.9, 86.4, "cathode (−)\nshort leg",
          ha="right" if sa > 0 else "left")


class Resistor(Part):
    def __init__(self, name, x, attach, value="220 Ω", label="right"):
        super().__init__(name)
        self.x, self.value, self.label_side = float(x), value, label
        self.attach = attach
        self.pins = {"a": (self.x, Y_LEG), "b": (self.x, Y_RB)}
        self.bodies = [(self.x - 1.1, 70, self.x + 1.1, 76)]

    def draw(self, ax):
        x = self.x
        self.leg(ax, [(x, Y_LEG), (x, 76)])
        self.leg(ax, [(x, 70), (x, Y_RB)])
        ax.add_patch(FancyBboxPatch((x - 1.1, 70), 2.2, 6,
                                    boxstyle="round,pad=0,rounding_size=0.5",
                                    fc="#e8d3a2", ec="#6d4c41", lw=1.2, zorder=4))
        for yb, c in ((74.6, "#d32f2f"), (73.5, "#d32f2f"), (72.4, "#6d4c41"), (70.8, "#c9a227")):
            ax.add_patch(Rectangle((x - 1.1, yb), 2.2, 0.55, fc=c, ec="none", zorder=5))
        if self.label_side == "right":
            T(ax, x + 1.7, 73, self.value, ha="left", weight="bold")
        elif self.label_side == "left":
            T(ax, x - 1.7, 73, self.value, ha="right", weight="bold")
        else:   # rotated, hugging the right side (tight pin pitch)
            T(ax, x + 2.15, 73, self.value, rotation=90, weight="bold", fontsize=8.5)


class Button(Part):
    """4-leg tactile push button, top view. 1a/2a = lower legs, 1b/2b = upper."""

    def __init__(self, name, x1a):
        super().__init__(name)
        self.xl = float(x1a) - 1.5
        xl = self.xl
        self.pins = {"T1a": (xl + 1.5, Y_LEG), "T2b": (xl + 11.5, 92.0)}
        self.unused = {"T2a": (xl + 6.5, 79.6), "T1b": (xl + 1.5, 92.0)}
        self.plabel = {"T1a": "Button terminal 1a", "T2b": "Button terminal 2b"}
        self.bodies = [(xl, 82, xl + 8, 90)]

    def draw(self, ax):
        xl = self.xl
        self.leg(ax, [(xl + 1.5, 82), (xl + 1.5, Y_LEG)])
        self.leg(ax, [(xl + 6.5, 82), (xl + 6.5, 79.6)])
        self.leg(ax, [(xl + 1.5, 90), (xl + 1.5, 92)])
        self.leg(ax, [(xl + 6.5, 90), (xl + 6.5, 92), (xl + 11.5, 92)])
        ax.add_patch(FancyBboxPatch((xl, 82), 8, 8, boxstyle="round,pad=0,rounding_size=0.8",
                                    fc="#3a3a3a", ec="#000", lw=1.2, zorder=4))
        ax.add_patch(Circle((xl + 4, 86), 2.5, fc="#c62828", ec="#000", lw=1.2, zorder=5))
        T(ax, xl + 0.6, 79.9, "1a", ha="right", weight="bold")
        T(ax, xl + 7.4, 80.4, "2a", ha="left", color="#666")
        T(ax, xl + 0.6, 91.6, "1b", ha="right", color="#666")
        T(ax, xl + 9.3, 93.3, "2b", weight="bold")
        T(ax, xl + 4, 96.3, "Push button", fontsize=10.5, weight="bold")


class RGBLed(Part):
    """Common-cathode RGB LED, Tinkercad leg order: Red, Cathode, Blue, Green."""
    P = 8.0

    def __init__(self, name, x0):
        super().__init__(name)
        self.x0 = float(x0)
        xs = [self.x0 + i * self.P for i in range(4)]
        self.pins = dict(zip(("R", "C", "B", "G"), [(x, Y_LEG) for x in xs]))
        self.plabel = {"R": "RGB Red leg", "C": "RGB Cathode (−)",
                       "B": "RGB Blue leg", "G": "RGB Green leg"}
        cx = self.x0 + 1.5 * self.P
        self.cx = cx
        self.bodies = [(cx - 5.2, 86, cx + 5.2, 94.6)]

    def draw(self, ax):
        cx = self.cx
        for i, (k, lab) in enumerate((("R", "Red"), ("C", "Cathode\n(−)"),
                                      ("B", "Blue"), ("G", "Green"))):
            x = self.pins[k][0]
            bx = cx - 3 + 2 * i
            self.leg(ax, [(bx, 86), (x, 82.6), (x, Y_LEG)])
            T(ax, x + 0.8, 80.3, lab, ha="left", weight="bold")
        ax.add_patch(Rectangle((cx - 5.2, 86), 10.4, 1.1, fc="#ececec", ec="#333", lw=1.2, zorder=4))
        ax.add_patch(Rectangle((cx - 4.5, 87.1), 9, 3, fc="#f4f4f4", ec="none", zorder=4))
        ax.add_patch(Wedge((cx, 90.1), 4.5, 0, 180, fc="#f4f4f4", ec="none", zorder=4))
        ax.plot([cx - 4.5, cx - 4.5], [87.1, 90.1], color="#333", lw=1.2, zorder=5)
        ax.plot([cx + 4.5, cx + 4.5], [87.1, 90.1], color="#333", lw=1.2, zorder=5)
        ax.add_patch(Wedge((cx, 90.1), 4.5, 0, 180, fc="none", ec="#333", lw=1.2, zorder=5))
        for dx, c in ((-2.2, "#e53935"), (0, "#43a047"), (2.2, "#1e88e5")):
            ax.add_patch(Circle((cx + dx, 90.2), 0.9, fc=c, ec="none", zorder=5))
        T(ax, cx, 96.6, "RGB LED (common cathode)", fontsize=10.5, weight="bold")


class Pot(Part):
    def __init__(self, name, x1, title="10 kΩ potentiometer"):
        super().__init__(name)
        self.x1, self.title = float(x1), title
        xs = [self.x1, self.x1 + 6, self.x1 + 12]
        self.pins = dict(zip(("T1", "W", "T2"), [(x, Y_LEG) for x in xs]))
        self.plabel = {"T1": "Pot terminal 1", "W": "Pot wiper", "T2": "Pot terminal 2"}
        self.bodies = [(self.x1 - 3, 81, self.x1 + 15, 96)]

    def draw(self, ax):
        x1 = self.x1
        for k, lab in (("T1", "Terminal 1"), ("W", "Wiper"), ("T2", "Terminal 2")):
            x = self.pins[k][0]
            self.leg(ax, [(x, 81), (x, Y_LEG)])
            T(ax, x, 81.6, lab, rotation=90, va="bottom", color="white", fontsize=8.5)
        ax.add_patch(FancyBboxPatch((x1 - 3, 81), 18, 15, boxstyle="round,pad=0,rounding_size=1",
                                    fc="#3f6fb5", ec="#1c3d6e", lw=1.4, zorder=4))
        ax.add_patch(Circle((x1 + 6, 92), 3.0, fc="#d9d9d9", ec="#333", lw=1.2, zorder=5))
        ax.plot([x1 + 6, x1 + 7.8], [92, 94], color="#333", lw=2, zorder=6)
        T(ax, x1 + 6, 97.7, self.title, fontsize=10.5, weight="bold")


class Buzzer(Part):
    """Piezo buzzer; legs are identified by the + / - labels."""

    def __init__(self, name, xneg, xpos):
        super().__init__(name)
        self.xn, self.xp = float(xneg), float(xpos)
        self.pins = {"neg": (self.xn, Y_LEG), "pos": (self.xp, Y_LEG)}
        self.plabel = {"neg": "Buzzer − (negative)", "pos": "Buzzer + (positive)"}
        cx = (self.xn + self.xp) / 2
        self.bodies = [(cx - 6, 82, cx + 6, 94)]

    def draw(self, ax):
        cx = (self.xn + self.xp) / 2
        self.leg(ax, [(self.xn, 83.5), (self.xn, Y_LEG)])
        self.leg(ax, [(self.xp, 83.5), (self.xp, Y_LEG)])
        ax.add_patch(Circle((cx, 88), 6, fc="#262626", ec="#000", lw=1.4, zorder=4))
        ax.add_patch(Circle((cx, 88), 4.6, fc="none", ec="#555", lw=1, zorder=5))
        ax.add_patch(Circle((cx, 88), 1.0, fc="#8a8a8a", ec="#000", lw=1, zorder=5))
        sp = 1 if self.xp > cx else -1
        T(ax, self.xp, 85.0, "+", color="white", fontsize=12, weight="bold")
        T(ax, self.xn, 85.0, "−", color="white", fontsize=12, weight="bold")
        T(ax, self.xp + sp * 0.9, 79.6, "positive (+)", ha="left" if sp > 0 else "right",
          color="#b00000", weight="bold")
        T(ax, self.xn - sp * 0.9, 79.6, "negative (−)", ha="right" if sp > 0 else "left",
          weight="bold")
        T(ax, cx, 96.0, "Piezo buzzer", fontsize=10.5, weight="bold")


class HCSR04(Part):
    P = 5.0

    def __init__(self, name, x0):
        super().__init__(name)
        self.x0 = float(x0)
        self.names = ("VCC", "TRIG", "ECHO", "GND")
        for i, n in enumerate(self.names):
            self.pins[n] = (self.x0 + i * self.P, Y_LEG)
            self.plabel[n] = "HC-SR04 " + n
        self.cx = self.x0 + 1.5 * self.P
        self.bodies = [(self.cx - 13, 81, self.cx + 13, 94.5)]

    def draw(self, ax):
        cx = self.cx
        for n in self.names:
            x = self.pins[n][0]
            self.leg(ax, [(x, 81), (x, Y_LEG)])
            T(ax, x, 82.5, n, color="white", fontsize=8.5, weight="bold")
        ax.add_patch(Rectangle((cx - 13, 81), 26, 13.5, fc="#1565c0", ec="#0b3d7a", lw=1.4, zorder=4))
        for dx, lab in ((-7.3, "T"), (7.3, "R")):
            ax.add_patch(Circle((cx + dx, 89.2), 4.4, fc="#cfd3d6", ec="#444", lw=1.2, zorder=5))
            ax.add_patch(Circle((cx + dx, 89.2), 3.1, fc="#7d858b", ec="#333", lw=1, zorder=5))
            T(ax, cx + dx, 89.2, lab, color="white", fontsize=9, weight="bold")
        T(ax, cx, 96.2, "HC-SR04 ultrasonic sensor", fontsize=10.5, weight="bold")


class PIR(Part):
    P = 6.0

    def __init__(self, name, x0):
        super().__init__(name)
        self.x0 = float(x0)
        self.names = ("Signal", "Power", "Ground")
        for i, n in enumerate(self.names):
            self.pins[n] = (self.x0 + i * self.P, Y_LEG)
            self.plabel[n] = "PIR " + n
        self.cx = self.x0 + self.P
        self.bodies = [(self.cx - 10, 81, self.cx + 10, 95)]

    def draw(self, ax):
        cx = self.cx
        for n in self.names:
            x = self.pins[n][0]
            self.leg(ax, [(x, 81), (x, Y_LEG)])
            T(ax, x, 83.6, n, color="white", fontsize=8.5, weight="bold")
        ax.add_patch(Rectangle((cx - 10, 81), 20, 6.3, fc="#2e7d32", ec="#174a1b", lw=1.4, zorder=4))
        ax.add_patch(Wedge((cx, 87.3), 7.5, 0, 180, fc="#f6f3e7", ec="#555", lw=1.3, zorder=5))
        for a in (30, 60, 90, 120, 150):
            ax.add_patch(Wedge((cx, 87.3), 7.5, a - 0.5, a + 0.5, fc="#bdb9a8", ec="none", zorder=5))
        ax.add_patch(Wedge((cx, 87.3), 4.0, 0, 180, width=0.25, fc="#bdb9a8", ec="none", zorder=5))
        T(ax, cx, 96.6, "PIR motion sensor", fontsize=10.5, weight="bold")


class TMP36(Part):
    P = 6.0

    def __init__(self, name, x0):
        super().__init__(name)
        self.x0 = float(x0)
        self.names = ("Power", "Vout", "GND")
        for i, n in enumerate(self.names):
            self.pins[n] = (self.x0 + i * self.P, Y_LEG)
            self.plabel[n] = "TMP36 " + n
        self.cx = self.x0 + self.P
        self.bodies = [(self.cx - 9, 81, self.cx + 9, 92.2)]

    def draw(self, ax):
        import math
        cx = self.cx
        for n in self.names:
            x = self.pins[n][0]
            self.leg(ax, [(x, 81), (x, Y_LEG)])
            T(ax, x, 82.9, n, color="white", fontsize=8.5, weight="bold")
        pts = [(cx - 9, 81), (cx + 9, 81), (cx + 9, 87)]
        pts += [(cx + 9 * math.cos(math.radians(a)), 87 + 5 * math.sin(math.radians(a)))
                for a in range(0, 181, 6)]
        ax.add_patch(Polygon(pts, closed=True, fc="#222222", ec="#000", lw=1.4, zorder=4))
        T(ax, cx, 88.0, "TMP36", color="white", fontsize=11, weight="bold")
        T(ax, cx, 95.4, "TMP36 temperature sensor\n(flat face toward viewer)", fontsize=10.5, weight="bold")


class LCD(Part):
    P = 4.0
    NAMES = ["VSS", "VDD", "V0", "RS", "RW", "E", "DB0", "DB1", "DB2", "DB3",
             "DB4", "DB5", "DB6", "DB7", "LED A", "LED K"]
    NC = (7, 8, 9, 10)

    def __init__(self, name, x1, lines=("", "")):
        super().__init__(name)
        self.x1, self.lines = float(x1), lines
        for i, n in enumerate(self.NAMES, start=1):
            self.pins[str(i)] = (self.x1 + (i - 1) * self.P, Y_LEG)
            self.plabel[str(i)] = "LCD %d %s" % (i, n)
        self.xa, self.xb = self.x1 - 3.5, self.x1 + 15 * self.P + 3.5
        self.bodies = [(self.xa, 81, self.xb, 95.6)]

    def draw(self, ax):
        for i, n in enumerate(self.NAMES, start=1):
            x = self.pins[str(i)][0]
            if i in self.NC:
                self.leg(ax, [(x, 81), (x, 79.6)], color="#b5b5b5")
            else:
                self.leg(ax, [(x, 81), (x, Y_LEG)])
            T(ax, x, 81.4, "%d %s" % (i, n), rotation=90, va="bottom", fontsize=8.3,
              color="#cfe8d4" if i in self.NC else "white")
        ax.add_patch(Rectangle((self.xa, 81), self.xb - self.xa, 14.6, fc="#1b7a3c",
                               ec="#0d4a22", lw=1.4, zorder=4))
        cx = (self.xa + self.xb) / 2
        ax.add_patch(Rectangle((cx - 27, 88.4), 54, 6.4, fc="#101820", ec="#000", lw=1.2, zorder=5))
        ax.add_patch(Rectangle((cx - 25.5, 88.9), 51, 5.4, fc="#b9dc5a", ec="#5c7a1e", lw=1, zorder=5))
        T(ax, cx, 91.6, "%-16s\n%-16s" % self.lines, family="monospace", fontsize=10.5,
          color="#1d2a05", weight="bold", linespacing=1.15)
        T(ax, cx, 97.4, "LCD 16x2 (HD44780, 4-bit mode)", fontsize=10.5, weight="bold")


# --------------------------------------------------------------------------
# wires
# --------------------------------------------------------------------------
class Wire:
    """Orthogonal polyline.  frm / to are 'PART.pin' refs (or None).
    moves = 'v59 h42 v41'  (v = go vertically to y, h = go horizontally to x)"""

    def __init__(self, frm, to, net, color, moves, start=None, frm_label=None,
                 to_label=None, rail=False, table=True):
        self.frm, self.to, self.net, self.color = frm, to, net, color
        self.moves, self.start = moves, start
        self.frm_label, self.to_label = frm_label, to_label
        self.rail, self.table = rail, table
        self.pts = []

    def build(self, parts):
        if self.frm is not None:
            p = pin_pos(parts, self.frm)
        else:
            p = (float(self.start[0]), float(self.start[1]))
        pts = [p]
        for tok in self.moves.split():
            v = float(tok[1:])
            x, y = pts[-1]
            pts.append((x, v) if tok[0] == "v" else (v, y))
        self.pts = pts

    def segs(self):
        return [(a[0], a[1], b[0], b[1]) for a, b in zip(self.pts[:-1], self.pts[1:])]


def pin_pos(parts, ref):
    pn, pin = ref.split(".")
    assert pn in parts, "unknown part %r in %r" % (pn, ref)
    assert pin in parts[pn].pins, "part %s has no pin %r" % (pn, pin)
    return parts[pn].pins[pin]


# --------------------------------------------------------------------------
# 3. layouts (shared wiring) - the per-question data table is QUESTIONS below
# --------------------------------------------------------------------------
NOTE_DOT = "A filled dot marks a real junction. Wires that cross without a dot are NOT connected."
NOTE_LED = ("LED polarity: long leg = anode (+) goes to the 220 Ω resistor; "
            "short leg = cathode (−) goes to GND.")
NOTE_GND = "All GND pins of the UNO are the same ground, so any of them may be used."


def layout_led(pin="D13"):
    """Q1-Q3: one LED + 220 ohm on D13."""
    parts = [LED("LED1", 30, 36), Resistor("R1", 36, "LED1.anode")]
    wires = [
        Wire("R1.b", "UNO." + pin, pin, "orange", "v59 h42 v41"),
        Wire("LED1.cathode", "UNO.GND1", "GND", "black", "v57 h38 v41"),
    ]
    notes = [NOTE_LED, "The 220 Ω resistor limits the LED current; it may sit on either side of the LED."]
    return parts, wires, [], notes


def layout_led_button():
    """Q4-Q6: LED + 220 ohm on D13, push button on D2 (INPUT_PULLUP)."""
    parts, wires, labels, notes = layout_led()
    parts += [Button("BTN", 82)]
    wires += [
        Wire("BTN.T1a", "UNO.D2", "D2", "blue", "v59 h88 v41"),
        Wire("BTN.T2b", "UNO.GND3", "GND", "black", "v57 h105 v10 h64 v14"),
    ]
    notes = ["Button uses INPUT_PULLUP: no external resistor. Pressed = LOW (active-low).",
             "Use two diagonally opposite button legs (1a and 2b); legs 1b and 2a stay unconnected.",
             NOTE_LED, NOTE_GND]
    return parts, wires, labels, notes


def layout_rgb():
    """Q7-Q8: common-cathode RGB LED, R D11, G D10, B D9."""
    parts = [RGBLed("RGB", 61),
             Resistor("RR", 61, "RGB.R"), Resistor("RB", 77, "RGB.B"),
             Resistor("RG", 85, "RGB.G")]
    wires = [
        Wire("RR.b", "UNO.D11", "D11", "orange", "v59 h50 v41"),
        Wire("RGB.C", "UNO.GND1", "GND", "black", "v57 h38 v41"),
        Wire("RB.b", "UNO.D9", "D9", "blue", "v55 h58 v41"),
        Wire("RG.b", "UNO.D10", "D10", "green", "v53 h54 v41"),
    ]
    notes = ["RGB LED is common cathode (Tinkercad default). Leg order left to right: Red, Cathode, Blue, Green.",
             "One 220 Ω resistor per colour leg; the cathode goes straight to GND. HIGH = colour ON.",
             "D9, D10 and D11 are PWM (~) pins.", NOTE_DOT]
    return parts, wires, [], notes


def _pot_wires():
    return [
        Wire("POT.T1", "UNO.5V", "5V", "red", "v8 h56 v14"),
        Wire("POT.W", "UNO.A0", "A0", "purple", "v59 h7 v10 h76 v14"),
    ]


def layout_pot_led(pin):
    """Q9 (D9, PWM) / Q10 (D13): 10k pot wiper on A0 + one LED."""
    xa = Arduino().pins[pin][0]          # LED anode sits straight above its pin
    xc = xa - 6
    parts = [Pot("POT", 4), LED("LED1", xc, xa), Resistor("R1", xa, "LED1.anode")]
    wires = _pot_wires()
    xr = max(38.0, xc)
    wires += [
        Wire(None, None, "GND", "black", "h%g" % xr, start=(16, Y_GND), rail=True, table=False),
        Wire("POT.T2", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LED1.cathode", None, "GND", "black", "v62", to_label="GND rail"),
        Wire(None, "UNO.GND1", "GND", "black", "v41", start=(38, Y_GND), frm_label="GND rail"),
        Wire("R1.b", "UNO." + pin, pin, "orange", "v41"),
    ]
    labels = [(27, 63.4, "GND rail", "#111")]
    notes = ["Potentiometer: terminal 1 to 5V, wiper (middle leg) to A0, terminal 2 to GND.",
             NOTE_LED, NOTE_DOT]
    if pin == "D9":
        notes.insert(1, "D9 is a PWM (~) pin, required for analogWrite().")
    return parts, wires, labels, notes


def layout_pot_3led():
    """Q11: pot on A0, GREEN D2, YELLOW D3, RED D4."""
    parts = [Pot("POT", 4),
             LED("LEDR", 38, 44, "red", "Red LED"), Resistor("R_R", 44, "LEDR.anode"),
             LED("LEDY", 65, 71, "yellow", "Yellow LED"), Resistor("R_Y", 71, "LEDY.anode"),
             LED("LEDG", 92, 98, "green", "Green LED"), Resistor("R_G", 98, "LEDG.anode")]
    wires = _pot_wires()
    wires += [
        Wire(None, None, "GND", "black", "h92", start=(16, Y_GND), rail=True, table=False),
        Wire("POT.T2", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LEDR.cathode", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LEDY.cathode", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LEDG.cathode", None, "GND", "black", "v62", to_label="GND rail"),
        Wire(None, "UNO.GND1", "GND", "black", "v41", start=(38, Y_GND), frm_label="GND rail"),
        Wire("R_R.b", "UNO.D4", "D4", "orange", "v57 h80 v41"),
        Wire("R_Y.b", "UNO.D3", "D3", "yellow", "v59 h84 v41"),
        Wire("R_G.b", "UNO.D2", "D2", "green", "v55 h88 v41"),
    ]
    labels = [(27, 63.4, "GND rail", "#111")]
    notes = ["Potentiometer: terminal 1 to 5V, wiper (middle leg) to A0, terminal 2 to GND.",
             "GREEN = D2, YELLOW = D3, RED = D4. Each LED has its own 220 Ω resistor.",
             NOTE_LED, NOTE_DOT]
    return parts, wires, labels, notes


def layout_lcd(lines):
    """Q12-Q14: LCD 16x2 in 4-bit mode, LiquidCrystal lcd(12, 11, 5, 4, 3, 2)."""
    parts = [Pot("POT", 4, "10 kΩ pot (contrast)"), LCD("LCD", 27, lines),
             Resistor("R15", 83, "LCD.15", label="rot")]
    wires = [
        # 5V: pot terminal 1 runs straight down to the 5V pin, the rail tees off it
        Wire("POT.T1", "UNO.5V", "5V", "red", "v8 h56 v14"),
        Wire(None, None, "5V", "red", "h83", start=(4, Y_5V), rail=True, table=False),
        Wire("LCD.2", None, "5V", "red", "v65", to_label="5V rail"),
        Wire("R15.b", None, "5V", "red", "v65", to_label="5V rail"),
        # GND rail
        Wire(None, None, "GND", "black", "h87", start=(16, Y_GND), rail=True, table=False),
        Wire("POT.T2", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LCD.1", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LCD.5", None, "GND", "black", "v62", to_label="GND rail"),
        Wire("LCD.16", None, "GND", "black", "v62", to_label="GND rail"),
        Wire(None, "UNO.GND1", "GND", "black", "v41", start=(38, Y_GND), frm_label="GND rail"),
        # contrast
        Wire("LCD.3", "POT.W", "V0", "brown", "v55 h10 v78"),
        # control + data
        Wire("LCD.4", "UNO.D12", "D12", "purple", "v49 h46 v41"),
        Wire("LCD.6", "UNO.D11", "D11", "cyan", "v47 h50 v41"),
        Wire("LCD.11", "UNO.D5", "D5", "orange", "v53 h76 v41"),
        Wire("LCD.12", "UNO.D4", "D4", "yellow", "v55 h80 v41"),
        Wire("LCD.13", "UNO.D3", "D3", "green", "v57 h84 v41"),
        Wire("LCD.14", "UNO.D2", "D2", "blue", "v59 h88 v41"),
    ]
    labels = [(57, 66.4, "5V rail", COL["red"]), (57, 63.4, "GND rail", "#111")]
    notes = ["LiquidCrystal lcd(12, 11, 5, 4, 3, 2);   // RS, E, DB4, DB5, DB6, DB7",
             "LCD pins 7-10 (DB0-DB3) are not connected (4-bit mode). RW (pin 5) is tied to GND.",
             "Pot terminal 1 is wired straight to the Arduino 5V pin; the 5V rail tees off that wire.",
             "Turn the 10 kΩ pot to set the contrast if the screen looks blank. Backlight: pin 15 to 5V "
             "through 220 Ω, pin 16 to GND.",
             NOTE_DOT]
    return parts, wires, labels, notes


def layout_ultrasonic():
    """Q15-Q17: HC-SR04 TRIG D9 / ECHO D10, piezo buzzer D8."""
    parts = [HCSR04("HC", 66), Buzzer("BUZ", 96, 102)]
    wires = [
        Wire("HC.VCC", "UNO.5V", "5V", "red", "v59 h7 v10 h56 v14"),
        Wire("HC.TRIG", "UNO.D9", "D9", "blue", "v57 h58 v41"),
        Wire("HC.ECHO", "UNO.D10", "D10", "green", "v55 h54 v41"),
        Wire("HC.GND", "UNO.GND3", "GND", "black", "v62 h105 v8 h64 v14"),
        Wire("BUZ.neg", None, "GND", "black", "v62", to_label="GND wire (at dot)"),
        Wire("BUZ.pos", "UNO.D8", "D8", "orange", "v53 h62 v41"),
    ]
    notes = ["HC-SR04 = Tinkercad 'Ultrasonic Distance Sensor (4-pin)': VCC, TRIG, ECHO, GND.",
             "Buzzer − joins the sensor's GND wire at the dot; that wire goes to an Arduino GND pin.",
             "Piezo buzzer: + (positive) to D8, − (negative) to GND. Check the + mark on the part.",
             NOTE_DOT]
    return parts, wires, [], notes


def layout_pir(with_led):
    """Q18 (PIR + buzzer) / Q19 (PIR + buzzer + LED on D13)."""
    parts = [PIR("PIR", 88), Buzzer("BUZ", 66, 72)]
    wires = [
        Wire("PIR.Signal", "UNO.D2", "D2", "blue", "v41"),
        Wire("PIR.Power", "UNO.5V", "5V", "red", "v57 h105 v10 h56 v14"),
        Wire("PIR.Ground", "UNO.GND3", "GND", "black", "v59 h107 v8 h64 v14"),
        Wire("BUZ.pos", "UNO.D8", "D8", "orange", "v57 h62 v41"),
        Wire("BUZ.neg", "UNO.GND1", "GND", "black", "v62 h38 v41"),
    ]
    notes = ["PIR leg order (left to right): Signal, Power, Ground. Signal is HIGH while motion is detected.",
             "Piezo buzzer: + (positive) to D8, − (negative) to GND. Check the + mark on the part.",
             NOTE_GND, NOTE_DOT]
    if with_led:
        parts += [LED("LED1", 36, 42), Resistor("R1", 42, "LED1.anode")]
        wires += [
            Wire("R1.b", "UNO.D13", "D13", "green", "v41"),
            Wire("LED1.cathode", None, "GND", "black", "v62 h38", to_label="GND wire (at dot)"),
        ]
        notes.insert(2, NOTE_LED)
        notes.remove(NOTE_GND)
    return parts, wires, [], notes


def layout_tmp36():
    """Q20: TMP36 Vout on A0."""
    parts = [TMP36("TMP", 50)]
    wires = [
        Wire("TMP.Power", "UNO.5V", "5V", "red", "v55 h7 v6 h56 v14"),
        Wire("TMP.Vout", "UNO.A0", "A0", "orange", "v57 h105 v10 h76 v14"),
        Wire("TMP.GND", "UNO.GND3", "GND", "black", "v59 h107 v8 h64 v14"),
    ]
    notes = ["TMP36 with its flat face toward you, left to right: Power, Vout, GND.",
             "Reversing Power and GND will overheat the sensor: check the orientation before powering.",
             "Readings appear on the Serial Monitor at 9600 baud (no extra wiring: USB only)."]
    return parts, wires, [], notes


# ---- expected netlists, transcribed by hand from PIN_MAP.md -----------------
def _e(*items):
    return set(items)


E_LED13 = _e(("LED1.anode", "R", "D13"), ("LED1.cathode", "", "GND"))
E_BTN = E_LED13 | _e(("BTN.T1a", "", "D2"), ("BTN.T2b", "", "GND"))
E_RGB = _e(("RGB.R", "R", "D11"), ("RGB.G", "R", "D10"), ("RGB.B", "R", "D9"), ("RGB.C", "", "GND"))
E_POT = _e(("POT.T1", "", "5V"), ("POT.W", "", "A0"), ("POT.T2", "", "GND"))
E_LCD = _e(("LCD.1", "", "GND"), ("LCD.2", "", "5V"), ("LCD.3", "", "POT.W"), ("POT.W", "", "LCD.3"),
           ("LCD.4", "", "D12"), ("LCD.5", "", "GND"), ("LCD.6", "", "D11"),
           ("LCD.11", "", "D5"), ("LCD.12", "", "D4"), ("LCD.13", "", "D3"), ("LCD.14", "", "D2"),
           ("LCD.15", "R", "5V"), ("LCD.16", "", "GND"), ("POT.T1", "", "5V"), ("POT.T2", "", "GND"))
E_HC = _e(("HC.VCC", "", "5V"), ("HC.TRIG", "", "D9"), ("HC.ECHO", "", "D10"), ("HC.GND", "", "GND"),
          ("BUZ.pos", "", "D8"), ("BUZ.neg", "", "GND"))
E_PIR = _e(("PIR.Signal", "", "D2"), ("PIR.Power", "", "5V"), ("PIR.Ground", "", "GND"),
           ("BUZ.pos", "", "D8"), ("BUZ.neg", "", "GND"))
E_TMP = _e(("TMP.Power", "", "5V"), ("TMP.Vout", "", "A0"), ("TMP.GND", "", "GND"))

# ---- per-question table: (number, filename stem, title, layout, expected) ---
QUESTIONS = [
    (1, "Q01_Automatic_Corridor_Light", "Automatic Corridor Light", layout_led, E_LED13),
    (2, "Q02_Emergency_Warning_Indicator", "Emergency Warning Indicator", layout_led, E_LED13),
    (3, "Q03_Railway_Platform_Indicator", "Railway Platform Indicator", layout_led, E_LED13),
    (4, "Q04_Classroom_Light_Control", "Classroom Light Control", layout_led_button, E_BTN),
    (5, "Q05_Security_Door_Indicator", "Security Door Indicator", layout_led_button, E_BTN),
    (6, "Q06_Toggle_Based_Lamp_Control", "Toggle Based Lamp Control", layout_led_button, E_BTN),
    (7, "Q07_Traffic_Signal_Status_Indicator", "Traffic Signal Status Indicator", layout_rgb, E_RGB),
    (8, "Q08_Mood_Lighting_System", "Mood Lighting System", layout_rgb, E_RGB),
    (9, "Q09_Variable_Brightness_Controller", "Variable Brightness Controller",
     lambda: layout_pot_led("D9"),
     E_POT | _e(("LED1.anode", "R", "D9"), ("LED1.cathode", "", "GND"))),
    (10, "Q10_Over_Voltage_Warning_System", "Over Voltage Warning System",
     lambda: layout_pot_led("D13"), E_POT | E_LED13),
    (11, "Q11_Three_Level_Voltage_Indicator", "Three Level Voltage Indicator", layout_pot_3led,
     E_POT | _e(("LEDG.anode", "R", "D2"), ("LEDY.anode", "R", "D3"), ("LEDR.anode", "R", "D4"),
                ("LEDG.cathode", "", "GND"), ("LEDY.cathode", "", "GND"), ("LEDR.cathode", "", "GND"))),
    (12, "Q12_Student_Identification_Display", "Student Identification Display",
     lambda: layout_lcd(("Your Name", "Roll No: 00")), E_LCD),
    (13, "Q13_Digital_Welcome_System", "Digital Welcome System",
     lambda: layout_lcd(("WELCOME TO AIEC", "ARDUINO LAB")), E_LCD),
    (14, "Q14_Mini_Information_Display", "Mini Information Display",
     lambda: layout_lcd(("AIEC - E&TC Dept", "")), E_LCD),
    (15, "Q15_Smart_Parking_Alert", "Smart Parking Alert", layout_ultrasonic, E_HC),
    (16, "Q16_Obstacle_Detection_System", "Obstacle Detection System", layout_ultrasonic, E_HC),
    (17, "Q17_Water_Tank_Level_Warning", "Water Tank Level Warning", layout_ultrasonic, E_HC),
    (18, "Q18_Motion_Based_Security_Alarm", "Motion Based Security Alarm",
     lambda: layout_pir(False), E_PIR),
    (19, "Q19_Smart_Entry_Alert", "Smart Entry Alert",
     lambda: layout_pir(True), E_PIR | E_LED13),
    (20, "Q20_Temperature_Monitoring_System", "Temperature Monitoring System", layout_tmp36, E_TMP),
]

# --------------------------------------------------------------------------
# 5. self-check helpers
# --------------------------------------------------------------------------
EPS = 1e-6


def on_seg(p, s):
    x, y = p
    x0, y0, x1, y1 = s
    return (min(x0, x1) - EPS <= x <= max(x0, x1) + EPS and
            min(y0, y1) - EPS <= y <= max(y0, y1) + EPS)


def strictly_inside(p, s):
    """p lies on s but is not one of its end points."""
    return on_seg(p, s) and abs(p[0] - s[0]) + abs(p[1] - s[1]) > EPS and \
        abs(p[0] - s[2]) + abs(p[1] - s[3]) > EPS


def collinear_overlap(a, b):
    ah, bh = abs(a[1] - a[3]) < EPS, abs(b[1] - b[3]) < EPS
    if ah and bh and abs(a[1] - b[1]) < EPS:
        return min(max(a[0], a[2]), max(b[0], b[2])) - max(min(a[0], a[2]), min(b[0], b[2])) > EPS
    if (not ah) and (not bh) and abs(a[0] - b[0]) < EPS:
        return min(max(a[1], a[3]), max(b[1], b[3])) - max(min(a[1], a[3]), min(b[1], b[3])) > EPS
    return False


def x_cross(a, b):
    """True if a and b cross at a point interior to both (a real 'X')."""
    ah, bh = abs(a[1] - a[3]) < EPS, abs(b[1] - b[3]) < EPS
    if ah == bh:
        return False
    h, v = (a, b) if ah else (b, a)
    return (min(h[0], h[2]) + EPS < v[0] < max(h[0], h[2]) - EPS and
            min(v[1], v[3]) + EPS < h[1] < max(v[1], v[3]) - EPS)


def seg_hits_rect(s, r, pad):
    x0, x1 = min(s[0], s[2]) - pad, max(s[0], s[2]) + pad
    y0, y1 = min(s[1], s[3]) - pad, max(s[1], s[3]) + pad
    return min(x1, r[2]) - max(x0, r[0]) > EPS and min(y1, r[3]) - max(y0, r[1]) > EPS


def check_and_netlist(qn, parts, wires, expected):
    errs = []
    uno = parts["UNO"]
    # (1) every referenced pin exists (pin_pos asserts), wire ends land on 'to'
    for w in wires:
        assert w.net in ("GND", "5V", "V0") or w.net in uno.pins, "bad net %r" % w.net
        assert w.color in COL, "bad colour %r" % w.color
        if w.to is not None:
            tp = pin_pos(parts, w.to)
            if abs(tp[0] - w.pts[-1][0]) + abs(tp[1] - w.pts[-1][1]) > EPS:
                errs.append("wire %s->%s ends at %s, pin is at %s" % (w.frm, w.to, w.pts[-1], tp))
        for s in w.segs():
            if abs(s[0] - s[2]) > EPS and abs(s[1] - s[3]) > EPS:
                errs.append("non-orthogonal segment in %s->%s" % (w.frm, w.to))
        if (w.color == "red") != (w.net == "5V") or (w.color == "black") != (w.net == "GND"):
            errs.append("colour code broken on %s->%s (%s, net %s)" % (w.frm, w.to, w.color, w.net))
    # resistors really touch the leg they are attached to
    for p in parts.values():
        if p.attach:
            a = pin_pos(parts, p.attach)
            if a != p.pins["a"]:
                errs.append("resistor %s does not touch %s" % (p.name, p.attach))
    # distinct signal colours
    sig = {}
    for w in wires:
        if w.net not in ("GND", "5V"):
            sig.setdefault(w.color, set()).add(w.net)
    for c, nets in sig.items():
        if len(nets) > 1:
            errs.append("colour %s reused for nets %s" % (c, sorted(nets)))

    # (2) geometry: overlaps, crossings, junctions -> geometric nets (union-find)
    parent = list(range(len(wires)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    crossings = 0
    for i, a in enumerate(wires):
        for j in range(i + 1, len(wires)):
            b = wires[j]
            touch = False
            for sa in a.segs():
                for sb in b.segs():
                    if collinear_overlap(sa, sb):
                        errs.append("wires overlap: %s->%s and %s->%s" % (a.frm, a.to, b.frm, b.to))
                    if x_cross(sa, sb):
                        crossings += 1
                        if a.net == b.net:
                            errs.append("same-net X crossing without modelled junction (%s)" % a.net)
            for end in (a.pts[0], a.pts[-1]):
                if any(on_seg(end, sb) for sb in b.segs()):
                    touch = True
            for end in (b.pts[0], b.pts[-1]):
                if any(on_seg(end, sa) for sa in a.segs()):
                    touch = True
            # a bend of one wire lying on the other wire also counts as contact
            for q in a.pts[1:-1]:
                if any(on_seg(q, sb) for sb in b.segs()):
                    touch = True
            for q in b.pts[1:-1]:
                if any(on_seg(q, sa) for sa in a.segs()):
                    touch = True
            if touch:
                if a.net != b.net:
                    errs.append("SHORT: %s->%s (%s) touches %s->%s (%s)" %
                                (a.frm, a.to, a.net, b.frm, b.to, b.net))
                parent[find(i)] = find(j)
    # a wire must not cross itself
    for w in wires:
        ss = w.segs()
        for i in range(len(ss)):
            for j in range(i + 2, len(ss)):
                if x_cross(ss[i], ss[j]) or collinear_overlap(ss[i], ss[j]):
                    errs.append("wire %s->%s crosses itself" % (w.frm, w.to))

    groups = {}
    for i, w in enumerate(wires):
        groups.setdefault(find(i), []).append(w)

    # (3) one net per Arduino pin, one wire per header hole, nets match pins
    hole = {}
    for w in wires:
        for ref in (w.frm, w.to):
            if ref and ref.startswith("UNO."):
                hole.setdefault(ref, []).append(w)
    for ref, ws in hole.items():
        if len(ws) > 1:
            errs.append("Arduino pin %s used by %d wires" % (ref, len(ws)))
        if len({w.net for w in ws}) > 1:
            errs.append("Arduino pin %s used by two different nets" % ref)
    group_of = {}
    for gid, ws in groups.items():
        refs = set()
        for w in ws:
            refs.update(r for r in (w.frm, w.to) if r)
        unos = {canon(r.split(".")[1]) for r in refs if r.startswith("UNO.")}
        if len(unos) > 1:
            errs.append("net joins several Arduino pins: %s" % sorted(unos))
        if len({w.net for w in ws}) > 1:
            errs.append("geometric net mixes declared nets %s" % sorted({w.net for w in ws}))
        for u in unos:
            if ws[0].net != u:
                errs.append("net declared %s but lands on Arduino %s" % (ws[0].net, u))
        if not unos and ws[0].net != "V0":
            errs.append("net %s never reaches an Arduino pin" % ws[0].net)
        for r in refs:
            if r in group_of:
                errs.append("pin %s belongs to two nets" % r)
            group_of[r] = (refs, unos)

    # (4) no wire through a body, a foreign leg or a foreign pin
    for w in wires:
        own = {w.pts[0], w.pts[-1]}
        for s in w.segs():
            for p in parts.values():
                for r in p.bodies:
                    if seg_hits_rect(s, r, 0.2):
                        errs.append("wire %s->%s passes through body of %s" % (w.frm, w.to, p.name))
                for lg in p.legs:
                    r = (lg[0] - 0.1, lg[1] + 0.1, lg[2] + 0.1, lg[3] - 0.1)
                    if r[3] > r[1] and seg_hits_rect(s, r, 0.0):
                        errs.append("wire %s->%s runs over a leg of %s" % (w.frm, w.to, p.name))
                for pn, pp in p.pins.items():
                    if pp not in own and on_seg(pp, s):
                        errs.append("wire %s->%s passes over pin %s.%s" % (w.frm, w.to, p.name, pn))

    # (5) derived netlist == PIN_MAP expectation
    derived = set()
    for r, (refs, unos) in group_of.items():
        pn = r.split(".")[0]
        if pn == "UNO":
            continue
        if parts[pn].attach:                       # resistor bottom lead
            tgt = unos or {x for x in refs if x != r and not x.startswith("UNO.")}
            for u in tgt:
                derived.add((parts[pn].attach, "R", u))
            continue
        if unos:
            for u in unos:
                derived.add((r, "", u))
        else:
            for o in refs:
                if o != r:
                    derived.add((r, "", o))
    if derived != expected:
        errs.append("NETLIST MISMATCH vs PIN_MAP: extra=%s missing=%s" %
                    (sorted(derived - expected), sorted(expected - derived)))
    return errs, crossings, groups, derived


def junction_points(groups):
    dots = []
    for ws in groups.values():
        segs = [s for w in ws for s in w.segs()]
        cand = {w.pts[0] for w in ws} | {w.pts[-1] for w in ws}
        for p in cand:
            arms = set()
            for s in segs:
                if not on_seg(p, s):
                    continue
                for q in ((s[0], s[1]), (s[2], s[3])):
                    dx, dy = q[0] - p[0], q[1] - p[1]
                    if abs(dx) > EPS:
                        arms.add("E" if dx > 0 else "W")
                    if abs(dy) > EPS:
                        arms.add("N" if dy > 0 else "S")
            if len(arms) >= 3:
                dots.append((p, ws[0].color))
    return dots


# --------------------------------------------------------------------------
# 4. renderer
# --------------------------------------------------------------------------
def wire_label(parts, ref):
    pn, pin = ref.split(".")
    return parts[pn].plabel[pin]


def table_rows(parts, wires):
    rows = []
    for w in wires:
        if not w.table:
            continue
        to = w.to_label or wire_label(parts, w.to)
        if w.frm_label:
            frm = w.frm_label
        else:
            pn = w.frm.split(".")[0]
            if parts[pn].attach:
                frm = wire_label(parts, parts[pn].attach)
                to = "%s → %s" % (parts[pn].value, to)
            else:
                frm = wire_label(parts, w.frm)
        rows.append((frm, to, w.color))
    return rows


def draw_table(ax, rows, notes):
    x0, x1 = TABLE_X0, TABLE_X1
    cx = (x0 + 0.8, x0 + 20.6, x0 + 39.5)
    y = 93.5
    T(ax, x0, y, "Connections", ha="left", fontsize=15, weight="bold")
    T(ax, x1, y - 0.2, "Arduino UNO R3 · Tinkercad Circuits", ha="right", fontsize=8.5, color="#555")
    y -= 3.6
    rh = 2.95
    ax.add_patch(Rectangle((x0, y - rh / 2), x1 - x0, rh, fc="#263238", ec="none", zorder=1))
    for x, s in zip(cx, ("From", "To", "Wire colour")):
        T(ax, x, y, s, ha="left", color="white", fontsize=10, weight="bold")
    for i, (frm, to, c) in enumerate(rows):
        y -= rh
        ax.add_patch(Rectangle((x0, y - rh / 2), x1 - x0, rh,
                               fc="#f1f4f6" if i % 2 == 0 else "white", ec="none", zorder=1))
        T(ax, cx[0], y, frm, ha="left", fontsize=10)
        T(ax, cx[1], y, to, ha="left", fontsize=10)
        ax.plot([cx[2], cx[2] + 3.4], [y, y], color=COL[c], lw=4.5, solid_capstyle="butt", zorder=3)
        T(ax, cx[2] + 4.4, y, c, ha="left", fontsize=10)
    ybot = y - rh / 2
    ax.add_patch(Rectangle((x0, ybot), x1 - x0, (93.5 - 3.6 + rh / 2) - ybot, fc="none",
                           ec="#263238", lw=1.2, zorder=2))
    y = ybot - 3.2
    T(ax, x0, y, "Notes", ha="left", fontsize=12, weight="bold")
    y -= 2.7
    for n in notes:
        # keep "220 Ω" / "10 kΩ" on one line
        lines = textwrap.wrap(n.replace("220 Ω", "220 Ω").replace("10 kΩ", "10 kΩ"), 60)
        for k, ln in enumerate(lines):
            ln = ln.replace(" ", " ")
            T(ax, x0 + (0.0 if k == 0 else 1.6), y, ("• " if k == 0 else "") + ln,
              ha="left", fontsize=9.5)
            y -= 2.15
        y -= 0.75
    return y


def render(qn, stem, title, layout, expected):
    plist, wires, labels, notes = layout()
    uno = Arduino()
    parts = {"UNO": uno}
    for p in plist:
        assert p.name not in parts, "duplicate part " + p.name
        parts[p.name] = p
    for w in wires:
        w.build(parts)

    fig = plt.figure(figsize=(W / 10, H / 10), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")

    T(ax, W / 2, 101.2, "Q%d - %s" % (qn, title), fontsize=21, weight="bold")
    ax.plot([2, W - 2], [99.2, 99.2], color="#263238", lw=1.2, zorder=1)
    ax.plot([113.5, 113.5], [2, 98], color="#cfd8dc", lw=1, zorder=1)

    used = {r.split(".")[1] for w in wires for r in (w.frm, w.to) if r and r.startswith("UNO.")}
    uno.draw(ax, used)
    for p in plist:
        p.draw(ax)

    errs, crossings, groups, derived = check_and_netlist(qn, parts, wires, expected)

    # wires: rails first, then the rest; a white halo makes crossings read as
    # "one wire passes over the other" (no dot = no connection)
    for w in sorted(wires, key=lambda w: not w.rail):
        xs = [p[0] for p in w.pts]
        ys = [p[1] for p in w.pts]
        lw = 4.2 if w.rail else 2.8
        ax.plot(xs, ys, color="white", lw=lw + 2.6, solid_capstyle="butt",
                solid_joinstyle="miter", zorder=5)
        ax.plot(xs, ys, color=COL[w.color], lw=lw, solid_capstyle="round",
                solid_joinstyle="round", zorder=5)
    for (x, y), c in junction_points(groups):
        ax.add_patch(Circle((x, y), 0.62, fc=COL[c], ec="white", lw=0.8, zorder=6))
    for w in wires:
        if w.to and w.to.startswith("UNO."):
            x, y = w.pts[-1]
            ax.add_patch(Circle((x, y), 0.5, fc=COL[w.color], ec="#000", lw=0.8, zorder=7))
    for x, y, s, c in labels:
        T(ax, x, y, s, color=c, fontsize=9, weight="bold", style="italic")

    ynotes = draw_table(ax, table_rows(parts, wires), notes)
    if ynotes < 1.5:
        errs.append("notes run off the bottom of the page")

    # text checks need real extents
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    boxes = []
    for t in ax.texts:
        bb = t.get_window_extent(rend).transformed(inv)
        boxes.append((t.get_text().replace("\n", " "), (bb.x0, bb.y0, bb.x1, bb.y1)))
    for s, b in boxes:
        if b[0] < 0.3 or b[1] < 0.3 or b[2] > W - 0.3 or b[3] > H - 0.3:
            errs.append("text clipped by page edge: %r" % s)
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if min(a[2], b[2]) - max(a[0], b[0]) > 0.05 and min(a[3], b[3]) - max(a[1], b[1]) > 0.05:
                errs.append("text overlap: %r / %r" % (boxes[i][0], boxes[j][0]))
    for w in wires:
        for s in w.segs():
            for txt, b in boxes:
                if seg_hits_rect(s, b, 0.3):
                    errs.append("wire %s->%s runs through text %r" % (w.frm, w.to, txt))

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, stem + ".png")
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    return errs, crossings, derived, table_rows(parts, wires)


def main():
    bad = 0
    for qn, stem, title, layout, expected in QUESTIONS:
        errs, crossings, derived, rows = render(qn, stem, title, layout, expected)
        print("Q%02d %-40s wires=%2d crossings=%d %s" %
              (qn, stem, len(rows), crossings, "OK" if not errs else "FAIL"))
        if "-v" in sys.argv:
            for frm, to, c in rows:
                print("      %-22s -> %-22s [%s]" % (frm, to, c))
        for e in sorted(set(errs)):
            bad += 1
            print("   !! " + e)
    files = sorted(os.listdir(OUT_DIR))
    want = sorted(q[1] + ".png" for q in QUESTIONS)
    assert files == want, "circuits folder must hold exactly the 20 PNGs: %s" % (set(files) ^ set(want))
    if bad:
        sys.exit("%d self-check problem(s)" % bad)
    print("all 20 diagrams written, self-check passed")


if __name__ == "__main__":
    main()
