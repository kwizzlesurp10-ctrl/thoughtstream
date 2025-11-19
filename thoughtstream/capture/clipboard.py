import pyperclip
import time
import asyncio
from ..db import db

async def monitor_clipboard():
    last_content = ""
    while True:
        try:
            content = pyperclip.paste()
            if content != last_content:
                last_content = content
                # Only capture if explicitly requested? 
                # README says "Voluntary Clipboard: Manual capture on demand"
                # But also "monitor". 
                # Let's assume we just track it for now or wait for a signal.
                pass
        except Exception:
            pass
        await asyncio.sleep(1)

def capture_now():
    content = pyperclip.paste()
    if content:
        db.add_entry("clipboard", content)
        print("Clipboard captured.")

