import customtkinter as ctk
import subprocess
import os
import platform
import psutil
import sys
import ctypes
import pywinstyles

LAUNCHER_ROOT = os.path.dirname(os.path.abspath(__file__))
SYS_FOLDER = os.path.join(LAUNCHER_ROOT, "sys")
TOKEN_FILE = os.path.join(SYS_FOLDER, "launch_token.txt")
LOCAL_VERSION_FILE = os.path.join(SYS_FOLDER, "itm.py")

local_version = "ERROR"
if os.path.exists(LOCAL_VERSION_FILE):
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("VERSION") and "=" in line:
                    parts = line.split("=")
                    version_candidate = parts[1].strip().strip('"').strip("'")
                    if version_candidate:
                        local_version = version_candidate
                        break
    except Exception:
        pass

if len(sys.argv) < 2:
    print("Access Denied — Please launch through the official launcher.")
    sys.exit()

given_token = sys.argv[1].strip()
if not os.path.exists(TOKEN_FILE):
    print("Access Denied — Invalid launch path.")
    sys.exit()

with open(TOKEN_FILE, "r") as f:
    valid_token = f.read().strip()

if given_token != valid_token:
    print("Access Denied — Invalid or expired token.")
    sys.exit()

try:
    os.remove(TOKEN_FILE)
except:
    pass

ctk.set_appearance_mode("dark")
try:
    ctk.set_default_color_theme("dark-blue")
except FileNotFoundError:
    ctk.set_default_color_theme("dark")  # fallback if theme missing


root = ctk.CTk()
root.title(f"Macro Launcher {local_version}")
root.geometry("600x450")
root.resizable(False, False)

root.attributes("-topmost", True)

class WINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_uint),
        ("flags", ctypes.c_uint),
        ("showCmd", ctypes.c_uint),
        ("ptMinPosition", ctypes.wintypes.POINT),
        ("ptMaxPosition", ctypes.wintypes.POINT),
        ("rcNormalPosition", ctypes.wintypes.RECT)
    ]

ctypes.wintypes.WINDOWPLACEMENT = WINDOWPLACEMENT

def check_minimize():
    placement = WINDOWPLACEMENT()
    placement.length = ctypes.sizeof(placement)
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.user32.GetWindowPlacement(hwnd, ctypes.byref(placement))
    if placement.showCmd == 2:  # 2 = minimized
        root.attributes("-topmost", False)
    else:
        root.attributes("-topmost", True)
    root.after(500, check_minimize)

check_minimize()

hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
try:
    pywinstyles.apply_style(hwnd, style="Acrylic", opacity=0.85)
except Exception:
    pass

header_label = ctk.CTkLabel(
    root,
    text=f"Macro Launcher {local_version}",
    font=("Segoe UI", 18, "bold"),
    text_color="#4d79ff"
)
header_label.pack(pady=(15, 5))

notebook = ctk.CTkTabview(root)
notebook.pack(expand=True, fill="both", padx=20, pady=(10, 20))

notebook.add("Macros")
notebook.add("Instructions")
notebook.add("Settings")
notebook.add("Info")

macro_tab = notebook.tab("Macros")
macro_buttons = {}
macro_processes = {}

macro_frame = ctk.CTkScrollableFrame(
    macro_tab,
    scrollbar_button_color="#2a2a2a",
    scrollbar_button_hover_color="#4d79ff"
)
macro_frame.pack(expand=True, fill="both", padx=5, pady=5)

macros_folder = os.path.join(LAUNCHER_ROOT, "macros")
macro_list = []

if os.path.exists(macros_folder):
    for folder_name in os.listdir(macros_folder):
        folder_path = os.path.join(macros_folder, folder_name)
        if os.path.isdir(folder_path):
            pyw_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pyw")]
            if pyw_files:
                chosen_file = pyw_files[0]
                macro_list.append({
                    "name": folder_name,
                    "folder": folder_path,
                    "file": chosen_file
                })

def kill_process_by_name(name):
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == name.lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

for macro in macro_list:
    frame = ctk.CTkFrame(macro_frame, fg_color="#2a2a2a", corner_radius=8, border_width=0)
    frame.pack(fill="x", padx=10, pady=5)

    label = ctk.CTkLabel(frame, text=macro["name"], font=("Segoe UI", 14), text_color="white")
    label.pack(side="left", padx=10, pady=5)

    def toggle_macro(macro_name=macro["name"], macro_file=macro["file"], macro_folder=macro["folder"]):
        current = macro_buttons[macro_name].cget("text")
        script_path = os.path.join(macro_folder, macro_file)

        if current.startswith("Start"):
            macro_buttons[macro_name].configure(text="Stop Macro")
            if not os.path.exists(script_path):
                print(f"File not found: {script_path}")
                return
            proc = subprocess.Popen([sys.executable, script_path, given_token], close_fds=True)
            macro_processes[macro_name] = proc
        else:
            macro_buttons[macro_name].configure(text="Start Macro")
            if macro_name in macro_processes:
                proc = macro_processes[macro_name]
                try:
                    proc.terminate()
                except Exception:
                    pass
                macro_processes.pop(macro_name, None)

    btn = ctk.CTkButton(frame, text="Start Macro", fg_color="#2a2a2a", hover_color="#4d79ff",
                        text_color="white", corner_radius=10, command=toggle_macro)
    btn.pack(side="right", padx=10)
    macro_buttons[macro["name"]] = btn

