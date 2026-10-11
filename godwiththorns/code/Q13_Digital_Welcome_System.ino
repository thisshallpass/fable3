/*
  Q13 - Digital Welcome System

  Problem:
    On power-up a 16x2 LCD must show a welcome message, and after
    3 seconds replace it with the student's name and roll number.

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
    Power-up: "WELCOME TO AIEC" / "ARDUINO LAB".
    After 3 s the screen clears and shows name / roll number,
    which then stays.

  Assumptions:
    Name and roll number are placeholders; edit them below.
    Each string must be 16 characters or fewer.
*/

#include <LiquidCrystal.h>

#define WELCOME_LINE_1 "WELCOME TO AIEC"
#define WELCOME_LINE_2 "ARDUINO LAB"
#define STUDENT_NAME   "Your Name"
#define ROLL_NUMBER    "Roll No: 00"

const unsigned long WELCOME_TIME_MS = 3000;

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);   // RS, E, DB4, DB5, DB6, DB7

void setup() {
  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print(WELCOME_LINE_1);
  lcd.setCursor(0, 1);
  lcd.print(WELCOME_LINE_2);

  delay(WELCOME_TIME_MS);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(STUDENT_NAME);
  lcd.setCursor(0, 1);
  lcd.print(ROLL_NUMBER);
}

void loop() {
  // Nothing to do: name and roll number stay on the display.
}
