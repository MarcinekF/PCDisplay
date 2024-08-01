from kivy.uix.screenmanager import Screen
import serial

class MainScreen(Screen):
    def go_to_settings_screen(self):
        self.manager.current = 'settings_screen'

    def go_to_temperature_screen(self):
        self.manager.current = 'temperature_screen'

    def connect_with_board(self):
        self.monitoring = False
        self.c = None

        try:
            self.manager.ser = serial.Serial('COM4', 9600, timeout=1)
            self.ids.connection_status.text = "Polaczono"
            self.ids.connect_button.parent.remove_widget(self.ids.connect_button)
            self.ids.connection_status.color = (0, 1, 0, 1)  # Kolor zielony
        except serial.SerialException as e:
            self.ids.connection_status.text = "Nie moge polaczyc sie z plytka"
            self.ser = None