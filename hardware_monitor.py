import clr

clr.AddReference(r'C:\Users\Marcin\Desktop\PCDisplay\Lib\OpenHardwareMonitorLib')

from OpenHardwareMonitor.Hardware import Computer
from OpenHardwareMonitor.Hardware import HardwareType

# Initialize the Computer object and enable CPU and GPU monitoring
def get_computer():
    computer = Computer()
    computer.CPUEnabled = True
    computer.GPUEnabled = True
    computer.Open()
    return computer

# Function to get the CPU model
def get_cpu_model(computer):
    if computer:
        for hardware in computer.Hardware:
            if hardware.HardwareType == HardwareType.CPU:
                return hardware.Name[4:]
    return "Unknown CPU model"

# Function to get the GPU model
def get_gpu_model(computer):
    if computer:
        for hardware in computer.Hardware:
            if hardware.HardwareType in (HardwareType.GpuNvidia, HardwareType.GpuAti):
                return hardware.Name[22:]
    return "Unknown GPU model"