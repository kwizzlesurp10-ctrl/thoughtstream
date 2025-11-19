from pynput import keyboard
from .clipboard import capture_now

def on_activate():
    capture_now()

def start_hotkeys():
    # Super+Shift+N
    # Note: 'cmd' or 'win' key is usually Key.cmd
    try:
        with keyboard.GlobalHotKeys({
                '<cmd>+<shift>+n': on_activate,
                '<ctrl>+<shift>+n': on_activate # Fallback
            }) as h:
            h.join()
    except Exception as e:
        print(f"Hotkey error: {e}")

