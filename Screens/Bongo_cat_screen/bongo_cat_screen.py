from kivy.uix.screenmanager import Screen
import time

class BongoCatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.current = 'main_screen'

    def start_bongo(self):
        self.manager.monitoring = False
        if self.manager.ser and self.manager.ser.is_open:
            try:
                self.manager.ser.write("Stop\n".encode())
                time.sleep(0.2)
                self.manager.ser.write("Bongo\n".encode())
                time.sleep(0.2)
            except Exception as e:
                print(f"Error sending data: {e}")