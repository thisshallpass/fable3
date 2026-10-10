/*
  Q15 - Smart Parking Alert

  Problem:
    An ultrasonic sensor measures the distance to an obstacle while
    parking. A buzzer beeps slowly when the obstacle is near and
    rapidly when it is very close.

  Components:
    - Arduino UNO R3
    - 1 x HC-SR04 ultrasonic distance sensor (4-pin)
    - 1 x piezo buzzer

  Pin mapping:
    HC-SR04: VCC -> 5V, TRIG -> D9, ECHO -> D10, GND -> GND
    Buzzer:  positive (+) -> D8, negative -> GND

  Expected behaviour:
    distance > 50 cm (or no echo)  -> buzzer OFF
    20 cm <= distance <= 50 cm     -> slow beep (ON 200 ms / OFF 500 ms)
    distance < 20 cm               -> rapid beep (ON 100 ms / OFF 100 ms)

  Assumptions:
    distance_cm = pulseIn(ECHO, HIGH, 30000) * 0.0343 / 2.
    A reading of 0 (timeout) means nothing is in range.
    The 20 cm / 50 cm zones come from the question; the beep timings
    (and treating exactly 20 cm and 50 cm as "slow") are our choice.
*/

const int TRIG_PIN   = 9;
const int ECHO_PIN   = 10;
const int BUZZER_PIN = 8;

const unsigned int  BUZZER_FREQ_HZ  = 1000;
const unsigned long ECHO_TIMEOUT_US = 30000;

const float FAR_LIMIT_CM  = 50.0;
const float NEAR_LIMIT_CM = 20.0;

const unsigned long SLOW_ON_MS   = 200;
const unsigned long SLOW_OFF_MS  = 500;
const unsigned long RAPID_ON_MS  = 100;
const unsigned long RAPID_OFF_MS = 100;
const unsigned long IDLE_DELAY_MS = 100;   // gap between readings when silent

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);            // 10 us trigger pulse
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  return duration * 0.0343 / 2;            // 0 if no echo
}

void beep(unsigned long onMs, unsigned long offMs) {
  tone(BUZZER_PIN, BUZZER_FREQ_HZ);
  delay(onMs);
  noTone(BUZZER_PIN);
  delay(offMs);
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  float distance = readDistanceCm();

  if (distance == 0 || distance > FAR_LIMIT_CM) {
    noTone(BUZZER_PIN);                    // nothing in range
    delay(IDLE_DELAY_MS);
  } else if (distance >= NEAR_LIMIT_CM) {
    beep(SLOW_ON_MS, SLOW_OFF_MS);         // 20 cm to 50 cm
  } else {
    beep(RAPID_ON_MS, RAPID_OFF_MS);       // closer than 20 cm
  }
}
