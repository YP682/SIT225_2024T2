#include <DHT.h>
#include <WiFiNINA.h>
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "arduino_secrets.h"

// Network credentials
const char SSID[] = SECRET_SSID;
const char PASS[] = SECRET_OPTIONAL_PASS;

DHT dht(2, DHT11); 

float temperature;
float humidity;

void onTemperatureChange() {
  // Function called on temperature change
}

void onHumidityChange() {
  // Function called on humidity change
}

void initProperties() {
  ArduinoCloud.addProperty(temperature, READ, ON_CHANGE, onTemperatureChange);
  ArduinoCloud.addProperty(humidity, READ, ON_CHANGE, onHumidityChange);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Initialize WiFi
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize Arduino IoT Cloud
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  delay(2000);
}

