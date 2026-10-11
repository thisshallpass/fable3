/*
  Q10 - Over Voltage Warning System

  Problem:
    A potentiometer simulates a varying voltage. A warning LED must
    turn ON when the voltage goes above 2.5 V.

  Components:
    - Arduino UNO R3
    - 1 x 10 k ohm potentiometer
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    Potentiometer: terminal 1 -> 5V, wiper (middle) -> A0, terminal 2 -> GND
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    voltage > 2.5 V  -> LED ON
    voltage <= 2.5 V -> LED OFF

  Assumptions:
    voltage = reading * 5.0 / 1023.0 (5 V reference).
*/

const int POT_PIN = A0;
const int LED_PIN = 13;

const float VOLTAGE_LIMIT = 2.5;   // volts

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int reading = analogRead(POT_PIN);
  float voltage = reading * 5.0 / 1023.0;

  if (voltage > VOLTAGE_LIMIT) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
