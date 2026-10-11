/*
  Q19 - Smart Entry Alert

  Problem:
    A PIR sensor at an entrance detects a person. While motion is
    detected both an LED and a buzzer must be ON.

  Components:
    - Arduino UNO R3
    - 1 x PIR sensor
    - 1 x piezo buzzer
    - 1 x LED
    - 1 x 220 ohm resistor

  Pin mapping:
    PIR:    Signal -> D2, Power -> 5V, Ground -> GND
    Buzzer: positive (+) -> D8, negative -> GND
    D13 -> 220 ohm -> LED anode (long leg), LED cathode -> GND

  Expected behaviour:
    Motion (PIR HIGH) -> LED ON and buzzer ON
    No motion         -> LED OFF and buzzer OFF

  Assumptions:
    None.
*/

const int PIR_PIN    = 2;
const int BUZZER_PIN = 8;
const int LED_PIN    = 13;

const unsigned int BUZZER_FREQ_HZ = 1000;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(PIR_PIN) == HIGH) {   // HIGH = motion
    digitalWrite(LED_PIN, HIGH);
    tone(BUZZER_PIN, BUZZER_FREQ_HZ);
  } else {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
  }
}
