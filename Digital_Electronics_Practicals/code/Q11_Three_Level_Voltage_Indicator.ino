/*
  Q11 - Three Level Voltage Indicator

  Problem:
    A potentiometer simulates a varying voltage. Three LEDs show
    whether the voltage is low, medium or high.

  Components:
    - Arduino UNO R3
    - 1 x 10 k ohm potentiometer
    - 1 x green LED, 1 x yellow LED, 1 x red LED
    - 3 x 220 ohm resistor

  Pin mapping:
    Potentiometer: terminal 1 -> 5V, wiper (middle) -> A0, terminal 2 -> GND
    D2 -> 220 ohm -> GREEN LED anode,  cathode -> GND
    D3 -> 220 ohm -> YELLOW LED anode, cathode -> GND
    D4 -> 220 ohm -> RED LED anode,    cathode -> GND

  Expected behaviour:
    voltage < 1.5 V            -> green only
    1.5 V <= voltage <= 3.5 V  -> yellow only
    voltage > 3.5 V            -> red only

  Assumptions:
    voltage = reading * 5.0 / 1023.0 (5 V reference).
    The boundaries 1.5 V and 3.5 V themselves belong to the yellow band.
*/

const int POT_PIN    = A0;
const int GREEN_PIN  = 2;
const int YELLOW_PIN = 3;
const int RED_PIN    = 4;

const float LOW_LIMIT  = 1.5;   // volts
const float HIGH_LIMIT = 3.5;   // volts

void setup() {
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
}

void loop() {
  int reading = analogRead(POT_PIN);
  float voltage = reading * 5.0 / 1023.0;

  if (voltage < LOW_LIMIT) {
    digitalWrite(GREEN_PIN, HIGH);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, LOW);
  } else if (voltage <= HIGH_LIMIT) {
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(YELLOW_PIN, HIGH);
    digitalWrite(RED_PIN, LOW);
  } else {
    digitalWrite(GREEN_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(RED_PIN, HIGH);
  }
}
