/*
  Q18 - Motion Based Security Alarm

  Problem:
    A PIR sensor detects motion. When motion is detected a buzzer must
    sound for 5 seconds and then switch off.

  Components:
    - Arduino UNO R3
    - 1 x PIR sensor
    - 1 x piezo buzzer

  Pin mapping:
    PIR:    Signal -> D2, Power -> 5V, Ground -> GND
    Buzzer: positive (+) -> D8, negative -> GND

  Expected behaviour:
    Motion (PIR HIGH) -> buzzer ON for 5 s, then OFF
    No motion         -> buzzer OFF

  Assumptions:
    If motion is still present after the 5 s, the alarm sounds again.
*/

const int PIR_PIN    = 2;
const int BUZZER_PIN = 8;

const unsigned int  BUZZER_FREQ_HZ = 1000;
const unsigned long ALARM_TIME_MS  = 5000;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(PIR_PIN) == HIGH) {   // HIGH = motion
    tone(BUZZER_PIN, BUZZER_FREQ_HZ);
    delay(ALARM_TIME_MS);
    noTone(BUZZER_PIN);
  } else {
    noTone(BUZZER_PIN);
  }
}
