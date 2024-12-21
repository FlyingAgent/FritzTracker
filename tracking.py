from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
import threading
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
# FritzBox Zugangsdaten
FRITZBOX_ADDRESS = os.getenv('FRITZBOX_ADDRESS')
USERNAME = os.getenv('FRITZBOX_USERNAME')
PASSWORD = os.getenv('FRITZBOX_PASSWORD')


# Verbindung zur FRITZ!Box herstellen
home_auto = FritzHomeAutomation(address=FRITZBOX_ADDRESS, user=USERNAME, password=PASSWORD)
devices = home_auto.get_homeautomation_devices()

# Interval für die Speicherung der Daten in Sekunden
interval = int(os.getenv('INTERVAL', 60))  # Default to 60 if not set

def getName(ain):
   return home_auto.get_device_information_by_identifier(ain)['NewDeviceName']

def getPower(ain):
    return home_auto.get_device_information_by_identifier(ain)['NewMultimeterPower'] / 100

def getTemperature(ain):
    return home_auto.get_device_information_by_identifier(ain)['NewTemperatureCelsius'] / 10.0

def getDate():
    return datetime.now().strftime('%Y-%m-%d')

devicestats = []

class Device:
    def __init__(self, ain, name, power, temperature, date):
        self.ain = ain
        self.name = name
        self.power = power
        self.temperature = temperature
        self.date = date

    def __str__(self):
        try:
            return f"   AIN: {self.ain}, Name: {self.name}, Power: {self.power}, Temperature: {self.temperature}, Date: {self.date}"
        except Exception as e:
            return f"Error getting device information: {e}"
    
    def update(self):
        try:
            power = getPower(self.ain)
            temp = getTemperature(self.ain)
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            name = self.name
            self.power.append(power)
            self.temperature.append(temp)
            self.date = getDate()
            print(f"    {name} - {date} --> {power}W | {temp}°C")
        except Exception as e:
            print(f"Error updating device: {e}")
    
    def save_data(self):
        try:
            data = {
                'device_name': self.name,
                'power_values': self.power,
                'tempereture_values': self.temperature,
            }
            with open(f'data_{self.name}_{self.date}.json', 'w') as f:
                json.dump(data, f, indent=4)
            print("Data saved successfully")    
        except Exception as e:
            print(f"Error saving data: {e}")

print("Searching for devices...")
for device in devices:
    try:
        devicestats.append(Device(device.AIN, getName(device.AIN), [], [], getDate()))
        print(f"    AIN: {device.AIN}")
        print(f"    Name: {getName(device.AIN)}")
    except Exception as e:
        print(f"Error getting device information: {e}")

print("Getting device stats...")
for device in devicestats:
    try:
        print(device)
    except Exception as e:
        print(f"Error printing device: {e}")

timer = None

def execute_periodically():
    global timer
    current_date = getDate()
    
    for device in devicestats:
        if (device.date != current_date):
            device.power.clear()
            device.temperature.clear()
            device.date = current_date
            print(f"    {device.name} - Data reset")
        device.update()
        device.save_data()
    
    # Schedule next execution
    timer = threading.Timer(interval, execute_periodically)
    timer.start()

def start_collection():
    """
    Starts the periodic data collection process.
    This function initializes the periodic execution of device data updates and saves.
    """
    print("Starting data collection...")
    execute_periodically()

start_collection()