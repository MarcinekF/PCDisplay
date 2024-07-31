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
  static String inputText = ""; // Przechowuj tekst poza funkcją loop

  while (Serial.available()) {
    char c = Serial.read(); // Odczytaj pojedynczy znak

    if (c == '\n' || c == '\r') {
      // Koniec wiersza - przetwórz zgromadzony tekst
      if (inputText.length() > 0) {
        Serial.println("Received: " + inputText); // Debugowanie

        // Wyczyść bufor wyświetlacza
        display.clearDisplay();
        
        // Ustaw kursor i wyświetl tekst
        display.setCursor(0, 0);
        display.print(inputText);
        display.display();
        
        // Wyczyść zgromadzony tekst po wyświetleniu
        inputText = "";
      }
    } else {
      // Dodaj znak do zgromadzonego tekstu
      inputText += c;
    }
  }
}

