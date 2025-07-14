# ESP32 MicroPython OTA Updater

This repository provides a **OTA (Over-The-Air) updater** for ESP32 running MicroPython. It checks a GitHub repository for updates to `main.py` and downloads the latest version if available, allowing you to update your ESP32 remotely without reflashing firmware manually.

---

## 🚀 Features

✅ **Checks for updates** by comparing `version.json` on the device and on GitHub.  
✅ **Connects to WiFi automatically** using your credentials.  
✅ **Downloads `main.py`** from your GitHub repository if a newer version is available.  
✅ **Stores the updated version and timestamp** locally in `version.json`.  
✅ **Automatically restarts the ESP32** after updating to run the new code.  
✅ **Provides LED blink feedback** for status indication.


---

## 🛠️ Setup Instructions

### 1️⃣ Create `wifi_cred.py`

Add your WiFi credentials:
```python
# wifi_cred.py
ssid = "YourSSID"
password = "YourPassword"
```

### 2️⃣ Create `version.json`

Initially:
```python
{
  "version": 0,
  "time": 0
}
```

### 3️⃣ Upload files

Upload:
- `ota.py` 
- `wifi_cred.py`
- `version.json`
- A starter  `main.py` file

to your ESP32.

### 4️⃣ Configure GitHub Repository

- Host your `main.py` and `version.json` in your GitHub repository.
- `version.txt` should be:
```json
{
  "version": 1
}
```
- Update the `repo_url` inside `ota.py`:
```python
repo_url = "YourGitHubUsername/YourRepoName"
```

### ⚡ Notes
- ✅ Ensure your GitHub repository is public or raw file links are accessible without authentication
- ✅ Update the `version` number everytime you change the `main.py` of the repo.