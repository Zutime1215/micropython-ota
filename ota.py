import os
import json
import machine
import network
import urequests
from time import sleep, time
import wifi_cred


def blink(t):
    led = machine.Pin(2, machine.Pin.OUT)
    for i in range(4):
        led.value(1)
        sleep(t)
        led.value(0)
        sleep(t)
        
        
def main():
    repo_url = ""
    version_url = f"https://raw.githubusercontent.com/{repo_url}/refs/heads/main/version.json"
    mainCode_url = f"https://raw.githubusercontent.com/{repo_url}/refs/heads/main/main.py"
    
    
    # Check For Do OTA
    with open('version.json') as f:
        prev_time = int(json.load(f)['time'])
    
    #if time() - prev_time > 30:
    # Connect To WIFI
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(wifi_cred.ssid, wifi_cred.password)
    while not sta_if.isconnected():
        print('.', end="")
        sleep(0.25)
    print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
    blink(0.4)

    # Check For Update
    if 'version.json' in os.listdir():    
        with open('version.json') as f:
            current_version = int(json.load(f)['version'])
    else:
        current_version = 0
        with open('version.json', 'w') as f:
            json.dump({'version': current_version}, f)
    
    res = urequests.get(version_url).text
    data = json.loads(res)
    latest_version = data['version']
    
    if current_version < latest_version:
        blink(0.1)
        # Change The main and version file
        res = urequests.get(mainCode_url).text
        with open('main.py', 'w') as f:
            f.write(res)
            
        with open('version.json', 'w') as f:
            json.dump({'version': latest_version, 'time': int(time())}, f)
        
        # Restart The Machine    
        machine.reset()
    else:
        return

