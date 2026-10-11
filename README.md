# Digital Electronics Practicals: Arduino UNO & Tinkercad

Twenty simulation practicals (Q1-Q20) for Arduino UNO in Tinkercad Circuits. Each question has one standalone sketch and one matching wiring diagram. The hardware-only (H/W) practicals are not included.

## Repository layout

```
godwiththorns/
├── code/        20 Arduino sketches, one per question (.ino)
├── circuits/    20 wiring diagrams, one per question (.png)
└── .vscode/     VS Code tasks to compile the sketches with arduino-cli
PIN_MAP.md       shared pin mapping used by both the code and the diagrams
draw_circuits.py script that generates the diagrams from the pin map
```

## Practicals

| Q | Title | Hardware | Behaviour |
|---|-------|----------|-----------|
| 1 | [Automatic Corridor Light](godwiththorns/code/Q01_Automatic_Corridor_Light.ino) · [circuit](godwiththorns/circuits/Q01_Automatic_Corridor_Light.png) | LED | ON 2 s, OFF 1 s, repeating |
| 2 | [Emergency Warning Indicator](godwiththorns/code/Q02_Emergency_Warning_Indicator.ino) · [circuit](godwiththorns/circuits/Q02_Emergency_Warning_Indicator.png) | LED | One blink cycle per 500 ms, double-flash strobe pattern |
| 3 | [Railway Platform Indicator](godwiththorns/code/Q03_Railway_Platform_Indicator.ino) · [circuit](godwiththorns/circuits/Q03_Railway_Platform_Indicator.png) | LED | Three quick flashes, then a 2 s pause |
| 4 | [Classroom Light Control](godwiththorns/code/Q04_Classroom_Light_Control.ino) · [circuit](godwiththorns/circuits/Q04_Classroom_Light_Control.png) | LED, push button | LED ON while the button is pressed |
| 5 | [Security Door Indicator](godwiththorns/code/Q05_Security_Door_Indicator.ino) · [circuit](godwiththorns/circuits/Q05_Security_Door_Indicator.png) | LED, push button | Switch active = door open = LED ON |
| 6 | [Toggle-Based Lamp Control](godwiththorns/code/Q06_Toggle_Based_Lamp_Control.ino) · [circuit](godwiththorns/circuits/Q06_Toggle_Based_Lamp_Control.png) | LED, push button | Each press toggles the LED (debounced) |
| 7 | [Traffic Signal Status Indicator](godwiththorns/code/Q07_Traffic_Signal_Status_Indicator.ino) · [circuit](godwiththorns/circuits/Q07_Traffic_Signal_Status_Indicator.png) | RGB LED | Red STOP, green GO, blue WAIT |
| 8 | [Mood Lighting System](godwiththorns/code/Q08_Mood_Lighting_System.ino) · [circuit](godwiththorns/circuits/Q08_Mood_Lighting_System.png) | RGB LED | Cycles six colours, 1 s each |
| 9 | [Variable Brightness Controller](godwiththorns/code/Q09_Variable_Brightness_Controller.ino) · [circuit](godwiththorns/circuits/Q09_Variable_Brightness_Controller.png) | Potentiometer, LED | PWM brightness follows the pot |
| 10 | [Over-Voltage Warning System](godwiththorns/code/Q10_Over_Voltage_Warning_System.ino) · [circuit](godwiththorns/circuits/Q10_Over_Voltage_Warning_System.png) | Potentiometer, LED | LED ON above 2.5 V |
| 11 | [Three-Level Voltage Indicator](godwiththorns/code/Q11_Three_Level_Voltage_Indicator.ino) · [circuit](godwiththorns/circuits/Q11_Three_Level_Voltage_Indicator.png) | Potentiometer, 3 LEDs | Green below 1.5 V, yellow 1.5-3.5 V, red above 3.5 V |
| 12 | [Student Identification Display](godwiththorns/code/Q12_Student_Identification_Display.ino) · [circuit](godwiththorns/circuits/Q12_Student_Identification_Display.png) | 16x2 LCD | Name on line 1, roll number on line 2 |
| 13 | [Digital Welcome System](godwiththorns/code/Q13_Digital_Welcome_System.ino) · [circuit](godwiththorns/circuits/Q13_Digital_Welcome_System.png) | 16x2 LCD | Welcome message, then name and roll number after 3 s |
| 14 | [Mini Information Display](godwiththorns/code/Q14_Mini_Information_Display.ino) · [circuit](godwiththorns/circuits/Q14_Mini_Information_Display.png) | 16x2 LCD | College, name, roll number, practical number, 2 s each |
| 15 | [Smart Parking Alert](godwiththorns/code/Q15_Smart_Parking_Alert.ino) · [circuit](godwiththorns/circuits/Q15_Smart_Parking_Alert.png) | HC-SR04, buzzer | Off above 50 cm, slow beep 20-50 cm, rapid beep below 20 cm |
| 16 | [Obstacle Detection System](godwiththorns/code/Q16_Obstacle_Detection_System.ino) · [circuit](godwiththorns/circuits/Q16_Obstacle_Detection_System.png) | HC-SR04, buzzer | Buzzer ON within 15 cm |
| 17 | [Water Tank Level Warning](godwiththorns/code/Q17_Water_Tank_Level_Warning.ino) · [circuit](godwiththorns/circuits/Q17_Water_Tank_Level_Warning.png) | HC-SR04, buzzer | Buzzer ON below 10 cm |
| 18 | [Motion-Based Security Alarm](godwiththorns/code/Q18_Motion_Based_Security_Alarm.ino) · [circuit](godwiththorns/circuits/Q18_Motion_Based_Security_Alarm.png) | PIR, buzzer | Buzzer ON for 5 s on motion |
| 19 | [Smart Entry Alert](godwiththorns/code/Q19_Smart_Entry_Alert.ino) · [circuit](godwiththorns/circuits/Q19_Smart_Entry_Alert.png) | PIR, buzzer, LED | LED and buzzer ON while motion is detected |
| 20 | [Temperature Monitoring System](godwiththorns/code/Q20_Temperature_Monitoring_System.ino) · [circuit](godwiththorns/circuits/Q20_Temperature_Monitoring_System.png) | TMP36 | Serial output in °C, alert above 35 °C |

