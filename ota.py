import json
import machine
import network
import urequests
from time import sleep
from otaDir import configOTA
from os import remove


def blink(t):
    led = machine.Pin(configOTA.builtinLED, machine.Pin.OUT)
    for i in range(4):
        led.value(1)
        sleep(t)
        led.value(0)
        sleep(t)
        
def main():
    headers = {"User-Agent": "ESP-MicroPython"}
    check_url = f"https://api.github.com/repos/{configOTA.repoURL}/git/trees/{configOTA.branch}?recursive=1"
    mainCode_url = f"https://raw.githubusercontent.com/{configOTA.repoURL}/refs/heads/{configOTA.branch}/otaDir/"

    # Connect To WIFI
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(configOTA.ssid, configOTA.password)
    while not sta_if.isconnected():
        sleep(0.25)
    print(f"Machine: Wifi Connected. IP: {sta_if.ifconfig()[0]}")

    # Read sha.json  
    with open('otaDir/sha.json') as f:
        shaJson = json.load(f)
        current_version = shaJson['version']
        old_files = shaJson["files"]

    # Listing Present Files
    old_files_names = {old_file["name"] for old_file in old_files}

    # Checking For New Updated Files
    checkResponse = json.loads(urequests.get(check_url, headers=headers).text)
    repo_tree = checkResponse["tree"]
    files = []

    for leaf in repo_tree:
        nameL = leaf["path"].split("otaDir")
        if nameL[0] == leaf["path"]:
            continue
        elif nameL[0] == '':
            if nameL[1] == '':
                if current_version == leaf["sha"]:
                    return
                latest_version = leaf["sha"]
            elif nameL[1].startswith('/'):
                files.append({"name": nameL[1][1:], "sha": leaf["sha"]})
    
    # if Remote otaDir not contains any files
    if len(files) == 0:
        latest_version = checkResponse["sha"]

    new_files_names = {file["name"] for file in files}
    
    # Replace and Creating Files
    for file in files:
        flag = True
        for old_file in old_files:
            if file["sha"] == old_file["sha"]:
                flag = False
                break
        if flag:
            print("Machine: Updating", file)
            fileResponse = urequests.get(mainCode_url + file["name"]).text
            with open(file["name"], 'w') as f:
                f.write(fileResponse)


    # Remove Files not NEEDED
    deletable_files = list(old_files_names - new_files_names)
    print("Machine: Deleting", deletable_files if len(deletable_files) != 0 else "0 files")
    for delFiles in deletable_files:
        remove(delFiles)
    
    
    # Update The sha.json
    print("Machine: Updating sha.json")
    with open('otaDir/sha.json', 'w') as f:
        json.dump({'version': latest_version, "files": files}, f)
        
    # set updateGPIO to HIGH
    blink(0.4)
    sleep(10)
