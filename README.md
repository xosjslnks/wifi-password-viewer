# 🔑 WiFi Password Viewer CLI

Quickly view all saved WiFi passwords on your machine — no more forgetting them.

WiFi Password Viewer CLI is a lightweight command-line tool that lets you see every WiFi network your computer has previously connected to along with its saved password (when accessible).

The tool supports **Windows, macOS, and Linux** and automatically detects which system it is running on.

Everything runs **locally on your machine**.  
No internet connection, no external servers, and no data collection.

---

# ✨ Features

- List all saved WiFi profiles
- Show clear-text passwords (when accessible)
- Filter results by SSID
- Output results as JSON
- Copy credentials to clipboard
- Optional colorful terminal output
- Safe read-only operation
- Fast and lightweight

---

# 💡 Use Cases

This tool is useful for:

- Recovering forgotten WiFi passwords
- Sharing network credentials quickly
- Checking which networks are saved on a device
- Troubleshooting connection issues
- Exporting saved networks for documentation

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/xosjslnks/wifi-password-viewer.git
cd wifi-password-viewer
```

(Optional) install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies enable:

- Colored terminal output
- Clipboard copy functionality

The script can still run without them.

---

# 🚀 Usage

Run the tool from the project directory:

```bash
python src/viewer.py
```

---

## Show All Saved Networks

```bash
python src/viewer.py
```

Displays every saved WiFi network and its password.

---

## Show Only One Network

```bash
python src/viewer.py --ssid "MyHomeWiFi"
```

---

## JSON Output (for scripts)

```bash
python src/viewer.py --json
```

---

## Copy All Credentials to Clipboard

```bash
python src/viewer.py --clipboard
```

This copies all `SSID:password` pairs.

---

## List Networks Only

```bash
python src/viewer.py --list-only
```

Shows only SSIDs without revealing passwords.

---

## Help Menu

```bash
python src/viewer.py --help
```

Displays all available commands.

---

# 📊 Example Output (Windows)

```
SSID     : HomeNetwork_5G
Password : P@ssw0rd2026!
----------------------------------------

SSID     : Cafe_Free_WiFi
Password : welcome123
----------------------------------------

SSID     : Office-Secure
Password : Corporate2025
----------------------------------------
```

---

# 🖥 Platform Support

| Platform | Command Used | Notes |
|--------|--------------|------|
| Windows | `netsh wlan show profile` | Works for most user profiles |
| macOS | `security` + `networksetup` | May request keychain permission |
| Linux | `nmcli` | Requires NetworkManager |

---

# 🔒 Security & Privacy

WiFi Password Viewer CLI is designed to be safe:

- No internet access required
- No telemetry or tracking
- No data leaves your computer
- Read-only operations only
- Uses built-in system tools

---

# 🤝 Contributing

Pull requests are welcome.

Possible improvements include:

- Export results to CSV or TXT
- Sorting networks by last connection date
- Improved error handling
- GUI version of the tool
- Packaging as a pip-installable CLI

---

# 📜 License

MIT License

You are free to use, modify, and distribute this software.

---

# ⭐ Support

If this project helped you recover a WiFi password or saved you time, consider giving the repository a star.

---

Made with ❤️ by **xobe**