## Conventions

- Board: Arduino UNO R3 in Tinkercad Circuits.
- LEDs use a 220 Ω series resistor; push buttons use `INPUT_PULLUP` (pressed = LOW) with no external resistor.
- RGB LED is common cathode, with one 220 Ω resistor per colour.
- Ultrasonic sensor: TRIG on D9, ECHO on D10. PIR signal on D2. Buzzer on D8. TMP36 output on A0.
- LCD (4-bit mode): `LiquidCrystal lcd(12, 11, 5, 4, 3, 2);` with a 10 kΩ pot for contrast.
- Full pin tables are in [PIN_MAP.md](PIN_MAP.md).

## Using the sketches

1. In Tinkercad, create a new Circuit and add an Arduino UNO R3.
2. Build the circuit shown in the matching PNG under `circuits/`.
3. Open **Code**, switch to **Text**, and paste the matching `.ino` file.
4. Press **Start Simulation**.

Before use, edit the placeholders at the top of Q12-Q14 (`STUDENT_NAME`, `ROLL_NUMBER`, `COLLEGE_NAME`, `PRACTICAL_NO`). Each string must be 16 characters or fewer.

## Compiling locally (VS Code)

Install [arduino-cli](https://arduino.github.io/arduino-cli/) with the `arduino:avr` core and the `LiquidCrystal` library, open the `godwiththorns` folder in VS Code, and run the task **Arduino: Verify all 20 sketches** (or `Ctrl+Shift+B` to verify the open sketch).

## Assumptions

The problem statements leave a few details open. These are the choices made, each marked in the sketch header and editable as a named constant:

- Q2: the "emergency" pattern is a double-flash strobe inside each 500 ms cycle (`EMERGENCY_PATTERN 0` gives a plain blink).
- Q7: durations are red 5 s, green 5 s, blue 2 s.
- Q14: the four messages repeat in a loop.
- Q15: slow beep is 200 ms on / 500 ms off, rapid beep is 100 ms on / 100 ms off.
- Q18: if motion is still present after the 5 s alarm, the alarm sounds again.

## Verification status

- All 20 sketches compile for Arduino UNO with arduino-cli (`arduino:avr` 1.8.8).
- Every sketch's pins were cross-checked against its diagram.
- The circuits have not yet been run in the Tinkercad simulator.
