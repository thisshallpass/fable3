# Shared pin-mapping specification (Q1–Q20)

Single source of truth for BOTH the firmware and the circuit diagrams.
Board: Arduino UNO R3 in Tinkercad Circuits. Do not deviate from any pin, value or filename below.

## Global conventions

- Every plain LED: Arduino pin -> 220 Ω resistor -> LED anode (long leg); LED cathode (short leg) -> GND.
- Push button: one leg -> Arduino pin, diagonally opposite leg -> GND. No external resistor; code uses `INPUT_PULLUP`, so pressed = LOW (active-low).
- RGB LED: COMMON CATHODE (the Tinkercad default). Tinkercad leg order left-to-right: Red, Cathode, Blue, Green. One 220 Ω resistor per colour leg; cathode -> GND. HIGH = colour on.
- Potentiometer: 10 kΩ. Terminal 1 -> 5V, wiper (middle) -> A0, terminal 2 -> GND.
- Buzzer: Tinkercad piezo. Positive (+) -> Arduino pin, negative -> GND. Driven with `tone(pin, 1000)` / `noTone(pin)`.
- HC-SR04 (Tinkercad "Ultrasonic Distance Sensor (4-pin)"): VCC -> 5V, TRIG -> D9, ECHO -> D10, GND -> GND.
  distance_cm = pulseIn(ECHO, HIGH, 30000) * 0.0343 / 2. A reading of 0 (timeout / no echo) means "nothing in range".
- PIR sensor (Tinkercad leg order left-to-right: Signal, Power, Ground): Signal -> D2, Power -> 5V, Ground -> GND. HIGH = motion.
- TMP36 (flat face toward viewer, left-to-right: Power, Vout, GND): Power -> 5V, Vout -> A0, GND -> GND.
  voltage = reading * 5.0 / 1024.0 ; tempC = (voltage - 0.5) * 100.0
- LCD 16x2 (HD44780, 4-bit mode), `LiquidCrystal lcd(12, 11, 5, 4, 3, 2);`
  | LCD pin | Connects to |
  |---|---|
  | 1 VSS (GND) | GND |
  | 2 VDD (VCC) | 5V |
  | 3 V0 (contrast) | wiper of 10 kΩ potentiometer (pot ends: 5V and GND) |
  | 4 RS | D12 |
  | 5 RW | GND |
  | 6 E | D11 |
  | 7–10 DB0–DB3 | not connected |
  | 11 DB4 | D5 |
  | 12 DB5 | D4 |
  | 13 DB6 | D3 |
  | 14 DB7 | D2 |
  | 15 LED anode (A) | 5V through 220 Ω |
  | 16 LED cathode (K) | GND |
- Personal details are editable placeholders: `STUDENT_NAME "Your Name"`, `ROLL_NUMBER "Roll No: 00"`, `COLLEGE_NAME "AIEC - E&TC Dept"`, `PRACTICAL_NO "Practical No: 14"` (each must fit 16 characters).

## Per-question table

