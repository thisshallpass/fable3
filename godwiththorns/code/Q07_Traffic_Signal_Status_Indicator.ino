/*
  Q7 - Traffic Signal Status Indicator

  Problem:
    An RGB LED shows traffic signal status: RED for STOP, GREEN for GO
    and BLUE for WAIT/CAUTION, each for a specified duration, repeating.

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
    RED 5 s -> GREEN 5 s -> BLUE 2 s -> repeat.

  Assumptions:
    The question says "a specified duration" without giving values;
    5 s / 5 s / 2 s are our assumption and are editable below.
    Common-cathode RGB LED, so HIGH = colour on.
*/

const int RED_PIN   = 11;
const int GREEN_PIN = 10;
const int BLUE_PIN  = 9;

const unsigned long STOP_TIME_MS = 5000;   // RED
const unsigned long GO_TIME_MS   = 5000;   // GREEN
const unsigned long WAIT_TIME_MS = 2000;   // BLUE

void setColour(int red, int green, int blue) {
  digitalWrite(RED_PIN, red);
  digitalWrite(GREEN_PIN, green);
  digitalWrite(BLUE_PIN, blue);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  setColour(HIGH, LOW, LOW);    // STOP
  delay(STOP_TIME_MS);

  setColour(LOW, HIGH, LOW);    // GO
  delay(GO_TIME_MS);

  setColour(LOW, LOW, HIGH);    // WAIT / CAUTION
  delay(WAIT_TIME_MS);
}
