#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1   // Reset pin # (or -1 if sharing Arduino reset pin)

String task = "";
String gpuModel = "";
String cpuModel = "";
String receivedMessage = "";
int messageCounter = 0;

Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup()   
{
  Serial.begin(9600);

  display.begin(0x3C, true);
  display.display();
  display.clearDisplay();
  delay(1000);

  display.setTextSize(1);       
  display.setTextColor(SH110X_WHITE); 
  display.setCursor(10, 32);          
  display.println("Oczekiwanie na dane");
  display.display(); 

  // Wait for data from the serial port
  unsigned long startTime = millis();
  while (millis() - startTime < 5000) // Wait up to 5 seconds
  {
    if (Serial.available())
    {
      char incomingChar = Serial.read(); // Read a character from the serial buffer
      if (incomingChar == '\n') 
      {
        // Process and store the message
        int commaIndex = receivedMessage.indexOf(',');
        if (commaIndex != -1) 
        {
          cpuModel = receivedMessage.substring(0, commaIndex);
          gpuModel = receivedMessage.substring(commaIndex + 1);

          display.clearDisplay();
          display.setTextSize(1); // Set text size
          display.setCursor(16, 32);
          display.setTextSize(1); // Set text size
          display.setTextColor(SH110X_WHITE); // Set text color (white)
          display.println("Polaczono z PC!");
          display.display();
          break;
        } 
        else 
        {
          // Display an error message if no comma is found
          display.clearDisplay();
          display.setCursor(0, 0);
          display.println("Invalid data");
          display.display();
        }
        receivedMessage = ""; // Clear the message buffer
        break;
      } 
      else 
      {
        // Append the character to the received message
        receivedMessage += incomingChar;
      }
    }
  }
}

void loop() 
{
  static String receivedMessage = ""; // Store received text outside of loop
  while (Serial.available()) 
  {
    char incomingChar = Serial.read(); // Read a character from the serial buffer
    if (incomingChar == '\n') 
    {
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
        display.println(cpuModel);
        display.setTextSize(2);
        display.setCursor(64, 16);
        display.println(tempCpu + (char)247 + "C");

        display.setTextSize(1);
        display.setCursor(0, 36); // Move cursor down for next line
        display.println(gpuModel);
        display.setTextSize(2);
        display.setCursor(64, 48); // Move cursor down for next line
        display.println(tempGpu + (char)247 + "C");
      } else {
        // Display an error message if no comma is found
        display.println("Invalid data");
      }

      display.display();
      receivedMessage = ""; // Clear the message buffer
    }
     
     else 
     {
      // Append the character to the received message
      receivedMessage += incomingChar;
    }
  }
}


