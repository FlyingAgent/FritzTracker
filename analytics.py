#####################################
# Wichtige Angaben für das Programm:
#####################################

import json
import matplotlib.pyplot as plt
import numpy as np
import argparse

override_power_buffer = 10
override_temp_buffer = 2

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process power and temperature data')
    parser.add_argument('--path', type=str, required=True, 
                        help='Path to JSON file')
    parser.add_argument('--max-power', type=int, default=800,
                        help='Maximum power value (default: 800)')
    parser.add_argument('--max-temp', type=int, default=40,
                        help='Maximum temperature value (default: 40)')
    parser.add_argument('--scale', type=float, default=1.0,
                        help='Scale factor (0-1, default: 1.0)')
    parser.add_argument('--override-max-power', type=bool, default=False,
                        help=f'Override the maximum power value with the highest value in the data and an additional {override_power_buffer} watts of buffer (default: false, write True with a capital T to use this feature)')
    parser.add_argument('--override-max-temp', type=bool, default=False,
                        help=f'Override the maximum temperature value with the highest value in the data and an additional {override_temp_buffer} °C of buffer (default: false, write True with a capital T to use this feature)')
    return parser.parse_args()

args = parse_arguments()
path = args.path
max_power = args.max_power
max_temp = args.max_temp
scale = args.scale
override_max_power = args.override_max_power
override_max_temp = args.override_max_temp

def extract_json_values(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {json_file_path} not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None
    
data = extract_json_values(path)
power = []
temp = []
name = ''
if data:
    power = data['power_values']
    temp = data['tempereture_values']
    name = data['device_name']

def findlowest(array):
    lowest = array[0]
    for i in array:
        if i < lowest:
            lowest = i
    return lowest

def findhighest(array):
    highest = array[0]
    for i in array:
        if i > highest:
            highest = i
    return highest

ymin1 = 0
ymax1 = max_power * scale

if override_max_power == True:
    ymax1 = findhighest(power) + override_power_buffer

if findlowest(temp) < 0:
    ymin2 = findlowest(temp) - 2
else:
    ymin2 = 0

ymax2 = max_temp * scale
if override_max_temp == True:
    ymax2 = findhighest(temp) + override_temp_buffer

# Create x-axis values in hours
hours = np.arange(len(power)) / 60  # Convert minutes to hours

# Erstelle die erste Achse für 'power_values'
fig, ax1 = plt.subplots()
ax1.plot(hours, power, color='tab:blue')
ax1.set_xlabel('Stunden')
ax1.set_ylabel('Watt', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Manuelle Skalierung der Achsen für ax1
ax1.set_ylim([ymin1, ymax1])

# Zweite y-Achse für 'tempreture_values'
ax2 = ax1.twinx()
ax2.plot(hours, temp, color='tab:red')
ax2.set_ylabel('Temperatur (°C)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Manuelle Skalierung der y-Achse für ax2
ax2.set_ylim([ymin2, ymax2])

# Titel hinzufügen
plt.title(f'{name} Leistung')

# Diagramm anzeigen
plt.show()