/*
  Q5 - Security Door Indicator

  Problem:
    A switch acts as a door sensor. An indicator LED must be ON when
    the door is open and OFF when the door is closed.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor
    - 1 x push button used as the door sensor (no external resistor)

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND
    D2  -> push button (door sensor) -> GND (diagonally opposite leg)

  Expected behaviour:
    Switch active (pressed)    = door open   -> LED ON
    Switch inactive (released) = door closed -> LED OFF

  Assumptions:
    A pressed switch (LOW, because of the internal pull-up) represents
    an open door.
*/

const int LED_PIN         = 13;
const int DOOR_SENSOR_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);
}

void loop() {
  bool doorOpen = (digitalRead(DOOR_SENSOR_PIN) == LOW);   // LOW = switch active

  if (doorOpen) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
