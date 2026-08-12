# ⚡ DNS Changer Pro

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6.svg?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Interface](https://img.shields.io/badge/UI-Rich%20TUI-cyan.svg?style=for-the-badge&logo=gnubash&logoColor=white)](https://github.com/Textualize/rich)
[![Status](https://img.shields.io/badge/Speed-1--Step%20Switch-success.svg?style=for-the-badge)](https://github.com/undeadmoon84/DNS-changer)

**A fast, modern, terminal-based DNS switcher, speed benchmarking suite, and profile manager for Windows.**  
*Switch DNS in 1 second, benchmark real UDP query latency, bypass anti-sanction filters, and protect your privacy.*

[Quick Start](#-quick-start) • [Features](#-key-features) • [DNS Providers](#-included-dns-providers) • [Benchmark](#-real-udp-dns-benchmark) • [Build .exe](#-building-standalone-windows-exe) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📺 Terminal Interface Preview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│         ⚡ DNS CHANGER PRO ⚡                                               │
│         Fast 1-Step DNS Switcher • Anti-Sanction & Gaming • Privacy         │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────── 📡 Live System Status ───────────────────────────┐
│       Privileges:  🛡️ Administrator                                          │
│ Active Interface:  📶 Wi-Fi                                                 │
│   Configured DNS:  178.22.122.100  |  185.51.200.2                          │
│   Active Profile:  ✨ Shecan (178)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────┬──────────────┬────────────────┬─────┬───────────────┬─────────────────┐
│   # │ Provider Name│ Primary IP     │   # │ Provider Name │ Primary IP      │
├─────┼──────────────┼────────────────┼─────┼───────────────┼─────────────────┤
│  1. │ Shecan (178) │ 178.22.122.100 │ 14. │ Alternate DNS │ 76.76.19.19     │
│  2. │ Shecan (185) │ 185.51.200.2   │ 15. │ Verisign      │ 64.6.64.6       │
│  3. │ Electro      │ 78.157.42.100  │ 16. │ Neustar Ultra │ 156.154.70.1    │
│  4. │ 403 Online   │ 10.202.10.202  │ 17. │ Comodo Secure │ 8.26.56.26      │
│  5. │ Radar Game   │ 10.202.10.10   │ 18. │ Yandex DNS    │ 77.88.8.8       │
│  6. │ Bogzar DNS   │ 185.55.226.26  │ 19. │ Dyn DNS       │ 216.146.35.35   │
│  7. │ Gozar DNS    │ 185.55.225.25  │ 20. │ Quad9 Malware │ 9.9.9.9         │
│  8. │ Host Iran    │ 172.29.2.100   │ 21. │ AdGuard (Def) │ 94.140.14.14    │
│  9. │ Shatel DNS   │ 85.15.1.15     │ 22. │ AdGuard (Leg) │ 176.103.130.130 │
│ 10. │ Pishgaman    │ 5.202.100.100  │ 23. │ CleanBrowsing │ 185.228.168.9   │
│ 11. │ Cloudflare   │ 1.1.1.1        │ 24. │ SafeDNS       │ 195.46.39.39    │
│ 12. │ Google Public│ 8.8.8.8        │ 25. │ DNS.Watch     │ 84.200.69.80    │
│ 13. │ OpenDNS      │ 208.67.222.222 │ 26. │ OpenNIC       │ 46.151.208.154  │
└─────┴──────────────┴────────────────┴─────┴───────────────┴─────────────────┘
  0. Reset to Automatic (DHCP)  [B] Benchmark Speed  •  [M] Custom DNS  •  [S] Switch Adapter  •  [F] Flush  •  [Q] Exit

👉 Enter DNS number [0-26] or Hotkey (B/M/S/F/Q): 
```

---

## 🌟 Key Features

* ⚡ **Instant 1-Step Switching**: Type any provider number (`1`-`26` or `0` for DHCP) and hit Enter. DNS applies immediately, flushes cache, and exits automatically in 1 second.
* 🚀 **Real UDP DNS Query Benchmark**: Concurrently queries target DNS servers (UDP Port 53) to benchmark resolution speed with live millisecond latency metrics and 1-click connection to the fastest provider.
* 🛡️ **Zero-Friction Windows Integration**:
  * **Automatic UAC Elevation**: Automatically prompts for Administrator rights on startup if not already elevated.
  * **Smart Adapter Detection**: Automatically selects the primary connected adapter (e.g. Wi-Fi, Ethernet).
  * **Spaces-Safe Adapter Names**: Reliably handles interface names containing spaces (`"Wi-Fi"`, `"Local Area Connection"`, `"Ethernet 2"`).
  * **Automatic Cache Flush**: Automatically runs `ipconfig /flushdns` after every change.
* 🎨 **Rich Terminal Experience**: Beautiful 2-column high-contrast layout, live status panel, color-coded latency tables, and full UTF-8 support.
* ⚙️ **Custom DNS Profiles**: Add, edit, and remove your own DNS servers with persistent JSON storage (`dns_config.json`).
* 📦 **Standalone Executable Ready**: Includes `build.bat` for 1-click PyInstaller `.exe` compilation.

---

## 📋 Included DNS Providers

### ⚡ Anti-Sanction & Bypass (IR)
| Provider Name | Primary DNS | Secondary DNS | Purpose |
| :--- | :--- | :--- | :--- |
| **Shecan (178)** | `178.22.122.100` | `185.51.200.2` | Popular Iranian sanction-bypass DNS |
| **Shecan (185)** | `185.51.200.2` | `178.22.122.100` | Alternative Shecan routing server |
| **Electro** | `78.157.42.100` | `78.157.42.101` | Sanction bypass & gaming optimization |
| **403 Online** | `10.202.10.202` | `10.202.10.102` | Developer & service sanction bypass |
| **Radar Game** | `10.202.10.10` | `10.202.10.11` | Low-ping gaming & service unblocker |
| **Bogzar DNS** | `185.55.226.26` | `185.55.225.25` | Fast sanction bypass DNS |
| **Gozar DNS** | `185.55.225.25` | `185.55.225.26` | Alternative bypass DNS |
| **Host Iran** | `172.29.2.100` | `172.29.0.100` | Infrastructure & regional DNS |
| **Shatel DNS** | `85.15.1.15` | `85.15.1.14` | Shatel ISP DNS |
| **Pishgaman DNS** | `5.202.100.100` | `5.202.100.101` | Pishgaman ISP DNS |

### 🌐 Global & Fast
| Provider Name | Primary DNS | Secondary DNS | Purpose |
| :--- | :--- | :--- | :--- |
| **Cloudflare (1.1.1.1)** | `1.1.1.1` | `1.0.0.1` | Global fastest privacy-first DNS |
| **Google Public DNS** | `8.8.8.8` | `8.8.4.4` | High stability & universal availability |
| **OpenDNS (Cisco)** | `208.67.222.222` | `208.67.220.220` | Enterprise security and reliability |
| **Alternate DNS** | `76.76.19.19` | `76.223.122.150` | Fast ad-blocking alternative |
| **Verisign** | `64.6.64.6` | `64.6.65.6` | Premium stability global DNS |
| **Neustar UltraDNS** | `156.154.70.1` | `156.154.71.1` | Recursive enterprise edge DNS |
| **Comodo Secure** | `8.26.56.26` | `8.20.247.20` | Security-filtered recursive DNS |
| **Yandex DNS** | `77.88.8.8` | `77.88.8.1` | Eastern Europe & CIS routing |
| **Dyn DNS** | `216.146.35.35` | `216.146.36.36` | Oracle Dyn public resolver |

### 🛡️ Privacy & Security
| Provider Name | Primary DNS | Secondary DNS | Purpose |
| :--- | :--- | :--- | :--- |
| **Quad9 (Malware Block)** | `9.9.9.9` | `149.112.112.112` | Blocks malicious domains & spyware |
| **AdGuard DNS (Default)** | `94.140.14.14` | `94.140.15.15` | Blocks ads, tracking & phishing |
| **AdGuard DNS (Legacy)** | `176.103.130.130` | `176.103.130.131` | Legacy AdGuard address pool |
| **CleanBrowsing** | `185.228.168.9` | `185.228.169.9` | Security filter & family safety |
| **SafeDNS** | `195.46.39.39` | `195.46.39.40` | Cyber-threat protection |
| **DNS.Watch** | `84.200.69.80` | `84.200.70.40` | Uncensored, no-logging German DNS |
| **OpenNIC** | `46.151.208.154` | `128.199.248.105` | Decentralized community DNS |

---

## 🚀 Quick Start

### 1. Prerequisites
- **Operating System**: Windows 10 / 11 / Windows Server
- **Python**: Python 3.9 or higher

### 2. Clone the Repository
```powershell
git clone https://github.com/undeadmoon84/DNS-changer.git
cd DNS-changer
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python main.py
```
*(Or use the legacy entry point: `python DNS.py`)*

> [!TIP]
> If you run the command in a non-admin terminal, DNS Changer will automatically request Windows Administrator elevation via UAC.

---

## ⌨️ Hotkeys & Navigation

| Key | Action | Description |
| :---: | :--- | :--- |
| **`0` - `26`** | **Quick Apply** | Sets the selected DNS on active interface, flushes cache, and exits in 1 second. |
| **`0`** | **Reset DHCP** | Reverts adapter DNS back to automatic router defaults. |
| **`B`** | **Benchmark** | Runs concurrent UDP latency queries and offers 1-click auto-connect to the fastest server. |
| **`M`** | **Custom DNS** | Opens manager to add or delete your own custom DNS servers. |
| **`S`** | **Switch Adapter** | Switch between Wi-Fi, Ethernet, VPN, or virtual adapters. |
| **`F`** | **Flush Cache** | Manually flushes Windows DNS resolver cache (`ipconfig /flushdns`). |
| **`Q`** | **Exit** | Exits the program without making any changes. |

---

## 🏎️ Real UDP DNS Benchmark

Press **`B`** from the main menu to run a live speed benchmark across all 26+ DNS servers simultaneously.

```text
              🚀 DNS Query Benchmark Results (Fastest to Slowest)              
┌───┬─────────┬──────────────────────┬────────────┬────────────────┬───────────┐
│ # │ Status  │ Provider Name        │ Category   │ Primary DNS    │   Latency │
├───┼─────────┼──────────────────────┼────────────┼────────────────┼───────────┤
│ 1 │ ⚡ FAST │ 403 Online           │ Anti-Sanc… │ 10.202.10.202  │    1.0 ms │
│ 2 │ ⚡ FAST │ Electro              │ Anti-Sanc… │ 78.157.42.100  │    1.2 ms │
│ 3 │ ⚡ FAST │ Shecan (178)         │ Anti-Sanc… │ 178.22.122.100 │    9.7 ms │
│ 4 │  ✔ OK   │ Cloudflare (1.1.1.1) │ Global & … │ 1.1.1.1        │   45.2 ms │
│ 5 │  ✔ OK   │ Google Public DNS    │ Global & … │ 8.8.8.8        │   52.1 ms │
│ 6 │ ✖ FAIL  │ SafeDNS              │ Privacy &… │ 195.46.39.39   │ Timed out │
└───┴─────────┴──────────────────────┴────────────┴────────────────┴───────────┘
```

* **⚡ FAST** (< 45 ms)
* **✔ OK** (45 – 100 ms)
* **⚠ SLOW** (> 100 ms)
* **✖ FAIL** (Timeout / No Response)

---

## 🛠️ Building Standalone Windows (.exe)

You can compile DNS Changer into a single standalone `.exe` file with the custom application icon:

### Method 1: One-Click Build Script *(Recommended)*
Simply double-click `build.bat` or run:
```cmd
build.bat
```

### Method 2: Manual PyInstaller Command
```powershell
pip install pyinstaller
pyinstaller --onefile --name "DNS-Changer" --icon="assets/DNS-Changer.ico" --clean main.py
```

The compiled standalone executable with the custom icon will be generated in `dist/DNS-Changer.exe`.

---

## 📁 Architecture & File Structure

```
DNS-changer/
├── assets/
│   └── DNS-Changer.ico  # Application icon
├── core/
│   ├── __init__.py
│   ├── network.py       # Adapter detection, netsh DNS set/clear, cache flushing, UAC elevation
│   ├── benchmark.py     # Concurrent UDP DNS query latency testing via ThreadPoolExecutor
│   └── storage.py       # Built-in presets, categories, provider matching, custom JSON storage
├── ui/
│   ├── __init__.py
│   ├── display.py       # Rich TUI formatting, status cards, 2-column tables, benchmark tables
│   └── menu.py          # Fast 1-step number dispatcher, Questionary interactive flows & hotkeys
├── main.py              # Application main entry point
├── DNS.py               # Backward-compatible wrapper
├── requirements.txt     # Dependencies (rich, questionary, dnspython, pyinstaller)
├── build.bat            # One-click Windows executable compiler with icon
├── .gitignore           # Git ignore rules (ignores dist/, build/, *.spec, *.exe)
└── README.md            # Documentation
```

---

## ❓ Troubleshooting

<details>
<summary><b>❌ Error: Failed to run command / Access Denied</b></summary>

**Reason**: Changing network adapter DNS requires Windows Administrator privileges.  
**Solution**: Right-click your terminal (or `DNS-Changer.exe`) and choose **"Run as administrator"**. If started normally, the app will automatically prompt Windows UAC elevation.
</details>

<details>
<summary><b>❌ Network adapter with spaces (e.g. "Wi-Fi" or "Ethernet 2") not working</b></summary>

**Solution**: DNS Changer Pro includes built-in quoting and whitespace parsing for all Windows adapter names, ensuring full compatibility with interfaces containing spaces.
</details>

<details>
<summary><b>❌ DNS speed benchmark times out for all servers</b></summary>

**Reason**: Some corporate firewalls or local ISPs restrict raw UDP port 53 packets.  
**Solution**: Ensure your connection allows outgoing UDP traffic on port 53, or switch to domestic anti-sanction providers (e.g., 403 Online, Shecan, Electro) which are locally accessible.
</details>

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
