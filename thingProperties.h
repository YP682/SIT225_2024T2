#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "arduino_secrets.h"

const char SSID[] = SECRET_SSID;    
const char PASS[] = SECRET_OPTIONAL_PASS;  

// Declare cloud variables
float acceleration_magnitude;  // Combined variable for acceleration magnitude
bool alarm_triggered;
bool reset_alarm;
float alarm_severity;  

void onResetAlarmChange();  // Declare the reset function

void initProperties() {
  // Add cloud properties and assign them to variables
  ArduinoCloud.addProperty(acceleration_magnitude, READ, ON_CHANGE, NULL);  // Combined acceleration magnitude
  ArduinoCloud.addProperty(alarm_triggered, READWRITE, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(reset_alarm, READWRITE, ON_CHANGE, onResetAlarmChange);  // Reset button callback
  ArduinoCloud.addProperty(alarm_severity, READ, ON_CHANGE, NULL);  // Alarm severity property
}

// Wi-Fi connection handler
WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

// Function to handle reset_alarm changes
void onResetAlarmChange() {
  if (reset_alarm) {
    alarm_triggered = false;  // Manually reset the alarm
    reset_alarm = false;      // Reset the button state
    alarm_severity = 0;       // Reset the severity
  }
}

