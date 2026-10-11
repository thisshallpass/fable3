/*
  Q6 - Toggle Based Lamp Control

  Problem:
    One push button controls a lamp (LED): the first press turns it ON,
    the next press turns it OFF, and so on.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor
    - 1 x push button (no external resistor)

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND
    D2  -> push button -> GND (diagonally opposite leg)

  Expected behaviour:
    LED starts OFF. Each press toggles it (1st press ON, 2nd OFF, ...).
    Holding the button does not toggle again.

  Assumptions:
    Internal pull-up is used (pressed = LOW). The toggle happens on the
    press edge, with a 50 ms debounce.
*/

const int LED_PIN    = 13;
const int BUTTON_PIN = 2;

const unsigned long DEBOUNCE_MS = 50;

bool ledOn = false;
int lastButtonState = HIGH;   // HIGH = released

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  int buttonState = digitalRead(BUTTON_PIN);

  if (buttonState != lastButtonState) {
    delay(DEBOUNCE_MS);                     // wait for contact bounce to settle
    buttonState = digitalRead(BUTTON_PIN);

    if (buttonState != lastButtonState) {   // change is real, not bounce
      if (buttonState == LOW) {             // press edge only
        ledOn = !ledOn;
        digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
      }
      lastButtonState = buttonState;
    }
  }
}
