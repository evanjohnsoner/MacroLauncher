import cv2
import numpy as np
import pyautogui
import threading
import tkinter as tk
import time
from pynput import keyboard
from pynput.keyboard import Controller
from mss import mss
import os
import importlib.util

# ---------- Load settings ----------
settings_path = os.path.join(os.path.dirname(__file__), "settings.py")
if os.path.exists(settings_path):
    spec = importlib.util.spec_from_file_location("settings", settings_path)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
else:
    raise FileNotFoundError("settings.py not found!")

# ---------- Parameters ----------
YELLOW_RGB = np.array(settings.YELLOW_RGB)
BLUE_RGB = np.array(settings.BLUE_RGB)
TOLERANCE = settings.TOLERANCE
X_TOLERANCE = settings.X_TOLERANCE
CLICK_COOLDOWN = settings.CLICK_COOLDOWN
SCREENSHOT_INTERVAL = settings.SCREENSHOT_INTERVAL
RECAST_TIMEOUT = 60

SCAN_X1, SCAN_Y1 = settings.SCAN_X1, settings.SCAN_Y1
SCAN_X2, SCAN_Y2 = settings.SCAN_X2, settings.SCAN_Y2
SPECIAL_COLOR = np.array(settings.SPECIAL_COLOR, dtype=np.uint8)
REG_X1, REG_Y1 = settings.REG_X1, settings.REG_Y1
REG_X2, REG_Y2 = settings.REG_X2, settings.REG_Y2
FIX_X, FIX_Y = settings.FIX_X, settings.FIX_Y

# ---------- Globals ----------
running = True
kb = Controller()

# ---------- Tkinter GUI ----------
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.3)
root.attributes("-transparentcolor", "black")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.configure(bg="black")

def stop_running():
    global running
    running = False
    root.quit()

root.protocol("WM_DELETE_WINDOW", stop_running)

def on_press(key):
    if key == keyboard.Key.f5:
        stop_running()

listener = keyboard.Listener(on_press=on_press)
listener.start()

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
canvas.place(x=0, y=0)
root.attributes("-disabled", True)

def draw_dotted_rect(x1, y1, x2, y2, dash=(5,3)):
    canvas.create_rectangle(x1, y1, x2, y2, outline="white", dash=dash, width=2)

draw_dotted_rect(SCAN_X1, SCAN_Y1, SCAN_X2, SCAN_Y2)
draw_dotted_rect(REG_X1, REG_Y1, REG_X2, REG_Y2)

# ---------- Status Label ----------
STATUS_WIDTH, STATUS_HEIGHT = 180, 30
status_canvas = tk.Canvas(root, width=STATUS_WIDTH, height=STATUS_HEIGHT, bg="black", highlightthickness=0)
status_canvas.place(x=SCAN_X1, y=SCAN_Y1 - STATUS_HEIGHT - 10)
status_text_var = tk.StringVar(value="Searching")

status_label = status_canvas.create_text(STATUS_WIDTH // 2, STATUS_HEIGHT // 2, text=status_text_var.get(), fill="white", font=("Segoe UI", 12, "bold"))

def update_status(text):
    status_text_var.set(text)
    status_canvas.itemconfig(status_label, text=text)

# ---------- Mouse Fix Thread ----------
def keep_mouse_at_position():
    while running:
        pyautogui.moveTo(FIX_X, FIX_Y)
        time.sleep(5)

mouse_thread = threading.Thread(target=keep_mouse_at_position, daemon=True)
mouse_thread.start()

# ---------- Fishing Loop ----------
def scan_fishing_loop():
    global running
    last_click_time = 0
    last_search_time = time.time()
    sct = mss()

    while running:
        start_time = time.time()
        sct_img = sct.grab(sct.monitors[0])
        frame = np.array(sct_img)[:, :, :3]
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Special color detection
        special_region = frame_bgr[REG_Y1:REG_Y2, REG_X1:REG_X2]
        mask_special = cv2.inRange(special_region, SPECIAL_COLOR, SPECIAL_COLOR)

        if np.any(mask_special):
            update_status("Recast")
            time.sleep(1)
            kb.press('e'); kb.release('e')
            time.sleep(1)
            try: pyautogui.click()
            except: pass
            time.sleep(1)
            last_search_time = time.time()
            continue

        # Yellow / Blue detection
        cropped = frame_bgr[SCAN_Y1:SCAN_Y2, SCAN_X1:SCAN_X2]

        # Yellow
        lower_y = np.clip(YELLOW_RGB - TOLERANCE, 0, 255)
        upper_y = np.clip(YELLOW_RGB + TOLERANCE, 0, 255)
        mask_y = cv2.inRange(cropped, lower_y, upper_y)
        contours_y, _ = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_x = max([cv2.boundingRect(c)[0]+cv2.boundingRect(c)[2]//2 for c in contours_y], default=None)

        # Blue
        lower_b = np.clip(BLUE_RGB - TOLERANCE, 0, 255)
        upper_b = np.clip(BLUE_RGB + TOLERANCE, 0, 255)
        mask_b = cv2.inRange(cropped, lower_b, upper_b)
        contours_b, _ = cv2.findContours(mask_b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_x = max([cv2.boundingRect(c)[0]+cv2.boundingRect(c)[2]//2 for c in contours_b], default=None)

        now = time.time()
        if yellow_x is not None and blue_x is not None:
            update_status("Tracking")
            last_search_time = time.time()
            if abs(yellow_x - blue_x) <= X_TOLERANCE and now - last_click_time >= CLICK_COOLDOWN:
                try: pyautogui.click()
                except: pass
                last_click_time = now
        else:
            update_status("Searching")

        # Auto recast if searching too long
        if now - last_search_time >= RECAST_TIMEOUT:
            update_status("Auto Recast")
            kb.press('e'); kb.release('e')
            try: pyautogui.click()
            except: pass
            last_search_time = now

        # Maintain FPS
        elapsed = time.time() - start_time
        if elapsed < SCREENSHOT_INTERVAL: time.sleep(SCREENSHOT_INTERVAL - elapsed)

# ---------- Run ----------
tracker_thread = threading.Thread(target=scan_fishing_loop, daemon=True)
tracker_thread.start()
root.mainloop()
running = False
listener.stop()
