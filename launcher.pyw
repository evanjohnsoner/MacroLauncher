import customtkinter as ctk
import subprocess
import os
import sys
import random
import string
import requests
import uuid
from pathlib import Path
from dotenv import load_dotenv, set_key
import ctypes
import time
import threading
import pywinstyles


# ==========================================================
#  PATH DETECTION (works both as .pyw and compiled .exe)
# ==========================================================
if getattr(sys, "frozen", False):
    LAUNCHER_ROOT = os.path.dirname(sys.executable)
else:
    LAUNCHER_ROOT = os.path.dirname(os.path.abspath(__file__))

SYS_FOLDER = os.path.join(LAUNCHER_ROOT, "sys")
os.makedirs(SYS_FOLDER, exist_ok=True)

# ------------------ FILE PATHS ------------------
ENV_FILE = os.path.join(SYS_FOLDER, ".env")
COMPILER_PATH = os.path.join(LAUNCHER_ROOT, "compiler.pyw")
COMPILER_FALLBACK = os.path.join(LAUNCHER_ROOT, "compiler.py")
LAUNCH_TOKEN_FILE = os.path.join(SYS_FOLDER, "launch_token.txt")
BAT_FILE = os.path.join(SYS_FOLDER, "install_requirements.bat")
LOCAL_VERSION_FILE = os.path.join(SYS_FOLDER, "itm.py")

# ------------------ FIREBASE CONFIG ------------------
FIREBASE_URL = "https://pythonmacrolauncher-default-rtdb.firebaseio.com/"
VERSION_PATH = f"{FIREBASE_URL}/version/version.json"
LICENSES_PATH = f"{FIREBASE_URL}/licenses.json"
SYS_KEY = "Lz3USHU9UrIsaxqEagf7DmGdLYors6LWFbtGiIwO"

# ==========================================================
#  LOAD .env
# ==========================================================
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
saved_key = os.getenv("SAVED_KEY", "")

# ==========================================================
#  LOCAL VERSION
# ==========================================================
local_version = "v0.0"
if os.path.exists(LOCAL_VERSION_FILE):
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            for line in f:
                if line.strip().startswith("VERSION"):
                    parts = line.split("=")
                    if len(parts) > 1:
                        val = parts[1].strip().strip('"').strip("'")
                        if val:
                            local_version = val
                            break
    except Exception:
        pass

# ==========================================================
#  FIREBASE CONNECTION
# ==========================================================
firebase_connected = False
supported_version = local_version
try:
    resp = requests.get(VERSION_PATH, params={"auth": SYS_KEY}, timeout=5)
    resp.raise_for_status()
    remote_version = resp.json()
    if remote_version:
        supported_version = remote_version
    firebase_connected = True
except requests.RequestException:
    firebase_connected = False

# ==========================================================
#  GUI SETUP (safe theme loading)
# ==========================================================
import customtkinter

ctk.set_appearance_mode("dark")

if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
    theme_path = os.path.join(base_path, "customtkinter", "assets", "themes", "dark-blue.json")
else:
    theme_path = os.path.join(os.path.dirname(customtkinter.__file__), "assets", "themes", "dark-blue.json")

if os.path.exists(theme_path):
    ctk.set_default_color_theme(theme_path)
else:
    ctk.set_default_color_theme("blue")  # fallback theme

root = ctk.CTk()
root.title(f"Macro Launcher {local_version}")
root.geometry("480x225")
root.resizable(False, False)

# Acrylic effect
try:
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    pywinstyles.apply_style(hwnd, style="Acrylic", color="#1e1e1e", opacity=0.85)
except Exception:
    pass

# ==========================================================
#  LOADING FRAME
# ==========================================================
loading_frame = ctk.CTkFrame(root, fg_color="#1e1e1e")
loading_frame.pack(expand=True, fill="both")
loading_frame.pack_propagate(False)

ctk.CTkFrame(loading_frame, fg_color="#1e1e1e", height=60).pack()

loading_label = ctk.CTkLabel(
    loading_frame,
    text="Checking dependencies...",
    font=("Segoe UI", 16, "bold"),
    text_color="#4d79ff",
)
loading_label.pack(pady=(0, 10))

progress_var = ctk.DoubleVar()
progress_bar = ctk.CTkProgressBar(
    loading_frame, variable=progress_var, width=400, progress_color="#4d79ff", fg_color="#2a2a2a"
)
progress_bar.pack(pady=(0, 5))

loader_status = ctk.CTkLabel(
    loading_frame, text="Initializing...", font=("Segoe UI", 10), text_color="grey"
)
loader_status.pack(pady=(0, 40))

root.update()


