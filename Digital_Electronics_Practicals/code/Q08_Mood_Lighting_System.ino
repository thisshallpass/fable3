/*
  Q8 - Mood Lighting System

  Problem:
    An RGB LED must cycle through several colours, one after another,
    to create a mood lighting effect.

  Components:
    - Arduino UNO R3
    - 1 x RGB LED (common cathode)
    - 3 x 220 ohm resistor (one per colour leg)

  Pin mapping:
    D11 -> 220 ohm -> Red leg
    D10 -> 220 ohm -> Green leg
    D9  -> 220 ohm -> Blue leg
    Cathode -> GND

  Expected behaviour:
    red, green, blue, yellow (R+G), cyan (G+B), magenta (R+B),
    1 s each, then repeat.

  Assumptions:
    Common-cathode RGB LED, so HIGH = colour on. The colour list and
    the 1 s hold time are our choice; the hold time is editable.
*/

const int RED_PIN   = 11;
const int GREEN_PIN = 10;
const int BLUE_PIN  = 9;

const unsigned long COLOUR_TIME_MS = 1000;

void showColour(int red, int green, int blue) {
  digitalWrite(RED_PIN, red);
  digitalWrite(GREEN_PIN, green);
  digitalWrite(BLUE_PIN, blue);
  delay(COLOUR_TIME_MS);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  showColour(HIGH, LOW,  LOW);    // red
  showColour(LOW,  HIGH, LOW);    // green
  showColour(LOW,  LOW,  HIGH);   // blue
  showColour(HIGH, HIGH, LOW);    // yellow
  showColour(LOW,  HIGH, HIGH);   // cyan
  showColour(HIGH, LOW,  HIGH);   // magenta
}
