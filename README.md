# ⚡ DNS Changer Pro

A fast, modern, and interactive terminal-based DNS switcher and benchmarking tool for Windows, written in Python with a rich TUI.

Easily switch between popular DNS providers, bypass sanctions, unblock gaming services, enhance your privacy, benchmark real DNS query latency across servers, and manage custom DNS servers.

---

## 🌟 Key Features

* **🎨 Modern Terminal UI (Rich TUI)**: Interactive arrow-key navigation, searchable menus, status cards, and color-coded latency tables.
* **🚀 Real UDP DNS Benchmark**: Measure actual query resolution latency (port 53 UDP) across all DNS servers concurrently with live progress tracking and 1-click connection to the fastest server.
* **📂 Categorized DNS Profiles**:
  * ⚡ **Anti-Sanction & Bypass (IR)**: Shecan, Electro, 403 Online, Radar Game, Bogzar, Gozar, Host Iran, Shatel, Pishgaman.
  * 🌐 **Global & Fast**: Cloudflare (1.1.1.1), Google Public DNS, OpenDNS Cisco, Neustar, Verisign, Comodo, Yandex.
  * 🛡️ **Privacy & Ad-Block**: Quad9 (Malware blocking), AdGuard DNS (Ad blocking), CleanBrowsing, SafeDNS, DNS.Watch, OpenNIC.
  * 🎮 **Gaming & Low Ping**: Cloudflare Gaming, Radar Game, Electro Gaming, Google DNS, Quad9.
* **⚙️ Custom DNS Manager**: Add, edit, and remove your own custom DNS profiles saved persistently in `dns_config.json`.
* **🔍 Search & Filter**: Instant filtering across all built-in and custom DNS profiles.
* **🛡️ Windows Network Integration**:
  * Auto UAC Administrator elevation prompt on startup.
  * Robust network interface detection (properly handles adapter names with spaces like `"Wi-Fi"`, `"Ethernet 2"`).
  * Auto-detects active internet adapter with manual interface switching.
  * Auto-flushes Windows DNS resolver cache (`ipconfig /flushdns`) after every change.
  * One-click reset to router default / automatic DHCP.
* **📦 Standalone Executable**: Easily compile to a single `.exe` using PyInstaller.

---

## 📋 Requirements

* Windows 10 / 11 / Server
* Python 3.9+ (if running from source)
* Administrator privileges (the script will automatically request UAC elevation if needed)

---

## 🚀 Quick Start

### 1. Clone or Download the Repository

```bash
git clone https://github.com/undeadmoon84/DNS-changer.git
cd DNS-changer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run DNS Changer

```bash
python main.py
```
*(or run `python DNS.py`)*

---

## 🛠️ Build Standalone Windows Executable (.exe)

You can build a single `.exe` file without needing Python installed on other machines:

### Option 1: Run the Build Script (Recommended)
Double-click `build.bat` or run:
```cmd
build.bat
```

### Option 2: Manual PyInstaller Command
```bash
pip install pyinstaller
pyinstaller --onefile --name "DNS-Changer" --clean main.py
```

The compiled standalone executable will be located in the `dist/DNS-Changer.exe` folder.

---

## 📁 Project Structure

```
DNS-changer/
├── core/
│   ├── network.py       # Windows adapter detection, DNS set/clear/read, auto UAC elevation
│   ├── benchmark.py     # Concurrent UDP DNS query latency testing
│   └── storage.py       # Categorized presets, provider identification, custom DNS storage
├── ui/
│   ├── display.py       # Rich formatting, status banners, benchmark tables, alerts
│   └── menu.py          # Questionary interactive flows (category picker, search, benchmark)
├── main.py              # Main interactive loop entrypoint
├── DNS.py               # Backward-compatible wrapper
├── requirements.txt     # Dependencies (rich, questionary, dnspython, pyinstaller)
├── build.bat            # One-click PyInstaller build script
├── .gitignore           # Git ignore configuration
└── README.md            # Documentation
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
