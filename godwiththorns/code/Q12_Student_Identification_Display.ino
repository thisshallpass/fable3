/*
  Q12 - Student Identification Display

  Problem:
    Show the student's name on the first line of a 16x2 LCD and the
    roll number on the second line.

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
    Line 1 shows the name, line 2 shows the roll number. Static.

  Assumptions:
    Name and roll number are placeholders; edit them below.
    Each string must be 16 characters or fewer.
*/

#include <LiquidCrystal.h>

#define STUDENT_NAME "Your Name"
#define ROLL_NUMBER  "Roll No: 00"

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);   // RS, E, DB4, DB5, DB6, DB7

void setup() {
  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print(STUDENT_NAME);

  lcd.setCursor(0, 1);
  lcd.print(ROLL_NUMBER);
}

void loop() {
  // Nothing to do: the display is static.
}
