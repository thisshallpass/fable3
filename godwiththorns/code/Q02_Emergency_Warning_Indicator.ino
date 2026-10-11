/*
  Q2 - Emergency Warning Indicator

  Problem:
    An emergency warning LED must blink continuously with one blink
    cycle every 500 ms.

  Components:
    - Arduino UNO R3
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    EMERGENCY_PATTERN 1 (default): double-flash strobe inside each
      500 ms cycle = ON 100, OFF 100, ON 100, OFF 200 ms.
    EMERGENCY_PATTERN 0: plain blink = ON 250 ms, OFF 250 ms.

  Assumptions:
    The question only asks for a 500 ms blink cycle. The double-flash
    strobe is our assumption of what an "emergency" pattern looks like;
    set EMERGENCY_PATTERN to 0 for the plain blink.
*/

#define EMERGENCY_PATTERN 1   // 1 = double-flash strobe, 0 = plain blink

const int LED_PIN = 13;

// Double-flash strobe timings (total 500 ms)
const unsigned long FLASH_ON_MS   = 100;
const unsigned long FLASH_GAP_MS  = 100;
const unsigned long FLASH_REST_MS = 200;

// Plain blink timings (total 500 ms)
const unsigned long BLINK_ON_MS  = 250;
const unsigned long BLINK_OFF_MS = 250;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
#if EMERGENCY_PATTERN
  digitalWrite(LED_PIN, HIGH);
  delay(FLASH_ON_MS);
  digitalWrite(LED_PIN, LOW);
  delay(FLASH_GAP_MS);
  digitalWrite(LED_PIN, HIGH);
  delay(FLASH_ON_MS);
  digitalWrite(LED_PIN, LOW);
  delay(FLASH_REST_MS);
#else
  digitalWrite(LED_PIN, HIGH);
  delay(BLINK_ON_MS);
  digitalWrite(LED_PIN, LOW);
  delay(BLINK_OFF_MS);
#endif
}
