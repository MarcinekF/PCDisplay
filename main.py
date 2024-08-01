from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import clr
from kivy.app import App

from Screens.Main_screen.main_screen import MainScreen
from Screens.Temperature_screen.temperature_screen import TemperatureScreen
from Screens.Settings_screen.settings_screen import SettingsScreen


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.ser = None

class PCDisplay(App):
    def build(self):

        # Load the KV files for screens
        Builder.load_file('screens/main_screen/main_screen.kv')
        Builder.load_file('screens/temperature_screen/temperature_screen.kv')
        Builder.load_file('screens/settings_screen/settings_screen.kv')

        # Initialize ScreenManager and add screens
        sm = WindowManager()
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(TemperatureScreen(name='temperature_screen'))
        sm.add_widget(SettingsScreen(name='settings_screen'))

        return sm

if __name__ == '__main__':
    PCDisplay().run()
