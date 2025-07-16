# MicroPython OTA Updater

This repository provides a **clean, reliable OTA (Over-The-Air) updater for ESP32/ESP8266**(Tested) **running MicroPython**. It checks your GitHub repository for updates to `main.py`, downloads the latest version if available, and restarts your Machine automatically to apply updates **without reflashing firmware manually**.

---

## 🚀 Features

✅ Checks for updates by comparing **SHA (`sha.json`) on the device and GitHub** (ensures reliable version detection).  
✅ Connects to WiFi automatically using your credentials.  
✅ Downloads `fileName` from your GitHub repository if a newer version is available.  
✅ Stores the updated SHA locally in `sha.json`.  
✅ Automatically restarts the ESP32 after updating to run the new code.  
✅ Optional LED blink feedback for status indication.  
✅ Controlled OTA updates using a **physical GPIO pin for safe updates** (update only when the pin is held LOW on boot).

---

## 🛠️ Setup Instructions

### 1️⃣ Fill `configOTA.py`
Add your WiFi and repository configurations:

```python
ssid = "YourSSID"
password = "YourPassword"
repoURL = "YourGitHubUsername/YourRepoName"
branch = "branchName"
fileName = "fileName.py"
builtinLED = 2            # GPIO for onboard LED (optional)
updateGPIO = 5            # GPIO pin to trigger OTA update
```

### 2️⃣ Prepare your GitHub repository
- GitHub must be public or raw URLs must be accessible without authentication.

### 3️⃣ Upload files to your ESP32
- `boot.py`
- `ota.py`
- `configOTA.py`
- `sha.json`
- A starter `main.py`



### 4️⃣ OTA update triggering
- Connect GPIO pin defined as `updateGPIO` (default GPIO 5) to GND during boot to trigger OTA.
- If the pin is HIGH during boot, OTA will be skipped.
---

### ⚡ How It Works
✅ On boot, if the `updateGPIO` pin is LOW:
- Connects to WiFi.
- Fetches the SHA of `fileName` from your GitHub repository.
- If the SHA differs from the stored SHA in `sha.json`, it:
  - Downloads the latest `fileName`.
  - Updates `sha.json` with the new SHA.
  - Restarts the Machine to apply the update.

✅ If the SHA is the same, it skips updating and runs normally.