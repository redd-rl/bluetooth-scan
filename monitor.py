import subprocess
import traceback
import simplepyble
from pprint import pprint
import os
import json
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from algs import detect_abnormality
import sys
os.system("color")
if len(sys.argv) == 1:
    try:
        scanning_time = int(input("Input scanning time in ms\n"))
    except:
        print("Defaulting to 15 000ms as inputted value was not an int")
        scanning_time = 15_000
else:
    try:
        scanning_time = int(sys.argv[1])
    except:
        print("Defaulting to 15 000ms as inputted value was not an int.")
        scanning_time = 15_000
try:
    with open(file="bluetooth_ids.json", encoding="utf-8", mode="r") as handle:
        bluetooth_manufacturers: dict = json.loads(handle.read())
except:
    traceback.print_exc()
    print("Failed to locate manufacturers file, all manufacturers will show up as unknown!")

adapters = simplepyble.Adapter.get_adapters()
trackers = {}
subprocess.Popen(f"python server.py {scanning_time}")
while True:
    if len(adapters) == 0:
        raise Exception("No adapters found.")
    adapter = adapters[0]
    iteration = 0
    adapter.scan_for(scanning_time)
    peripherals = adapter.scan_get_results()
    # tracks = [{(peripheral.address(), peripheral.identifier()): peripheral.rssi()} for peripheral in peripherals]
    total_output = []
    manufacturer_ids = []
    manufacturer_names = []
    device_identifiers = []
    try:
        for peripheral in peripherals:
            manufacturer_data = peripheral.manufacturer_data()
            manufacturer_id = 1135
            device_identifiers.append(peripheral.identifier())
            for manufacturer_id,value in manufacturer_data.items():
                manufacturer_id = manufacturer_id if manufacturer_id else 1135
                value=value
                lookup = str(manufacturer_id)
                if lookup in bluetooth_manufacturers.keys():
                    manufacturer_names.append(bluetooth_manufacturers[lookup])
                else:
                    print("name not found")
                    manufacturer_names.append(str(lookup))
        longest_manufacturer = max(manufacturer_names,key=len)
        standardised_len_manufacturers = [f"{name}{'-' * (len(longest_manufacturer) - len(name))}" for name in manufacturer_names]
        longest_identifier = max(device_identifiers,key=len)
        standardised_len_identifiers = [f"{identifier}{'-' * (len(longest_identifier) - len(identifier))}" for identifier in device_identifiers]

        for peripheral, manufacturer, identifier in zip(peripherals, standardised_len_manufacturers, standardised_len_identifiers):
            manufacturer_data = peripheral.manufacturer_data()
            manufacturer_id = 1135
            for manufacturer_id,value in manufacturer_data.items():
                manufacturer_id = manufacturer_id if manufacturer_id else "unknown"
                value=value
            if not peripheral.address() in trackers.keys():
                trackers[peripheral.address()] = {"abnormal":False,"history": []}

            trackers[peripheral.address()]["history"].append(peripheral.rssi())

            if len(trackers[peripheral.address()]['history']) > 15:
                trackers[peripheral.address()]['history'].pop(0)

            trackers[peripheral.address()]["abnormal"] = detect_abnormality(trackers[peripheral.address()]["history"])
            manufacturer_ids.append(manufacturer_id)
            white_space = "-" * (len("Not enough data to determine") - len(str(trackers[peripheral.address()]['abnormal'])))
            abnormal = str(trackers[peripheral.address()]['abnormal']) + white_space if type(trackers[peripheral.address()]['abnormal']) == bool else "Not enough data to determine"
            output = f"{Fore.RED if trackers[peripheral.address()]['abnormal'] == True else Fore.YELLOW if trackers[peripheral.address()]['abnormal'] == 'Not enough data to determine' else Fore.WHITE}'{peripheral.address()}'/'{manufacturer}'/'{identifier}': {{'abnormal': {abnormal}, 'history': {trackers[peripheral.address()]['history']}}}{Style.RESET_ALL}"
            total_output.append(output)
        iteration += 1
        total_output = [x for _, x in sorted(zip(standardised_len_manufacturers,total_output))]
        with open("output.txt", "w") as handle:
            handle.write(
                f"{Fore.WHITE}Formatted as 'Mac Address, Manufacturer, Device name (may be empty), followed by if the collected RSSI values seem abnormal or not, then show the last 20 collected RSSI values.{Style.RESET_ALL}\n" 
                +
                '\n'.join(total_output))
    except ValueError: 
        pass

