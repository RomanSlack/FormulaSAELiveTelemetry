#include <SoftwareSerial.h>

// Define pins for SoftwareSerial
SoftwareSerial loraSerial(2, 3); // RX on D2, TX on D3

unsigned long previousMillis = 0; // Stores the last time a message was sent
const long interval = 500; // Interval to wait between messages (3000 ms = 3 seconds)
int messageIndex = 0; // Track which message to send

void setup() {
  // Start hardware serial for debugging
  Serial.begin(115200);

  // Start communication with the LoRa module on SoftwareSerial
  loraSerial.begin(115200);

  // Wait for LoRa module to initialize
  delay(1000);
}

void loop() {
  // Get the current time in milliseconds
  unsigned long currentMillis = millis();

  // Check if 3 seconds have passed since the last message
  if (currentMillis - previousMillis >= interval) {
    // Save the last time the message was sent
    previousMillis = currentMillis;

    // Alternate between the three messages
    if (messageIndex == 0) {
      sendMessage("'0xd0', '0xc8', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'", 18);
    } else if (messageIndex == 1) {
      sendMessage("'0xd1', '0x4b', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'", 18);
    } else {
      sendMessage("'0xd0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0', '0x0'", 18);
    }

    // Cycle through message indices: 0, 1, 2
    messageIndex = (messageIndex + 1) % 3;
}


  // You can add other code here to run while waiting for the next message
}

void sendMessage(String message, int destinationAddress) {
  // Build the AT+SEND command string
  String atCommand = "AT+SEND=";
  atCommand += String(destinationAddress) + ",";
  atCommand += String(message.length()) + ",";
  atCommand += message;

  // Send the AT+SEND command to the LoRa module
  loraSerial.println(atCommand);

  // Wait for a response from the LoRa module
  delay(1000);

  // Check if LoRa module responds with "OK"
  if (loraSerial.available()) {
    while (loraSerial.available()) {
      Serial.write(loraSerial.read()); // Print the response to Serial Monitor
    }
  } else {
    Serial.println("No response from LoRa module");
  }
}
