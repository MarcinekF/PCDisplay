#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1   // Reset pin # (or -1 if sharing Arduino reset pin)

Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup()   
{
  Serial.begin(9600);

  display.begin(0x3C, true);
  display.display();
  display.clearDisplay();
  delay(1000);

  display.setTextSize(2);           // Set text size
  display.setTextColor(SH110X_WHITE); // Set text color (white)
  display.setCursor(0, 0);          // Set cursor to top-left corner

  // Clear the display and show a welcome message
  display.clearDisplay();
  display.setTextSize(1);           // Set text size
  display.setTextColor(SH110X_WHITE); // Set text color (white)
  display.setCursor(0, 0);          // Set cursor to top-left corner
  display.println("Send text via Serial");
  display.display(); // Update the display

}

void loop() {
  static String receivedMessage = ""; // Store received text outside of loop

  while (Serial.available()) 
  {
    char incomingChar = Serial.read(); // Read a character from the serial buffer
    if (incomingChar == '\n') {
      // If newline character received, process and display the message
      display.clearDisplay();
      display.setCursor(0, 0);
      display.setTextSize(1); // Set text size
      display.setTextColor(SH110X_WHITE); // Set text color (white)

      // Split the message based on comma
      int commaIndex = receivedMessage.indexOf(',');
      if (commaIndex != -1) {
        String tempCpu = receivedMessage.substring(0, commaIndex);
        String tempGpu = receivedMessage.substring(commaIndex + 1);
        
        // Display the numbers one below the other
        display.println("CPU Temp: " + tempCpu);
        display.setCursor(0, 16); // Move cursor down for next line
        display.println("GPU Temp: " + tempGpu);
      } else {
        // Display an error message if no comma is found
        display.println("Invalid data");
      }

      display.display();
      receivedMessage = ""; // Clear the message buffer
    } else {
      // Append the character to the received message
      receivedMessage += incomingChar;
    }
  }
}
