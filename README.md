# BluetoothScan
Scans nearby area for Bluetooth devices and displays them for clients, clients are able to connect via a WebSocket (port 8765).

# Set-up
## Client
`git clone https://github.com/redd-rl/bluetooth-scan.git`

`python -m pip install -r requirements.txt`

Then run the corresponding file for your OS, out of `run_windows.bat`, `run-mac.sh` and `run_linux.sh`
## Server
Prior knowledge here is assumed but the process is similar.
`git clone https://github.com/redd-rl/bluetooth-scan.git`

`python -m pip install -r requirements.txt`

# How to run
## Client
`python client.py`
##  Server
`python server.py`

### Footnote
If bluetooth_ids.json isn't present ALL manufacturers will show up as their CIC ids, as reported from the bluetooth device.
