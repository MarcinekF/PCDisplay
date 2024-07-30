const int controlPin = 9; // Pin, który chcesz ustawić na wysoki stan
const String triggerMessage = "Liza kwiatuszek"; // Oczekiwana wiadomość
String receivedMessage = "";

void setup() {
  Serial.begin(9600); // Inicjalizacja komunikacji szeregowej
  pinMode(controlPin, OUTPUT); // Ustawienie pinu jako wyjście
  digitalWrite(controlPin, LOW); // Ustawienie pinu na niski stan na początku
}

void loop() {
  // Sprawdzenie, czy dostępne są dane w porcie szeregowym
  while (Serial.available()) {
    char incomingChar = Serial.read();
    receivedMessage += incomingChar;
    
    // Jeśli otrzymano pełną wiadomość
    if (incomingChar == '\n') {
      receivedMessage.trim(); // Usunięcie zbędnych białych znaków
      
      // Sprawdzenie, czy wiadomość pasuje do oczekiwanej
      if (receivedMessage == triggerMessage) {
        digitalWrite(controlPin, HIGH); // Ustawienie pinu 9 na wysoki stan
        delay(1000); // Utrzymanie stanu wysokiego przez 1 sekundę
        digitalWrite(controlPin, LOW); // Ustawienie pinu 9 na niski stan
      }
      
      // Resetowanie wiadomości
      receivedMessage = "";
    }
  }
}
