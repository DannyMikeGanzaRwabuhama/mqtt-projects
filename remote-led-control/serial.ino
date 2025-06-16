// Define the LED pin
const int ledPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  Serial.println("Arduino ready. Send 'ON' or 'OFF' via serial to control the LED.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    // Remove any leading or trailing whitespace
    command.trim();

    // Convert the command to uppercase for case-insensitive comparison
    command.toUpperCase();

    // Check the received command
    if (command == "ON") {
      digitalWrite(ledPin, HIGH); // Turn the LED on
      Serial.println("LED is ON");
    } else if (command == "OFF") {
      digitalWrite(ledPin, LOW);  // Turn the LED off
      Serial.println("LED is OFF");
    } else {
      Serial.print("Unknown command: ");
      Serial.println(command);
    }
  }
}