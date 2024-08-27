#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>  
#include "arduino_secrets.h"

const float THRESHOLD = 2.5;  // Threshold for alarm (in g's)
const int CONSECUTIVE_SAMPLES = 5;  // Number of consecutive samples above threshold to trigger alarm
const int SAMPLES = 50;  // Buffer for acceleration samples

float accelMagnitude[SAMPLES];
int sampleIndex = 0;

void setup() {
  // Start serial communication
  Serial.begin(9600);
  while (!Serial);

  // Initialize cloud properties and connect to IoT Cloud
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  // Initialize the IMU sensor (LSM6DS3)
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Initialize variables
  alarm_triggered = false;
  reset_alarm = false;
  alarm_severity = 0;

  setDebugMessageLevel(2);  // Enable debug messages
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();  // Update the cloud with latest data

  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    
    // Calculate magnitude of acceleration
    float magnitude = sqrt(x * x + y * y + z * z);
    
    // Update cloud variable with the acceleration magnitude
    acceleration_magnitude = magnitude;

    // Store magnitude in circular buffer
    accelMagnitude[sampleIndex] = magnitude;
    sampleIndex = (sampleIndex + 1) % SAMPLES;

    // Check for alarm condition
    int highMagSamples = 0;
    for (int i = 0; i < SAMPLES; i++) {
      if (accelMagnitude[i] > THRESHOLD) {
        highMagSamples++;
        if (highMagSamples >= CONSECUTIVE_SAMPLES && alarm_triggered == false) {
          // Trigger the alarm and calculate severity
          alarm_triggered = true;
          alarm_severity = 100 * (magnitude - THRESHOLD) / (THRESHOLD * 2);  // Calculate severity as a percentage
          if (alarm_severity > 100) alarm_severity = 100;  // Cap the severity at 100%
          break;  // Once triggered, don't reset it
        }
      } else {
        highMagSamples = 0;
      }
    }
  }

  if (reset_alarm) {
    alarm_triggered = false;  // Reset the alarm
    reset_alarm = false;  // Reset the button
    alarm_severity = 0;  // Reset the severity
  }

  delay(10);  // Control the sampling rate (~100Hz)
}
