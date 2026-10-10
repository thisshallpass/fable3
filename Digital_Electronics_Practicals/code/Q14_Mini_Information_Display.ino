/*
  Q14 - Mini Information Display

  Problem:
    A 16x2 LCD must show college/department, student name, roll number
    and practical number one after another, 2 seconds each.

  Components:
    - Arduino UNO R3
    - 1 x LCD 16x2 (HD44780, 4-bit mode)
    - 1 x 10 k ohm potentiometer (contrast)
    - 1 x 220 ohm resistor (backlight)

  Pin mapping (LCD pin -> connection):
    1 VSS -> GND          2 VDD -> 5V
    3 V0  -> wiper of 10 k pot (pot ends: 5V and GND)
    4 RS  -> D12          5 RW  -> GND          6 E -> D11
    7-10 DB0-DB3 -> not connected
    11 DB4 -> D5   12 DB5 -> D4   13 DB6 -> D3   14 DB7 -> D2
    15 LED anode -> 5V through 220 ohm          16 LED cathode -> GND

  Expected behaviour:
    One item at a time on line 1, 2 s each:
    college/department -> name -> roll number -> practical number,
    then the sequence repeats.

  Assumptions:
    Repeating the sequence forever is our assumption.
    All four details are placeholders; edit them below.
    Each string must be 16 characters or fewer.
*/

#include <LiquidCrystal.h>

#define COLLEGE_NAME "AIEC - E&TC Dept"
#define STUDENT_NAME "Your Name"
#define ROLL_NUMBER  "Roll No: 00"
#define PRACTICAL_NO "Practical No: 14"

const unsigned long SCREEN_TIME_MS = 2000;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);   // RS, E, DB4, DB5, DB6, DB7

void showScreen(const char *text) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(text);
  delay(SCREEN_TIME_MS);
}

void setup() {
  lcd.begin(16, 2);
}

void loop() {
  showScreen(COLLEGE_NAME);
  showScreen(STUDENT_NAME);
  showScreen(ROLL_NUMBER);
  showScreen(PRACTICAL_NO);
}
