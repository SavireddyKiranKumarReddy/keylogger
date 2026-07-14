<div align="center">

# WindowsManager

### Professional Windows Keyboard Logging Demonstration

A Python-based Windows desktop application that demonstrates keyboard event capture, local log persistence, and startup integration in a controlled, educational context. The project is intended for authorized testing and internal analysis only, and should be used in strict compliance with applicable laws and organizational policies.

---

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Reference%20Project-brightgreen?style=for-the-badge)

---

</div>

## Overview

This repository provides a reference implementation of a Windows application that can:

- capture keyboard events system-wide
- format special keys into readable text
- write output to daily log files
- register itself for automatic startup
- display a first-run notification window

The implementation is meant to serve as an educational example of how such behavior can be built in Python on Windows.

## Key Features

- System-wide keyboard event capture
- Daily log file rotation
- Local-only file storage
- Windows startup registration support
- First-run user notification UI
- Plain-text log output for inspection

## Technology Stack

| Category | Technology | Purpose |
|:---|:---|:---|
| Language | Python | Core application logic |
| Keyboard Hooking | pynput | Capture keyboard events on Windows |
| GUI | tkinter | Display the first-run notification window |
| Persistence | Windows Registry | Optional startup registration |
| Packaging | PyInstaller | Build a standalone Windows executable |

## Project Structure

```text
Keylogger/
├── keylog.py           # Main application logic
├── Keylog.spec        # PyInstaller build configuration
├── build/             # Build artifacts
├── dist/              # Output executable directory
└── README.md          # Project documentation
```

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- pip

## Installation

```bash
cd Keylogger
pip install pynput pyinstaller
```

## Build Instructions

```bash
python -m PyInstaller Keylog.spec --noconfirm
```

The executable will be generated in the dist directory.

## Usage

Run the script directly:

```bash
python keylog.py
```

Or launch the compiled executable:

```powershell
dist\WindowsManager.exe
```

## Application Flow

1. The application starts and prepares its log directory.
2. It optionally registers itself for startup through the Windows Run key.
3. On first launch, it may display a brief notification window.
4. A keyboard listener is started to capture events.
5. Each event is written to a daily text log file.

## Configuration

The core configuration values are defined in the source file:

```python
LOG_BASE_DIR = os.path.join(os.environ['APPDATA'], "Windows Manager Logs")
STARTUP_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "WindowsSecurityService"
FLAG_FILE = os.path.join(LOG_BASE_DIR, ".initialized")
```

## Responsible Use

This project is provided strictly for educational, research, and authorized testing purposes. It must not be used to collect information without clear authorization or in violation of any applicable law, policy, or contractual obligation.

Recommended practices:

- use only in a controlled environment
- obtain explicit authorization before testing
- store logs locally and securely
- remove startup entries and generated files after testing

## Security Notes

- The implementation uses Windows-specific behavior and may trigger security warnings on some systems.
- The project is not intended for stealth deployment or unauthorized monitoring.
- Any runtime behavior should be reviewed carefully before execution.

## License

This project is provided for educational and research purposes only. Use it responsibly and lawfully.

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
