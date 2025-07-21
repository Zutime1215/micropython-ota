import json
import machine
import network
import urequests
from time import sleep
import configOTA
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
    #blink(0.4)

    # Read sha.json  
    with open('sha.json') as f:
        shaJson = json.load(f)
        current_version = shaJson['version']
        old_files = shaJson["files"]

    # Listing Present Files
    old_files_names = {old_file["name"] for old_file in old_files}

    # Checking For New Updated Files
    res = urequests.get(check_url, headers=headers).text
    repo_tree = json.loads(res)["tree"]
    files = []

    for leaf in repo_tree:
        nameL = leaf["path"].split("otaDir")
        if nameL[0] == '':
            if nameL[1] == '':
                if current_version == leaf["sha"]:
                    return
                latest_version = leaf["sha"]
            elif nameL[1].startswith('/'):
                files.append({"name": nameL[1][1:], "sha": leaf["sha"]})


    new_files_names = {file["name"] for file in files}
    
    # Replace and Creating Files
    for file in files:
        flag = True
        for old_file in old_files:
            if file["sha"] == old_file["sha"]:
                flag = False
                break
        if flag:
            res = urequests.get(mainCode_url + file["name"]).text
            with open(file["name"], 'w') as f:
                f.write(res)


    # Remove Files not NEEDED
    deletable_files = list(old_files_names - new_files_names)
    for delFiles in deletable_files:
        remove(delFiles)

    # Update The sha.json
    with open('sha.json', 'w') as f:
        json.dump({'version': latest_version, "files": files}, f)