instructions_tab = notebook.tab("Instructions")
instructions_frame = ctk.CTkScrollableFrame(
    instructions_tab,
    scrollbar_button_color="#2a2a2a",
    scrollbar_button_hover_color="#4d79ff"
)
instructions_frame.pack(expand=True, fill="both", padx=5, pady=5)

for macro in macro_list:
    instruct_txt = os.path.join(macro["folder"], "instruct.txt")
    if os.path.exists(instruct_txt):
        with open(instruct_txt, "r", encoding="utf-8") as f:
            link = f.read().strip()

        frame = ctk.CTkFrame(instructions_frame, fg_color="#2a2a2a", corner_radius=8, border_width=0)
        frame.pack(fill="x", padx=10, pady=5)

        label = ctk.CTkLabel(frame, text=macro["name"], font=("Segoe UI", 14), text_color="white")
        label.pack(side="left", padx=10, pady=5)

        def open_link(url=link):
            import webbrowser
            webbrowser.open(url)

        btn = ctk.CTkButton(frame, text="Open Instructions", fg_color="#2a2a2a",
                            hover_color="#4d79ff", text_color="white", corner_radius=10, command=open_link)
        btn.pack(side="right", padx=10)

settings_tab = notebook.tab("Settings")
settings_frame = ctk.CTkScrollableFrame(
    settings_tab,
    scrollbar_button_color="#2a2a2a",
    scrollbar_button_hover_color="#4d79ff"
)
settings_frame.pack(expand=True, fill="both", padx=5, pady=5)

for macro in macro_list:
    settings_file = os.path.join(macro["folder"], "settings.py")
    if os.path.exists(settings_file):
        collapse_btn = ctk.CTkButton(settings_frame, text=macro["name"], fg_color="#2a2a2a",
                                     hover_color="#4d79ff", text_color="white", corner_radius=5)
        collapse_btn.pack(fill="x", padx=10, pady=(5, 0))

        frame = ctk.CTkFrame(settings_frame, fg_color="#1e1e1e", corner_radius=5, border_width=0)
        frame.pack_forget()

        variables = {}
        with open(settings_file, "r") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    parts = line.split("=")
                    var_name = parts[0].strip()
                    var_value = "=".join(parts[1:]).strip()
                    variables[var_name] = var_value

        entries = {}
        for var_name, var_value in variables.items():
            entry_frame = ctk.CTkFrame(frame, fg_color="#1e1e1e", corner_radius=5, border_width=0)
            entry_frame.pack(fill="x", padx=5, pady=3)

            label = ctk.CTkLabel(entry_frame, text=var_name, text_color="white")
            label.pack(side="left", padx=5, pady=2)

            entry = ctk.CTkEntry(entry_frame, width=100, fg_color="#1e1e1e", text_color="white",
                                 border_width=0)
            entry.insert(0, var_value)
            entry.pack(side="right", padx=5, pady=2)
            entries[var_name] = entry

        def save_settings(macro_name=macro["name"], settings_file=settings_file, entries=entries):
            with open(settings_file, "w") as f:
                for var_name, entry_widget in entries.items():
                    f.write(f"{var_name} = {entry_widget.get()}\n")
            print(f"Saved settings for {macro_name}")

        save_btn = ctk.CTkButton(frame, text="Save Settings", fg_color="#4d79ff", command=save_settings)
        save_btn.pack(pady=5)

        def toggle_collapse(btn=collapse_btn, frame=frame):
            if frame.winfo_ismapped():
                frame.pack_forget()
                btn.configure(fg_color="#2a2a2a")
            else:
                frame.pack(after=btn, fill="x", padx=10, pady=5)
                btn.configure(fg_color="#4d79ff")

        collapse_btn.configure(command=toggle_collapse)

info_tab = notebook.tab("Info")
info_text = (
    f"Macro Launcher {local_version}\n"
    "Date Updated: 10/18/2025\n"
    "Built by Ak"
)
info_label = ctk.CTkLabel(info_tab, text=info_text, font=("Segoe UI", 14),
                          text_color="grey", justify="center")
info_label.pack(expand=True)

root.mainloop()
