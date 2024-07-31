import clr
import time
import threading
import serial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Load the OpenHardwareMonitorLib assembly
clr.AddReference(r'C:\Users\Marcin\PycharmProjects\ArduinoDisplay\OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

class PCDisplay(App):
    def build(self):
        self.monitoring = False
        self.c = None
        self.data = "Test message"

        try:
            self.ser = serial.Serial('COM4', 9600, timeout=1)
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
            self.ser = None

        # Layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.label1 = Label(text="CPU Temp: --", font_size='30sp')
        self.label2 = Label(text="GPU Temp: --", font_size='30sp')

        start_button = Button(text="Start", size_hint=(None, None), size=(200, 50))
        start_button.bind(on_press=self.start_button_click)

        stop_button = Button(text="Stop", size_hint=(None, None), size=(200, 50))
        stop_button.bind(on_press=self.stop_button_click)

        test_button = Button(text="Wiadomosc do kotka", size_hint=(None, None), size=(200, 50))
        test_button.bind(on_press=self.test_button_click)

        layout.add_widget(self.label1)
        layout.add_widget(self.label2)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)
        layout.add_widget(test_button)

        return layout

    def test_button_click(self, instance):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(self.data.encode())  # Wysłanie wiadomości do Arduino
            except Exception as e:
                print(f"Error sending data: {e}")

    def start_button_click(self, instance):
        self.label1.text = "Monitoring start"
        self.label2.text = "Monitoring start"
        if not self.monitoring:
            if not self.c:
                self.initialize_hardware()
            self.monitoring = True
            if not hasattr(self, 'monitoring_thread') or not self.monitoring_thread.is_alive():
                self.monitoring_thread = threading.Thread(target=self.monitor_hardware)
                self.monitoring_thread.start()

    def stop_button_click(self, instance):
        self.monitoring = False
        self.label1.text = "Monitoring stopped"
        self.label2.text = "Monitoring stopped"
        if self.c:
            self.c.Close()
            self.c = None

    def initialize_hardware(self):
        try:
            self.c = Computer()
            self.c.CPUEnabled = True
            self.c.GPUEnabled = True
            self.c.Open()
        except Exception as e:
            print(f"Failed to initialize hardware: {e}")

    def monitor_hardware(self):
        while self.monitoring:
            if self.c and len(self.c.Hardware) > 0:
                for hardware in self.c.Hardware:
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if "amdcpu/0/temperature" in str(sensor.Identifier):
                            tempcpu = sensor.get_Value()
                        if "nvidiagpu/0/temperature/0" in str(sensor.Identifier):
                            tempgpu = sensor.get_Value()
                
                # Schedule UI update on the main thread
                Clock.schedule_once(lambda dt: self.update_ui(tempcpu, tempgpu))

                # Send data to Arduino
                if self.ser and self.ser.is_open:
                    try:
                        self.ser.write(f"{tempcpu:.2f},{tempgpu:.2f}\n".encode())
                    except Exception as e:
                        print(f"Error sending data: {e}")

            else:
                print("No hardware components found or hardware not initialized.")

            time.sleep(2)

    def update_ui(self, tempcpu, tempgpu):
        self.label1.text = f"CPU Temp: {tempcpu:.2f}°C"
        self.label2.text = f"GPU Temp: {tempgpu:.2f}°C"

    def on_stop(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
            except Exception as e:
                print(f"Error closing serial port: {e}")

if __name__ == '__main__':
    PCDisplay().run()
