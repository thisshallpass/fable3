/*
  Q16 - Obstacle Detection System

  Problem:
    An ultrasonic sensor watches for obstacles. A buzzer must sound
    when an obstacle is within 15 cm.

  Components:
    - Arduino UNO R3
    - 1 x HC-SR04 ultrasonic distance sensor (4-pin)
    - 1 x piezo buzzer

  Pin mapping:
    HC-SR04: VCC -> 5V, TRIG -> D9, ECHO -> D10, GND -> GND
    Buzzer:  positive (+) -> D8, negative -> GND

  Expected behaviour:
    0 < distance <= 15 cm -> buzzer ON
    otherwise             -> buzzer OFF

  Assumptions:
    distance_cm = pulseIn(ECHO, HIGH, 30000) * 0.0343 / 2.
    A reading of 0 (timeout) means nothing is in range.
    "Within 15 cm" includes exactly 15 cm.
*/

const int TRIG_PIN   = 9;
const int ECHO_PIN   = 10;
const int BUZZER_PIN = 8;

const unsigned int  BUZZER_FREQ_HZ  = 1000;
const unsigned long ECHO_TIMEOUT_US = 30000;
const unsigned long READ_DELAY_MS   = 100;   // gap between readings

const float OBSTACLE_LIMIT_CM = 15.0;

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);              // 10 us trigger pulse
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  return duration * 0.0343 / 2;              // 0 if no echo
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  float distance = readDistanceCm();

  if (distance > 0 && distance <= OBSTACLE_LIMIT_CM) {
    tone(BUZZER_PIN, BUZZER_FREQ_HZ);
  } else {
    noTone(BUZZER_PIN);
  }

  delay(READ_DELAY_MS);
}
