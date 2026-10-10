/*
  Q1 - Automatic Corridor Light

  Problem:
    A corridor light must switch itself ON and OFF repeatedly:
    ON for 2 seconds, OFF for 1 second, forever.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    LED is ON for 2 s, then OFF for 1 s, and the cycle repeats.

  Assumptions:
    None.
*/

const int LED_PIN = 13;

const unsigned long ON_TIME_MS  = 2000;
const unsigned long OFF_TIME_MS = 1000;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(ON_TIME_MS);
  digitalWrite(LED_PIN, LOW);
  delay(OFF_TIME_MS);
}
