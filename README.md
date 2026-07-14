<div align="center">

# WindowsManager

### Advanced Keystroke Logging & Monitoring Framework

A lightweight, stealth-capable keystroke monitoring tool built for Windows systems.
Captures all keyboard input system-wide, organizes logs by date hierarchy, and persists across reboots — all from a single executable with zero configuration.

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Build](https://img.shields.io/badge/Build-PyInstaller-red?style=for-the-badge)

---

</div>

## Technologies Used

| Category | Technology | Purpose |
|:---|:---|:---|
| **Language** | Python 3.14 | Core runtime and logic |
| **Keyboard Hooking** | [pynput](https://pypi.org/project/pynput/) | Global low-level keyboard event capture via Windows API |
| **GUI Framework** | tkinter | First-run notification popup (built-in, no extra dependency) |
| **Persistence** | Windows Registry (WinReg) | Auto-start on boot via `HKCU\...\Run` |
| **Build System** | [PyInstaller](https://pyinstaller.org/) | Compiles Python to standalone `.exe` binary |
| **Threading** | Python threading | Concurrent keylogger listener on separate thread |
| **Keep-Alive** | `threading.Event` | Blocks main thread to keep process running |
| **File I/O** | UTF-8 File Streams | Daily log rotation and keystroke storage |

---

## Architecture

```
                    ┌──────────────────────────────┐
                    │     WindowsManager.exe        │
                    │     (console=False)            │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
            ┌───────▼───────┐            ┌─────────▼─────────┐
            │  Registry      │            │  Log Directory     │
            │  Persistence   │            │  Creation          │
            │  (HKCU\Run)   │            │  (%APPDATA%\...)   │
            └───────────────┘            └─────────┬─────────┘
                                                   │
                                      ┌────────────▼────────────┐
                                      │   First Run Check       │
                                      │   (.initialized flag)   │
                                      └────────────┬────────────┘
                                            ┌──────┴──────┐
                                      YES   │             │  NO
                                   ┌────────▼──────┐      │
                                   │  GUI Popup    │      │
                                   │  (tkinter)    │      │
                                   │  Show & Close │      │
                                   └────────┬──────┘      │
                                            │             │
                                            └──────┬──────┘
                                                   │
                                      ┌────────────▼────────────┐
                                      │  Keyboard Listener      │
                                      │  (pynput, separate      │
                                      │   thread + Event wait)  │
                                      └────────────┬────────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────────┐
                                      │  Daily .txt Log         │
                                      │  (Plain Text, UTF-8)    │
                                      │  Runs forever silently  │
                                      └────────────────────────┘
```

---

## Features

- **System-Wide Capture** — Records keystrokes across every application, window, and input field
- **Zero-Privilege Execution** — Runs entirely on standard user permissions (no admin required)
- **Boot Persistence** — Self-registers in Windows Registry for automatic startup on login
- **Completely Silent** — No console window, no flash, zero visible UI after first run
- **First-Run GUI** — Professional notification popup shown only once; invisible on all subsequent starts
- **Date-Organized Logs** — Automatic `Year > Month > Day.txt` folder hierarchy
- **Daily Auto-Rotation** — New `.txt` file created for each calendar day automatically
- **Plain Text Format** — Human-readable output with labeled special keys
- **Single Executable** — Fully self-contained `.exe` — no dependencies, no installation

---

## Project Structure

```
WindowsManager/
│
├── keylog.py                 # Core application source code
├── Keylog.spec               # PyInstaller build configuration (console=False)
│
├── dist/
│   └── WindowsManager.exe    # Compiled standalone executable
│
├── build/                    # PyInstaller intermediate build artifacts
│   └── Keylog/
│
└── README.md                 # Documentation
```

---

## Getting Started

### Prerequisites

- **OS:** Windows 10 or Windows 11
- **Python:** 3.10 or higher
- **pip:** Python package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/WindowsManager.git
cd WindowsManager

# Install dependencies
pip install pynput pyinstaller
```

### Building the Executable

```bash
python -m PyInstaller Keylog.spec --noconfirm
```

The compiled executable will be available at:
```
dist\WindowsManager.exe
```

### Running

```bash
# Option 1: Run directly with Python
python keylog.py

# Option 2: Run the compiled executable
dist\WindowsManager.exe
```

---

## How It Works

### Execution Flow

| Step | Action | Detail |
|:----:|:-------|:-------|
| 1 | **Launch** | User double-clicks `WindowsManager.exe` |
| 2 | **Registry Write** | Adds entry to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` |
| 3 | **Directory Setup** | Creates `%APPDATA%\Windows Manager Logs\{Year}\{Month}\` |
| 4 | **File Creation** | Generates today's log file: `DD-MM-YYYY.txt` |
| 5 | **First Run Check** | Reads `.initialized` flag file to determine if GUI should show |
| 6 | **GUI Display** | *(First run only)* Shows professional notification popup |
| 7 | **Flag Set** | Creates `.initialized` file — GUI will never show again |
| 8 | **Keyboard Hook** | Starts `pynput` keyboard listener on a separate thread |
| 9 | **Keep-Alive** | Main thread blocks on `threading.Event.wait()` — process stays alive forever |
| 10 | **Silent Operation** | All keystrokes written to daily `.txt` file silently |

### First Launch vs. Subsequent Boots

```
FIRST LAUNCH:
  exe runs
  → registry entry created
  → log directory created
  → .initialized does NOT exist → GUI shown
  → user clicks Close
  → .initialized created
  → keyboard listener starts
  → completely silent from here

SUBSEQUENT BOOT (after restart):
  Windows reads HKCU\Run
  → exe launches silently (no console, no window)
  → registry entry refreshed
  → log directory created
  → .initialized EXISTS → GUI skipped
  → keyboard listener starts immediately
  → completely silent — zero visible UI
```

---

## Log Storage

### Directory Structure

```
%APPDATA%\Windows Manager Logs\
│
├── .initialized               # Flag file — marks first run complete
│
├── 2025\
│   ├── January\
│   │   ├── 01-01-2025.txt
│   │   ├── 15-01-2025.txt
│   │   └── 31-01-2025.txt
│   ├── February\
│   │   └── ...
│   └── December\
│       └── ...
│
├── 2026\
│   ├── January\
│   │   └── ...
│   └── July\
│       ├── 14-07-2026.txt
│       ├── 15-07-2026.txt
│       └── 31-07-2026.txt
│
└── 2027\
    └── ...
```

### Log Format

Each daily file contains raw keystrokes in plain text:

```
hello world[BACKSPACE]world! this is a test
[SHIFT]hello[CTRL]v[ENTER]
password123[TAB]username[ENTER]
```

### Key Mapping Reference

| Keystroke | Stored As | Keystroke | Stored As |
|:----------|:----------|:----------|:----------|
| `a-z, 0-9` | As typed | `Space` | ` ` (space) |
| `Enter` | New line | `Tab` | Tab character |
| `Backspace` | `[BACKSPACE]` | `Delete` | `[DELETE]` |
| `Shift` | `[SHIFT]` | `Ctrl` | `[CTRL]` |
| `Alt` | `[ALT]` | `Esc` | `[ESC]` |
| `F1-F12` | `[F1]`–`[F12]` | `Win` | `[WIN]` |
| `↑↓←→` | `[UP]` `[DOWN]` `[LEFT]` `[RIGHT]` | | |
| `CapsLock` | `[CAPSLOCK]` | `PrintScreen` | `[PRTSC]` |
| `Insert` | `[INS]` | `Home/End` | `[HOME]` `[END]` |
| `PageUp/Down` | `[PGUP]` `[PGDN]` | `NumLock` | `[NUMLOCK]` |

---

## GUI Interface

On **first launch only**, a centered notification window is displayed:

```
┌───────────────────────────────────────────┐
│  WindowsManager                        [X]│  ← Blue title bar (#0078D4)
├───────────────────────────────────────────┤
│                                           │
│                   [ ✔ ]                   │  ← Green checkmark icon
│                                           │
│             WindowsManager                │  ← Bold heading
│   has been enabled successfully.          │
│   System protection is now active.        │  ← Subtitle
│                                           │
│              [  Close  ]                  │  ← Blue action button
│                                           │
└───────────────────────────────────────────┘
```

**Specifications:**
- Window Size: `420 x 260` pixels
- Position: Centered on primary display
- Title Bar: `#0078D4` (Windows Blue) with white text
- Always-on-top: Enabled
- Frameless: No window chrome, custom title bar
- Dismissal: Close button or X button
- **Shown only once** — subsequent runs are fully invisible

---

## Registry Persistence

### Key Location

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
    ├── Name:     WindowsSecurityService
    ├── Type:     REG_SZ
    └── Value:    "C:\path\to\WindowsManager.exe"
```

### Why This Key?

| Property | Detail |
|:---------|:-------|
| **Hive** | `HKCU` (Current User) — no elevated privileges needed |
| **Behavior** | Windows executes the value on every user login |
| **Survivability** | Persists across restarts, sleep, and hibernate |
| **Stealth** | Standard Windows mechanism — not flagged by most AV |
| **Removal** | Manual deletion via `reg delete` or Registry Editor |

---

## Removal & Cleanup

### Complete Removal Script

```powershell
# Step 1: Kill the running process
taskkill /F /IM WindowsManager.exe

# Step 2: Remove the startup registry entry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v WindowsSecurityService /f

# Step 3: Delete all log files
rmdir /S /Q "%APPDATA%\Windows Manager Logs"

# Step 4: Delete the executable
del "C:\path\to\WindowsManager.exe"
```

### Verify Removal

```powershell
# Confirm registry entry is removed
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v WindowsSecurityService
# Expected: "The system was unable to find the specified registry key or value."

# Confirm logs are deleted
dir "%APPDATA%\Windows Manager Logs"
# Expected: "The system cannot find the path specified."
```

---

## Configuration

All configuration is defined in `keylog.py`:

```python
LOG_BASE_DIR = os.path.join(os.environ['APPDATA'], "Windows Manager Logs")
STARTUP_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "WindowsSecurityService"
FLAG_FILE = os.path.join(LOG_BASE_DIR, ".initialized")
```

### Customization Options

| Variable | Default | Description |
|:---------|:--------|:------------|
| `LOG_BASE_DIR` | `%APPDATA%\Windows Manager Logs` | Base path for all log storage |
| `APP_NAME` | `WindowsSecurityService` | Registry entry name for persistence |
| `STARTUP_REG_KEY` | `HKCU\...\Run` | Registry key for auto-start |
| `FLAG_FILE` | `.initialized` in log dir | First-run detection flag file |

---

## Technical Specifications

| Component | Detail |
|:----------|:-------|
| **Language** | Python 3.14 |
| **Keyboard Library** | pynput 1.8.2 |
| **Build Tool** | PyInstaller 6.21.0 |
| **Target Platform** | Windows 10 / 11 (x64) |
| **Executable Type** | Windowed Application (`console=False`) |
| **Bootloader** | `runw.exe` (Windows subsystem, no console) |
| **Registry Hive** | HKCU (per-user, no admin required) |
| **GUI Framework** | tkinter (built-in, first run only) |
| **Log Encoding** | UTF-8 |
| **Exe Name** | `WindowsManager.exe` |
| **Registry Value** | `WindowsSecurityService` |
| **Log Path** | `%APPDATA%\Windows Manager Logs\` |
| **Keep-Alive** | `threading.Event.wait()` (blocks main thread) |
| **Listener** | `pynput.keyboard.Listener` on separate daemon thread |
| **First-Run Flag** | `.initialized` file in log directory |

---

## Security Notes

- The executable is **unsigned** — Windows SmartScreen may display a warning on first run
- Some antivirus software may flag the binary due to keyboard hooking behavior
- The process name `WindowsManager` is designed to blend with legitimate Windows processes
- All data is stored locally — no network transmission is implemented
- **Zero visible UI** after first run — no console, no window, no Task Manager tray icon

---

## License

This project is provided **for educational purposes only**. See [Disclaimer](#disclaimer) below.

---

## Disclaimer

> **IMPORTANT — READ BEFORE USE**

This software is provided **strictly for educational and authorized security testing purposes only**. By downloading, building, deploying, or using this software, you explicitly acknowledge and agree to the following:

1. **Authorized Use Only** — You must obtain explicit written permission from the owner of any system on which this software is deployed. Unauthorized interception of keystrokes, credentials, or any user input constitutes a criminal offense in most jurisdictions worldwide.

2. **Educational Purpose** — This project is designed solely to demonstrate and teach concepts related to:
   - Windows Registry persistence mechanisms
   - Low-level keyboard hooking via the Windows API
   - Python-based system monitoring and process management
   - Executable compilation and stealth techniques

3. **Legal Compliance** — You are solely responsible for ensuring that your use of this software complies with all applicable laws, including but not limited to:
   - The Computer Fraud and Abuse Act (CFAA) — United States
   - The Computer Misuse Act 1990 — United Kingdom
   - General Data Protection Regulation (GDPR) — European Union
   - Equivalent legislation in your jurisdiction

4. **No Liability** — The author assumes **no responsibility** for any damages, legal proceedings, or consequences resulting from the use or misuse of this software. The software is provided **"as is"** without warranty of any kind.

5. **No Malicious Use** — This tool must **never** be used for:
   - Credential theft or identity fraud
   - Unauthorized surveillance or espionage
   - Harassment, stalking, or invasion of privacy
   - Any activity that violates applicable laws

**By using this software, you accept full legal and moral responsibility for your actions. The author and contributors bear no liability for misuse.**

---

<div align="center">

**Built with Python**

*For educational and authorized security testing purposes only.*

</div>
