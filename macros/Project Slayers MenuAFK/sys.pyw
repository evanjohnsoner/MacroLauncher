import pyautogui
import time
import settings  # import your settings file

def main():
    x, y = settings.CLICK_POSITION
    delay = settings.CLICK_DELAY

    print(f"AFK macro started. Clicking every {delay} seconds at ({x}, {y}).")
    try:
        while True:
            pyautogui.click(x, y)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Macro stopped manually.")

if __name__ == "__main__":
    main()
