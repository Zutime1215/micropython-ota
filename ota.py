import json
import machine
import network
import urequests
from time import sleep
import wifi_cred


def blink(t):
    led = machine.Pin(2, machine.Pin.OUT)
    for i in range(4):
        led.value(1)
        sleep(t)
        led.value(0)
        sleep(t)
        
def main():
    repo_url = "Zutime1215/own_esp32_u"
    branch = "main"
    file_name = "main.py"

    check_url = f"https://api.github.com/repos/{repo_url}/contents/{file_name}?ref={branch}"
    mainCode_url = f"https://raw.githubusercontent.com/{repo_url}/refs/heads/{branch}/{file_name}"

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
    with open('sha.json') as f:
        current_version = json.load(f)['version']
    
    res = urequests.get(check_url).text
    data = json.loads(res)
    latest_version = data['sha']
    
    if current_version != latest_version:
        blink(0.1)
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