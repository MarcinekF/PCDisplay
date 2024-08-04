import time

from kivy.uix.screenmanager import Screen
from hardware_monitor import get_computer
from hardware_monitor import get_cpu_model
from hardware_monitor import get_gpu_model
import serial

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.c = get_computer()

    def go_to_bongo_cat_screen(self):
        self.manager.current = 'bongo_cat_screen'

    def go_to_settings_screen(self):
        self.manager.current = 'settings_screen'

    def go_to_temperature_screen(self):
        self.manager.current = 'temperature_screen'

    def connect_with_board(self):
        try:
            # Inicjalizacja połączenia szeregowego
            self.manager.ser = serial.Serial('COM4', 9600, timeout=1)
            self.ids.connection_status.text = "Połączono"

            time.sleep(4)
            # Przygotowanie wiadomości do wysłania
            message = f"{get_cpu_model(self.c)},{get_gpu_model(self.c)}\n"
            self.manager.ser.write(message.encode())

            # Zaktualizuj interfejs użytkownika
            self.ids.connect_button.parent.remove_widget(self.ids.connect_button)
            self.ids.connection_status.color = (0, 1, 0, 1)  # Kolor zielony, oznacza sukces

        except serial.SerialException as e:
            # Obsługuje wyjątek, gdy nie można połączyć się z płytką
            self.ids.connection_status.text = "Nie mogę połączyć się z płytką"
            self.manager.ser = None
            # Logowanie błędu
            print(f"SerialException: {e}")