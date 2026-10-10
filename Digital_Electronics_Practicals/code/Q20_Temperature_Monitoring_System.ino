/*
  Q20 - Temperature Monitoring System

  Problem:
    A TMP36 sensor measures temperature. The reading must be shown on
    the Serial Monitor, with an alert when it goes above 35 degrees C.

  Components:
    - Arduino UNO R3
    - 1 x TMP36 temperature sensor

  Pin mapping:
    TMP36 (flat face toward viewer, left to right):
      Power -> 5V, Vout -> A0, GND -> GND

  Expected behaviour:
    Every 1 s the Serial Monitor (9600 baud) prints
      Temperature: xx.xx C
    and, if the temperature is above 35.0 C, also prints
      HIGH TEMPERATURE ALERT

  Assumptions:
    voltage = reading * 5.0 / 1024.0 ; tempC = (voltage - 0.5) * 100.0
*/

const int SENSOR_PIN = A0;

const float ALERT_TEMP_C = 35.0;
const unsigned long READ_INTERVAL_MS = 1000;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(SENSOR_PIN);
  float voltage = reading * 5.0 / 1024.0;
  float tempC = (voltage - 0.5) * 100.0;   // TMP36: 10 mV per degree, 0.5 V offset

  Serial.print("Temperature: ");
  Serial.print(tempC, 2);
  Serial.println(" C");

  if (tempC > ALERT_TEMP_C) {
    Serial.println("HIGH TEMPERATURE ALERT");
  }

  delay(READ_INTERVAL_MS);
}
