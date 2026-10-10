/*
  Q3 - Railway Platform Indicator

  Problem:
    A platform indicator LED must give three quick flashes, pause for
    2 seconds, and then repeat the pattern.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    3 flashes (ON 150 ms / OFF 150 ms each), then LED stays OFF for
    2 s, then the pattern repeats.

  Assumptions:
    The 150 ms flash timing is our choice for "quick"; it is editable.
*/

const int LED_PIN = 13;

const int FLASH_COUNT = 3;
const unsigned long FLASH_ON_MS  = 150;
const unsigned long FLASH_OFF_MS = 150;
const unsigned long PAUSE_MS     = 2000;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  for (int i = 0; i < FLASH_COUNT; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(FLASH_ON_MS);
    digitalWrite(LED_PIN, LOW);
    delay(FLASH_OFF_MS);
  }
  delay(PAUSE_MS);   // LED is already OFF here
}
