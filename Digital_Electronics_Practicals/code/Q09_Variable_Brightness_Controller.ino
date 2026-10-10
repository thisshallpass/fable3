/*
  Q9 - Variable Brightness Controller

  Problem:
    The brightness of an LED must follow the position of a
    potentiometer knob.

  Components:
    - Arduino UNO R3
    - 1 x 10 k ohm potentiometer
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    Potentiometer: terminal 1 -> 5V, wiper (middle) -> A0, terminal 2 -> GND
    D9 (PWM) -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    Turning the knob from one end to the other changes the LED smoothly
    from fully OFF to full brightness.

  Assumptions:
    None.
*/

const int POT_PIN = A0;
const int LED_PIN = 9;   // PWM pin

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int reading = analogRead(POT_PIN);                  // 0..1023
  int brightness = map(reading, 0, 1023, 0, 255);     // scale to PWM range
  analogWrite(LED_PIN, brightness);
}
