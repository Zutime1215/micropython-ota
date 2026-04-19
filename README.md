# ESP MicroPython OTA Update System (Local Network)

This repository contains a simple **Over-The-Air (OTA)** update system for MicroPython-based devices (ESP8266/ESP32) that works **entirely over a local network (LAN)**. No cloud or remote hosting is required.

---

## 📁 Project Structure

```
ota.py          # Handles OTA update logic
configOTA.py    # Configuration file for WiFi and local server
boot.py         # Runs at boot to trigger OTA update
sha.json        # Stores current firmware version
```

---

## ⚙️ How It Works (LAN-based OTA)

1. On boot, the device checks a GPIO pin (`updateGPIO`).
2. If the pin is pulled **LOW**, OTA update process starts.
3. Device connects to your **local WiFi network**.
4. It queries a **local HTTP server (same LAN)** for the latest version hash.
5. Compares it with the local version stored in `sha.json`.
6. If a new version is found:
   - Downloads updated `main.py` from the local server
   - Updates `sha.json`
   - Restarts the device
7. If no update is available, it exits normally.

---

## 🧩 Configuration

Edit `configOTA.py`:

```python
ssid = "YOUR_WIFI_SSID"
password = "YOUR_WIFI_PASSWORD"
serverURL = "192.168.1.101:8080"  # Local server IP
branch = "main"
fileName = "main.py"
builtinLED = 2
updateGPIO = 5
```

### Parameters

- **ssid / password**: Your local WiFi credentials
- **serverURL**: **Local server IP + port** (must be in same network)
- **branch**: Used to read version hash from `.git` (optional but used here)
- **fileName**: File to download (typically `main.py`)
- **builtinLED**: LED pin (optional for debugging)
- **updateGPIO**: GPIO pin to trigger update mode

---

## 🖥️ Local Server Setup

You must run a server **inside your LAN**.

### Option 1: Simple Python HTTP Server

In your project folder:

```bash
python -m http.server 8080
```

Make sure your folder contains:

```
main.py
.git/refs/heads/main
```

### Option 2: Any Local Web Server

You can also use:
- Flask
- Node.js
- Nginx / Apache

As long as these endpoints work:

- `http://<serverIP>:8080/.git/refs/heads/main`
- `http://<serverIP>:8080/main.py`

---

## 🚀 Usage

### 1. Upload Files to Device

- `boot.py`
- `ota.py`
- `configOTA.py`
- `sha.json`

### 2. Start Local Server

Run your server on your PC (same WiFi network).

### 3. Trigger OTA Update

- Connect `updateGPIO` → **GND (LOW)**
- Restart device

The device will:
- Connect to WiFi
- Contact your **local server**
- Update if needed

---

## 💡 Notes

- This system works **offline (no internet required)**.
- Both device and server must be on the **same network**.
- `sha.json` must exist before first run.
- Only `main.py` is updated (can be extended).
- Uses `.git` reference to detect version changes.

---

## 🔧 Future Improvements

- Remove dependency on `.git` (use custom version API)
- Multi-file OTA updates
- Compression for faster transfer
- Authentication for security
- Web dashboard for updates

---

## 📜 License

Open-source — use and modify freely.

