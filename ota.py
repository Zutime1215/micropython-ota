import json
import machine
import network
import urequests
from time import sleep
import configOTA


def blink(t):
    led = machine.Pin(configOTA.builtinLED, machine.Pin.OUT)
    for i in range(4):
        led.value(1)
        sleep(t)
        led.value(0)
        sleep(t)
        
def main():
    headers = {"User-Agent": "ESP-MicroPython"}
    check_url = f"http://{configOTA.serverURL}/.git/refs/heads/{configOTA.branch}"
    mainCode_url = f"http://{configOTA.serverURL}/{configOTA.fileName}"

    # Connect To WIFI
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(configOTA.ssid, configOTA.password)
    while not sta_if.isconnected():
        print('.', end="")
        sleep(0.25)
    print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
    #blink(0.4)

    # Check For Update    
    with open('sha.json') as f:
        current_version = json.load(f)['version']
    
    latest_version = urequests.get(check_url, headers=headers).text
    
    if current_version != latest_version:
        #blink(0.1)
        # Change The main and version file
        res = urequests.get(mainCode_url).text
        with open('main.py', 'w') as f:
            f.write(res)
            
        with open('sha.json', 'w') as f:
            json.dump({'version': latest_version}, f)
        
        # Restart The Machine    
        machine.reset()
    else:
        return