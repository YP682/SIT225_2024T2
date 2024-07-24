int ledPin = 13; // Set the LED pin (e.g., built-in LED on pin 13)
int x;

void setup() {
  Serial.begin(9600);  // Set baud rate
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
}

void loop() {
  while (!Serial.available()) {} // Wait for data to arrive

  // Read string data from Serial and ignore newline/carriage return characters
  String input = Serial.readStringUntil('\n');
  x = input.toInt();
  
  // Debugging print to ensure the correct value is received
  Serial.print("Received: ");
  Serial.println(x);

  // Wait for x seconds before blinking the LED
  for (int i = 0; i < x; i++) {
    delay(1000);  // Wait for 1 second each loop iteration
  }

  // Blink the LED 'x' times
  for (int i = 0; i < x; i++) {
    digitalWrite(ledPin, HIGH);   // Turn the LED on
    delay(500);                  // Wait for half a second
    digitalWrite(ledPin, LOW);    // Turn the LED off
    delay(500);                  // Wait for half a second
  }

  // Send a random number back to Python
  int response = random(5, 10);
  Serial.println(response);  

  // Indicate that the Arduino is ready for the next command
  Serial.println("DONE");
  Serial.flush();  
}


