import json
from datetime import datetime
import argparse


class File:
    def __init__(self, path, power, temp, name):
        self.path = path
        self.name = name
        self.power = power
        self.temp = temp

    def __str__(self):
        try:
            return f"Path: {self.path}, Name: {self.name}"
        except Exception as e:
            return f"Error getting device information: {e}"
        
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process power and temperature data')
    parser.add_argument('--path', type=str, required=True, 
                        help='Path to the first JSON file')
    parser.add_argument('--end', type=str, required=True,
                        help='Date of the last JSON file')
    return parser.parse_args()

def extract_json_values(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None

def getFile(path):
    currentdata = extract_json_values(path)
    currentname = currentdata['device_name']
    print(currentname)

#Get parameters from the file name
def extract_params(param_string):
    # Parse "key=value,key2=value2" format
    params = []
    pairs = param_string.split('.')
    pairs.pop(pairs.index('json'))
    for pair in pairs:
        params.append(pair.split('_'))
    return params

#Get date, month and year from date string
def extract_date(date_string):
    return date_string.split('-')

#Find all files between two dates
def find_all_files(current_d, current_m, current_y, end_d, end_m, end_y):
    files = []
    c = True
    while c == True:
        path = f"testdata/data_Balkonkraftwerk_{current_y}-{current_m}-{current_d}.json"
        # Überprüfen, ob Datei
        if(extract_json_values(path) != None):
            print("File found: " + path)

            #
            files.append(File(path, extract_json_values(path)['power_values'], extract_json_values(path)['tempereture_values'], extract_json_values(path)['device_name']))
            #

            #Überprüfen, ob aktuelles Datum gleich Enddatum ist, also die Schleife beendet werden kann
            if current_d == end_d and current_m == end_m and current_y == end_y:
                c = False
                break

            #Da die Schleife nicht beendet werden muss, wird der aktuelle Tag um 1 erhöht
            current_d = current_d + 1
        else:
            current_d = current_d + 1
            if(extract_json_values(path) != None):
                print("File found: " + path)
            else:
                current_m = current_m + 1
                if (current_m > 12):
                    current_m = 1
                    current_y = current_y + 1
                current_d = 1
                if(extract_json_values(path) != None):
                    print("File found")
                else:
                    print("No file found")
    return files

def merge_data(data_to_merge):
    data = []
    for d in data_to_merge:
        data.append(d)
    return data

#Save merged data to file
def save_data(device, power, temp, start, end):
    try:
        data = {
            'device_name': device,
            'power_values': power,
            'tempereture_values': temp,
        }
        with open(f'merged_data_{device}_{start}_{end}.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully")    
    except Exception as e:
        print(f"Error saving data: {e}")

args = parse_arguments()
path = args.path
end = args.end

params = extract_params(path)[0]
prefix = params[0]
device = params[1]
date = params[2]

rootpath = f"{prefix}_{device}_{date}.json"

# Example usage:
start_date_string = date
end_date_string = end

start_date = extract_date(start_date_string)
end_date = extract_date(end_date_string)

current_d = int(start_date[2])
current_m = int(start_date[1])
current_y = int(start_date[0])
end_d = int(end_date[2])
end_m = int(end_date[1])
end_y = int(end_date[0])

print(f"Start date: {current_d}.{current_m}.{current_y}")
print(f"End date: {end_d}.{end_m}.{end_y}")

files = find_all_files(current_d, current_m, current_y, end_d, end_m, end_y)

data_power = []
data_temp = []

for file in files:
    print(file)
    for power in file.power:
        data_power.append(power)
    for temp in file.temp:
        data_temp.append(temp)

save_data(device, data_power, data_temp, start_date_string, end_date_string)