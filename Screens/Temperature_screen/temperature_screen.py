from kivy.uix.screenmanager import Screen
import clr
import threading
import time

from hardware_monitor import get_computer

class TemperatureScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monitoring = False
        self.c = get_computer()
        self.tempcpu=0
        self.tempgpu=0

    def start_measurement(self):
        self.ids.status_label.text = "ok"

        if self.manager.ser and self.manager.ser.is_open:
            try:
                self.manager.ser.write("Measure\n".encode())
                time.sleep(0.2)
            except Exception as e:
                print(f"Error sending data: {e}")

        if not self.monitoring:
            if not self.c:
                self.initialize_hardware()
            self.monitoring = True
            if not hasattr(self, 'monitoring_thread') or not self.monitoring_thread.is_alive():
                self.monitoring_thread = threading.Thread(target=self.monitor_hardware)
                self.monitoring_thread.start()

    def go_back(self):
        self.ids.status_label.text = ""
        self.manager.current = 'main_screen'

    def initialize_hardware(self):
        try:
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
                            tempcpu = int(round(float(tempcpu)))
                        if "nvidiagpu/0/temperature/0" in str(sensor.Identifier):
                            tempgpu = sensor.get_Value()
                            tempgpu = int(round(float(tempgpu)))

                # Send data to Arduino
                if self.manager.ser and self.manager.ser.is_open:
                    try:
                        self.manager.ser.write(f"{tempcpu},{tempgpu}\n".encode())
                        print(f"{tempcpu},{tempgpu}\n".encode())
                    except Exception as e:
                        print(f"Error sending data: {e}")

            else:
                print("No hardware components found or hardware not initialized.")

            time.sleep(2)

    def on_stop(self):
        if self.manager.ser and self.manager.ser.is_open:
            try:
                self.ser.manager.close()
            except Exception as e:
                print(f"Error closing serial port: {e}")

