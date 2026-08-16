# ⚡ DNS Changer Pro

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0078D6.svg?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/undeadmoon84/DNS-changer)
[![Build & Release](https://img.shields.io/badge/Release-Automated%20CI%2FCD-success.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/undeadmoon84/DNS-changer/releases)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Interface](https://img.shields.io/badge/UI-Rich%20TUI-cyan.svg?style=for-the-badge&logo=gnubash&logoColor=white)](https://github.com/Textualize/rich)
[![Speed](https://img.shields.io/badge/Startup-0.19s%20(Instant)-success.svg?style=for-the-badge)](https://github.com/undeadmoon84/DNS-changer)

**A high-speed, modern, cross-platform terminal-based DNS switcher, security auditor, speed benchmark suite, and profile manager for Windows, macOS & Linux.**  
*Switch DNS in 1 step, benchmark UDP resolution in <0.6s, audit DNS leaks & tampering, pin favorites, and automate via CLI flags.*

[Quick Start](#-quick-start) • [Features](#-key-features) • [CLI Automation](#-cli-automation--headless-mode) • [DNS Providers](#-included-dns-providers) • [Benchmark](#-real-udp-dns-benchmark) • [Leak Test](#-dns-leak--security-audit) • [Hotkeys](#-hotkeys--navigation)

</div>

---

## 📺 Terminal Interface Preview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│         ⚡ DNS CHANGER PRO ⚡                                               │
│         Instant 1-Step DNS Switcher • Low Latency & Bypass • Windows Native │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────── 📡 Live System Status ───────────────────────────┐
│       Privileges:  🛡️ Administrator                                          │
│ Active Interface:  📶 Wi-Fi                                                 │
│   Configured DNS:  178.22.122.100  |  185.51.200.2                          │
│   Active Profile:  ✨ Shecan (178)                                          │
│     Previous DNS:  1.1.1.1, 1.0.0.1 (Press [U] to revert)                   │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────┬──────────────────────────┬─────────────────┬─────┬──────────────────────────┬─────────────────┐
│   # │ Provider Name            │ Primary IP      │   # │ Provider Name            │ Primary IP      │
├─────┼──────────────────────────┼─────────────────┼─────┼──────────────────────────┼─────────────────┤
│  1. │ ⭐ Shecan (178)          │ 178.22.122.100  │ 14. │ Alternate DNS            │ 76.76.19.19     │
│  2. │ ⭐ Shecan (185)          │ 185.51.200.2    │ 15. │ Verisign                 │ 64.6.64.6       │
│  3. │ ⭐ Electro               │ 78.157.42.100   │ 16. │ Neustar UltraDNS         │ 156.154.70.1    │
│  4. │ 403 Online               │ 10.202.10.202   │ 17. │ Comodo Secure            │ 8.26.56.26      │
│  5. │ Radar Game               │ 10.202.10.10    │ 18. │ Yandex DNS               │ 77.88.8.8       │
│  6. │ Bogzar DNS               │ 185.55.226.26   │ 19. │ Dyn DNS                  │ 216.146.35.35   │
│  7. │ Gozar DNS                │ 185.55.225.25   │ 20. │ Quad9 (Malware Block)    │ 9.9.9.9         │
│  8. │ Host Iran                │ 172.29.2.100    │ 21. │ AdGuard DNS (Default)    │ 94.140.14.14    │
│  9. │ Shatel DNS               │ 85.15.1.15      │ 22. │ AdGuard DNS (Legacy)     │ 176.103.130.130 │
│ 10. │ Pishgaman DNS            │ 5.202.100.100   │ 23. │ CleanBrowsing (Security) │ 185.228.168.9   │
│ 11. │ ⭐ Cloudflare (1.1.1.1)  │ 1.1.1.1         │ 24. │ SafeDNS                  │ 195.46.39.39    │
│ 12. │ Google Public DNS        │ 8.8.8.8         │ 25. │ DNS.Watch                │ 84.200.69.80    │
│ 13. │ OpenDNS (Cisco)          │ 208.67.222.222  │ 26. │ OpenNIC                  │ 46.151.208.154  │
└─────┴──────────────────────────┴─────────────────┴─────┴──────────────────────────┴─────────────────┘
0. Reset DHCP • [U] Undo • [P] Fav Pin • [C] Current DNS • [L] Leak Test • [B] Benchmark • [M] Custom • [S] Adapter • [F] Flush • [Q] Exit

👉 Enter DNS number [0-26] or Hotkey (U/P/C/L/B/M/S/F/Q): 
```

---

## 🌟 Key Features

* ⚡ **Instant 1-Step Switching**: Type any provider number (`1`-`26` or `0` for DHCP) and hit `Enter`. DNS applies immediately, flushes cache via native Win32 API in 0.1ms, and exits automatically in 1 second.
* 🤖 **Full CLI Headless Automation**: Automate everything without opening the GUI (`--set 1`, `--auto-best`, `--clear`, `--status`, `--leak-test`, `--flush`).
* ⏪ **1-Click Undo / Revert (`[U]`)**: Automatically remembers your previous DNS configuration before every change, enabling instant rollback with `[U]`.
* ⭐ **Favorite Server Pinning (`[P]`)**: Pin your top-preferred DNS servers with golden star badges at the top of the grid.
* 🕵️ **DNS Leak & Hijack Auditor (`[L]`)**: Detects transparent ISP DNS proxying, NXDOMAIN query hijacking, and DNS response poisoning.
* 🌐 **Dual-Stack IPv6 Support**: Automatically configures corresponding IPv6 DNS addresses alongside IPv4 when IPv6 is enabled.
* 🚀 **0.59s Parallel UDP Speed Benchmark (`[B]`)**: Concurrently tests actual domain resolution latency (UDP Port 53) across 26+ servers with 1-click connect to the fastest responder.
* 🏷️ **Service & Gaming Badges**: Visual tags identifying ideal use-cases (`[🎮 Gaming]`, `[💻 Dev / Docker]`, `[⚡ Bypass]`, `[🛡️ AdBlock]`).
* 🛡️ **Zero-Friction Windows Integration**:
  * **Native Win32 C API Cache Flushing**: Direct `DnsFlushResolverCache` (0.1ms latency).
  * **Embedded UAC Admin Manifest**: Seamless elevation without duplicate console windows.
  * **Spaces-Safe Adapter Detection**: Handles interfaces with spaces (`"Wi-Fi"`, `"Local Area Connection"`).

---

## 🤖 CLI Automation & Headless Mode

DNS Changer Pro supports rich command-line arguments for scripting, scheduled tasks, and desktop shortcuts:

```powershell
# Instantly apply a preset by number
DNS-Changer.exe --set 1

# Apply by provider name (fuzzy match)
DNS-Changer.exe --set electro

# Apply custom DNS addresses directly
DNS-Changer.exe --set "1.1.1.1, 1.0.0.1"

# Silently benchmark and auto-connect to the lowest latency DNS
DNS-Changer.exe --auto-best

# Reset active adapter to DHCP (Router Default) and flush cache
DNS-Changer.exe --clear

# Print current adapter, DNS servers, and matching preset provider name
DNS-Changer.exe --current

# Print current adapter, DNS servers, and profile name to terminal
DNS-Changer.exe --status

# Run DNS leak, hijack, and tampering security audit
DNS-Changer.exe --leak-test

# Run high-speed UDP speed benchmark table
DNS-Changer.exe --benchmark

# Flush Windows DNS resolver cache directly
DNS-Changer.exe --flush

# Target a specific network interface
DNS-Changer.exe --set 1 --adapter "Ethernet"
```

---

## 🚀 Quick Start

### 📥 Option A: Standalone Executable (Recommended — No Python Needed)

#### 🪟 Windows
1. Download **`DNS-Changer-Windows.exe`** from the **[Latest GitHub Releases](https://github.com/undeadmoon84/DNS-changer/releases)**.
2. Double-click **`DNS-Changer-Windows.exe`** to run!

#### 🍎 macOS (MacBook / iMac / Mac Studio)
1. Download **`DNS-Changer-macOS-Universal.zip`** from GitHub Releases.
2. Unzip and double-click **`DNS-Changer.command`** (or run `sudo ./DNS-Changer` in Terminal).

#### 🐧 Linux (Ubuntu / Debian / Fedora / Arch)
1. Download **`DNS-Changer-Linux-x86_64`** (or `DNS-Changer-Linux.tar.gz`).
2. Make executable & run:
   ```bash
   chmod +x DNS-Changer-Linux-x86_64
   sudo ./DNS-Changer-Linux-x86_64
   ```

---

### 🛠️ Option B: Building Standalone Executable from Source

#### 🪟 Windows (`.exe` Build)
Simply double-click `build.bat` or run:
```cmd
build.bat
```
The compiled standalone executable with the custom icon will be generated in `dist/DNS-Changer.exe`.

#### 🍎 macOS (Mach-O Binary & `.command` Launcher)
Run the automated zero-config build script in Terminal:
```bash
chmod +x build.sh
./build.sh
```
*`build.sh` automatically manages an isolated virtual environment (`.build_venv`) to fully comply with modern macOS Homebrew / PEP 668 standards.*  
This outputs `dist/DNS-Changer` and a double-clickable `dist/DNS-Changer.command`!

---

### 🐍 Option C: Run from Source (Python)

#### 1. Prerequisites
- **Operating System**: Windows 10 / 11 / Windows Server OR macOS 11+ (Big Sur, Monterey, Ventura, Sonoma, Sequoia)
- **Python**: Python 3.9 or higher

#### 2. Clone the Repository
```bash
git clone https://github.com/undeadmoon84/DNS-changer.git
cd DNS-changer
```

#### 3. Setup & Run

##### 🪟 Windows:
```powershell
pip install -r requirements.txt
python main.py
```

##### 🍎 macOS (with Virtual Environment):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo python3 main.py
```
*(Or use the legacy entry point: `python DNS.py`)*

> [!TIP]
> On Windows, DNS Changer Pro automatically requests UAC Administrator elevation. On macOS, running with `sudo` gives permission to update system network services via `networksetup`.

---

## ⚡ Performance & Benchmarks

DNS Changer Pro is engineered for near-zero latency and instant execution:

| Metric / Phase | Before Optimization | After Optimization | Speedup |
| :--- | :--- | :--- | :--- |
| **Active Route & Adapter Detection** | `2,497 ms` *(Cold PowerShell)* | **`0.59 ms`** *(Native Socket Route)* | **~4,200x faster** ⚡ |
| **DNS Cache Flush** | `45 ms` *(Subprocess ipconfig)* | **`0.10 ms`** *(Native Win32 C API)* | **~450x faster** ⚡ |
| **Startup Module Imports** | `513 ms` *(Eager Load)* | **`117 ms`** *(Lazy Loading)* | **~4.4x faster** ⚡ |
| **Total Cold Startup Latency** | **`3,198 ms` (~3.2s)** | **`268 ms` (~0.26s)** | **~12x Faster (Instant Launch)** 🚀 |
| **Full 26-Server Benchmark** | `~2.2 seconds` | **`0.59 seconds`** *(26 Parallel Workers)* | **~3.7x faster** 🚀 |

---

## ⌨️ Hotkeys & Navigation

| Key | Action | Description |
| :---: | :--- | :--- |
| **`0` - `26`** | **Quick Apply** | Sets chosen DNS, flushes cache in 0.1ms, and auto-exits in 1s. |
| **`0`** | **Reset DHCP** | Reverts adapter DNS back to automatic router defaults. |
| **`U`** | **Undo / Revert** | Restores the previous DNS configuration in 1 click. |
| **`P`** | **Pin Favorites** | Toggle golden star pinned status for your preferred servers. |
| **`C`** | **Current DNS** | Inspects active DNS servers and matches against preset provider names. |
| **`L`** | **Leak Audit** | Runs comprehensive DNS leak, NXDOMAIN hijack & tampering audit. |
| **`B`** | **Benchmark** | Runs concurrent UDP latency queries and offers 1-click connect to fastest. |
| **`M`** | **Custom DNS** | Opens manager to add, edit, or delete your own custom DNS servers. |
| **`S`** | **Switch Adapter** | Switch between Wi-Fi, Ethernet, VPN, or virtual adapters. |
| **`F`** | **Flush Cache** | Manually flushes Windows DNS resolver cache via native Win32 API. |
| **`Q`** | **Exit** | Exits the program without making any changes. |

---

## 🕵️ DNS Leak & Security Audit

Press **`L`** (or run `DNS-Changer.exe --leak-test`) to run an instant security evaluation on your connection:

```text
┌──────────────────── 🕵️ DNS Leak & Security Audit Report ─────────────────────┐
│                                                                             │
│       Target Adapter:  Wi-Fi                                                │
│       Configured DNS:  1.1.1.1, 1.0.0.1                                     │
│     Security Posture:  🛡️ SECURE (Clean & Untampered)                        │
│  Resolver Responsive:  ✔ Yes                                                │
│   NXDOMAIN Hijacking:  ✔ Clean (Standard NXDOMAIN behavior)                 │
│     Domain Tampering:  ✔ Clean (Authentic query results)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏎️ Real UDP DNS Benchmark

Press **`B`** (or run `DNS-Changer.exe --benchmark`) to run a live speed benchmark across all 26+ DNS servers in 0.59s:

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

---

## 📁 Architecture & File Structure

```
DNS-changer/
├── assets/
│   └── DNS-Changer.ico  # Application icon
├── core/
│   ├── __init__.py
│   ├── cli.py           # Headless CLI argument parser & automated execution engine
│   ├── leak_test.py     # DNS leak, NXDOMAIN hijack & query tampering security auditor
│   ├── network.py       # Cross-platform network engine (Win32 / netsh & macOS networksetup)
│   ├── benchmark.py     # 26-worker parallel UDP DNS latency benchmark engine
│   └── storage.py       # Presets, badges, favorites, history tracking, custom JSON persistence
├── ui/
│   ├── __init__.py
│   ├── display.py       # Rich TUI layout, status cards, security report panels, grid rendering
│   └── menu.py          # Fast 1-step dispatcher, undo, favorite pinning, interactive menus
├── main.py              # Application entry point with CLI routing and interactive loop
├── DNS.py               # Backward-compatible wrapper
├── requirements.txt     # Dependencies (rich, questionary, dnspython, pyinstaller)
├── build.bat            # One-click Windows standalone executable builder with custom icon
├── build.sh             # One-click macOS standalone executable & .command builder
├── .gitignore           # Git ignore rules (ignores dist/, build/, *.spec, *.exe, dns_config.json)
└── README.md            # Comprehensive documentation
```

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).
