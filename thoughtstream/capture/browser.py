import asyncio
import sys
import subprocess

async def monitor_browser():
    while True:
        if sys.platform == "linux":
            try:
                # xdotool getwindowfocus getwindowname
                result = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"])
                title = result.decode().strip()
                # Log title if changed
            except Exception:
                pass
        await asyncio.sleep(5)