# ==========================================================
#  SMART DEPENDENCY CHECK
# ==========================================================
def check_dependencies():
    """Check if required Python packages are installed."""
    required = ["customtkinter", "psutil", "requests", "python-dotenv", "pywinstyles"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    return missing


def run_installer():
    """Run the .bat installer if dependencies are missing."""
    global process
    if not os.path.exists(BAT_FILE):
        loader_status.configure(text="Installer not found!", text_color="red")
        time.sleep(0.5)
        root.after(300, show_main_ui)
        return

    loader_status.configure(text="Installing missing dependencies...", text_color="grey")
    process = subprocess.Popen(
        [BAT_FILE],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    threading.Thread(target=smooth_progress, daemon=True).start()


def smooth_progress():
    """Smooth animated progress bar while installing."""
    while process.poll() is None:
        val = progress_var.get()
        if val < 0.95:
            progress_var.set(val + 0.003)
        root.update_idletasks()
        time.sleep(0.05)
    progress_var.set(1.0)
    loader_status.configure(text="Dependencies installed!", text_color="#4d79ff")
    time.sleep(0.5)
    root.after(300, show_main_ui)


def check_and_run():
    """Check if dependencies are missing before running installer."""
    missing = check_dependencies()
    if missing:
        loader_status.configure(text=f"Missing modules: {', '.join(missing)}", text_color="grey")
        run_installer()
    else:
        loader_status.configure(text="All dependencies already installed!", text_color="#4d79ff")
        progress_var.set(1.0)
        time.sleep(0.5)
        root.after(300, show_main_ui)


# ==========================================================
#  MAIN UI
# ==========================================================
def show_main_ui():
    loading_frame.pack_forget()

    header_label = ctk.CTkLabel(
        root, text=f"Macro Launcher {local_version}", font=("Segoe UI", 16, "bold"), text_color="#4d79ff"
    )
    header_label.pack(pady=(15, 15))

    version_label = ctk.CTkLabel(
        root,
        text=f"Current Version: {local_version} | Supported: {supported_version}",
        font=("Segoe UI", 12),
        text_color="grey",
    )
    version_label.pack(pady=(0, 10))

    key_entry = ctk.CTkEntry(
        root,
        placeholder_text="Enter Access Key",
        width=300,
        fg_color="#2a2a2a",
        border_width=1,
        border_color="#444",
        text_color="white",
    )
    key_entry.pack(pady=(0, 10))
    if saved_key:
        key_entry.insert(0, saved_key)

    def generate_token(length=32):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_hwid():
        return str(uuid.getnode())

    def check_key(key):
        try:
            resp = requests.get(LICENSES_PATH, params={"auth": SYS_KEY}, timeout=5)
            resp.raise_for_status()
            licenses = resp.json() or {}
            hwid = get_hwid()
            for lic_id, data in licenses.items():
                if data.get("Key") == key:
                    stored_hwid = data.get("HWID")
                    if not stored_hwid:
                        data["HWID"] = hwid
                        requests.patch(f"{FIREBASE_URL}/licenses/{lic_id}.json", params={"auth": SYS_KEY}, json=data)
                        return True, f"Key accepted, assigned to HWID {hwid}"
                    elif stored_hwid == hwid:
                        return True, "Key accepted (HWID match)"
                    else:
                        return False, "HWID mismatch!"
            return False, "Invalid Key"
        except requests.RequestException:
            return False, "Unable to connect to server!"

    def launch_compiler():
        key = key_entry.get().strip()
        if local_version != supported_version:
            status_label.configure(text="Unsupported version!", text_color="red")
            return

        valid, msg = check_key(key)
        if not valid:
            status_label.configure(text=msg, text_color="red")
            return

        if not os.path.exists(ENV_FILE):
            Path(ENV_FILE).touch()
        set_key(ENV_FILE, "SAVED_KEY", key)

        path_to_run = COMPILER_PATH if os.path.exists(COMPILER_PATH) else (
            COMPILER_FALLBACK if os.path.exists(COMPILER_FALLBACK) else None
        )

        if not path_to_run:
            status_label.configure(text="Compiler not found!", text_color="red")
            return

        token = generate_token()
        with open(LAUNCH_TOKEN_FILE, "w") as f:
            f.write(token)

        status_label.configure(text="Launching Compiler...", text_color="#4d79ff")
        subprocess.Popen([sys.executable, path_to_run, token], close_fds=True)
        root.destroy()

    launch_btn = ctk.CTkButton(
        root,
        text="Launch",
        command=launch_compiler,
        fg_color="#2a2a2a",
        hover_color="#444444",
        text_color="#4d79ff",
        border_width=1,
        border_color="#444",
    )
    launch_btn.pack(pady=(5, 5))

    global status_label
    status_label = ctk.CTkLabel(root, text="", font=("Segoe UI", 12, "bold"), text_color="#4d79ff")
    status_label.pack(pady=(5, 15))

    if not firebase_connected:
        status_label.configure(text="Cannot connect to Server", text_color="red")
    elif local_version != supported_version:
        status_label.configure(text="Version not Supported", text_color="red")
    else:
        status_label.configure(text="Connected to Server", text_color="#4d79ff")


# ==========================================================
#  RUN INSTALL CHECK
# ==========================================================
threading.Thread(target=check_and_run, daemon=True).start()

# ==========================================================
#  MAIN LOOP
# ==========================================================
root.mainloop()
