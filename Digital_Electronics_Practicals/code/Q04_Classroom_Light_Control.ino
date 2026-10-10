/*
  Q4 - Classroom Light Control

  Problem:
    A classroom light (LED) must be ON only while a push button is
    held down, and OFF when the button is released.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor
    - 1 x push button (no external resistor)

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND
    D2  -> push button -> GND (diagonally opposite leg)

  Expected behaviour:
    Button pressed  -> LED ON
    Button released -> LED OFF

  Assumptions:
    Internal pull-up is used, so the button reads LOW when pressed.
*/

const int LED_PIN    = 13;
const int BUTTON_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {   // LOW = pressed
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