| Q | Filename stem | Components | Pins | Required behaviour |
|---|---|---|---|---|
| 1 | Q01_Automatic_Corridor_Light | LED, 220 Ω | LED D13 | ON 2 s, OFF 1 s, forever |
| 2 | Q02_Emergency_Warning_Indicator | LED, 220 Ω | LED D13 | One blink cycle every 500 ms. `#define EMERGENCY_PATTERN 1` (default): emergency double-flash strobe inside each 500 ms cycle = ON 100, OFF 100, ON 100, OFF 200 ms. `0` = plain blink ON 250 / OFF 250 ms. Assumption documented in sketch. |
| 3 | Q03_Railway_Platform_Indicator | LED, 220 Ω | LED D13 | 3 quick flashes (ON 150 ms / OFF 150 ms each), then 2 s pause with LED off, repeat |
| 4 | Q04_Classroom_Light_Control | LED, 220 Ω, push button | LED D13, button D2 | LED ON while pressed, OFF when released |
| 5 | Q05_Security_Door_Indicator | LED, 220 Ω, push button (door sensor) | LED D13, button D2 | Switch active (pressed, LOW) = door open = LED ON; inactive = LED OFF |
| 6 | Q06_Toggle_Based_Lamp_Control | LED, 220 Ω, push button | LED D13, button D2 | Each press toggles LED (1st ON, 2nd OFF, ...). Act on the press edge, 50 ms debounce. LED starts OFF. |
| 7 | Q07_Traffic_Signal_Status_Indicator | RGB LED (common cathode), 3 × 220 Ω | R D11, G D10, B D9 | RED (STOP) 5 s -> GREEN (GO) 5 s -> BLUE (WAIT/CAUTION) 2 s -> repeat. Durations are editable constants (question says "a specified duration"; values are our assumption). |
| 8 | Q08_Mood_Lighting_System | RGB LED (common cathode), 3 × 220 Ω | R D11, G D10, B D9 | red, green, blue, yellow (R+G), cyan (G+B), magenta (R+B); 1 s each; repeat |
| 9 | Q09_Variable_Brightness_Controller | 10 kΩ pot, LED, 220 Ω | pot wiper A0, LED D9 (PWM) | brightness = map(analogRead(A0), 0, 1023, 0, 255) via analogWrite |
| 10 | Q10_Over_Voltage_Warning_System | 10 kΩ pot, LED, 220 Ω | pot wiper A0, LED D13 | voltage = reading * 5.0 / 1023.0; LED ON if voltage > 2.5 V, else OFF |
| 11 | Q11_Three_Level_Voltage_Indicator | 10 kΩ pot, green/yellow/red LEDs, 3 × 220 Ω | pot wiper A0, GREEN D2, YELLOW D3, RED D4 | < 1.5 V green only; 1.5 V to 3.5 V inclusive yellow only; > 3.5 V red only |
| 12 | Q12_Student_Identification_Display | LCD 16x2, 10 kΩ pot, 220 Ω | LCD as above | Line 1 = name, line 2 = roll number (static) |
| 13 | Q13_Digital_Welcome_System | LCD 16x2, 10 kΩ pot, 220 Ω | LCD as above | Power-up: "WELCOME TO AIEC" / "ARDUINO LAB"; after 3 s clear and show name / roll number, which then stays |
| 14 | Q14_Mini_Information_Display | LCD 16x2, 10 kΩ pot, 220 Ω | LCD as above | Show, one at a time, 2 s each: college/department, student name, roll number, practical number; then repeat (looping is our assumption) |
| 15 | Q15_Smart_Parking_Alert | HC-SR04, piezo buzzer | TRIG D9, ECHO D10, buzzer D8 | d > 50 cm (or no echo): OFF. 20 cm <= d <= 50 cm: slow beep (ON 200 ms / OFF 500 ms). d < 20 cm: rapid beep (ON 100 ms / OFF 100 ms) |
| 16 | Q16_Obstacle_Detection_System | HC-SR04, piezo buzzer | TRIG D9, ECHO D10, buzzer D8 | Buzzer ON while 0 < d <= 15 cm ("within 15 cm"), else OFF |
| 17 | Q17_Water_Tank_Level_Warning | HC-SR04, piezo buzzer | TRIG D9, ECHO D10, buzzer D8 | Buzzer ON while 0 < d < 10 cm (tank nearly full), else OFF |
| 18 | Q18_Motion_Based_Security_Alarm | PIR sensor, piezo buzzer | PIR signal D2, buzzer D8 | Motion (HIGH): buzzer ON for 5 s then OFF. No motion: OFF |
| 19 | Q19_Smart_Entry_Alert | PIR sensor, piezo buzzer, LED, 220 Ω | PIR signal D2, buzzer D8, LED D13 | While motion detected: LED ON and buzzer ON. No motion: both OFF |
| 20 | Q20_Temperature_Monitoring_System | TMP36 | Vout A0 | Serial 9600 baud. Every 1 s print `Temperature: xx.xx C`. If tempC > 35.0 also print `HIGH TEMPERATURE ALERT` |
