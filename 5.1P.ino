#include <Arduino_LSM6DS3.h>  // Correct library for the Nano 33 IoT

void setup() {
  Serial.begin(115200);
  while (!Serial);  // Wait for the serial connection to initialize
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("Gyroscope initialized.");
  Serial.println("Gyroscope sample rate = " + String(IMU.gyroscopeSampleRate()) + " Hz");
}

void loop() {
  float gyroX = IMU.readFloatGyroX();
  float gyroY = IMU.readFloatGyroY();
  float gyroZ = IMU.readFloatGyroZ();

  // Send gyroscope data to serial
  Serial.print("X:");
  Serial.print(gyroX);
  Serial.print(", Y:");
  Serial.print(gyroY);
  Serial.print(", Z:");
  Serial.println(gyroZ);

  delay(200);  // Increase delay to slow down the data rate (5 Hz)
}
