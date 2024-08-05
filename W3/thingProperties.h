#include <ArduinoIoTCloud.h>  // LIBRARY NEEDS TO BE INSTALLED
#include <Arduino_ConnectionHandler.h>  // LIBRARY NEEDS TO BE INSTALLED
// Additional LIBRARY: ArduinoHttpClient
#include "arduino_secrets.h"

const char SSID[]     = SECRET_SSID;    // Network SSID (name)
const char PASS[]     = SECRET_OPTIONAL_PASS;    // Network password (use for WPA, or use as key for WEP)

void onRandomTemperatureChange();

float randomTemperature;

void initProperties(){
  ArduinoCloud.addProperty(randomTemperature, READWRITE, ON_CHANGE, onRandomTemperatureChange);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);