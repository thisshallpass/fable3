/*
  Q17 - Water Tank Level Warning

  Problem:
    An ultrasonic sensor at the top of a tank measures the distance to
    the water surface. A buzzer must warn when the tank is nearly full.

  Components:
    - Arduino UNO R3
    - 1 x HC-SR04 ultrasonic distance sensor (4-pin)
    - 1 x piezo buzzer

  Pin mapping:
    HC-SR04: VCC -> 5V, TRIG -> D9, ECHO -> D10, GND -> GND
    Buzzer:  positive (+) -> D8, negative -> GND

  Expected behaviour:
    0 < distance < 10 cm (tank nearly full) -> buzzer ON
    otherwise                               -> buzzer OFF

  Assumptions:
    distance_cm = pulseIn(ECHO, HIGH, 30000) * 0.0343 / 2.
    A reading of 0 (timeout) means nothing is in range.
    The sensor faces down from the top of the tank, so a small
    distance means a high water level.
*/

const int TRIG_PIN   = 9;
const int ECHO_PIN   = 10;
const int BUZZER_PIN = 8;

const unsigned int  BUZZER_FREQ_HZ  = 1000;
const unsigned long ECHO_TIMEOUT_US = 30000;
const unsigned long READ_DELAY_MS   = 100;   // gap between readings

const float FULL_LIMIT_CM = 10.0;

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

  if (distance > 0 && distance < FULL_LIMIT_CM) {
    tone(BUZZER_PIN, BUZZER_FREQ_HZ);
  } else {
    noTone(BUZZER_PIN);
  }

  delay(READ_DELAY_MS);
}
