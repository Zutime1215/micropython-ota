# MicroPython OTA Updater

This repository provides a **clean, reliable OTA (Over-The-Air) updater for ESP32/ESP8266**(Tested) **running MicroPython**. It checks your GitHub repository for updates, downloads the **latest version** if available.

---

## 🚀 Features  
✅ Connects to WiFi automatically using your credentials.  
✅ Uses GitHub API to check file trees and commit hashes.  
✅ Stores the updated SHA locally in `sha.json`.  
✅ Downloads only changed files to save bandwidth.  
✅ Removes outdated files automatically.  
✅ Optional LED blink feedback for status indication.  
✅ Controlled OTA updates using a **physical GPIO pin for safe updates** (update only when the pin is held LOW on boot).

---
## 🧬 File Structure on Machine
- `boot.py`: Checks GPIO on boot; if pulled low, triggers OTA update.
- `otaDir/configOTA.py`: Stores WiFi, GitHub repo info, LED pin, and update trigger pin.
- `otaDir/ota.py`: Main OTA logic; connects WiFi, checks GitHub, downloads updated files, and cleans up.
- `otaDir/sha.json`: Stores the latest file SHAs for version tracking.
---

## 🛠️ Setup Instructions
### 1️⃣ Setup GitHub Repository
- Push your MicroPython project files inside `otaDir/` in your GitHub repo.

### 2️⃣ Fill `configOTA.py`
Add your WiFi and repository configurations:

```python
ssid = "YourWiFiSSID"
password = "YourWiFiPassword"
repoURL = "YourUserOrOrg/YourRepoName"
branch = "main"
builtinLED = 2       # GPIO for onboard LED
updateGPIO = 5       # GPIO to pull LOW for OTA update
```
### 3️⃣ OTA update triggering
- You push code updates to GitHub and reboot your device with `updateGPIO` pulled LOW to trigger OTA.
- If the pin is HIGH during boot, OTA will be skipped.
---