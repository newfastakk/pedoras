import os
import time
import random
import subprocess
import threading
from datetime import datetime
try:
    import requests
    from pyfiglet import Figlet
    from colorama import init, Fore
except ImportError:
    print("[HEXW0UND] Installing dependencies like a fuckin' boss...")
    subprocess.run(["pip", "install", "requests", "pyfiglet", "colorama"], check=True)
    import requests
    from pyfiglet import Figlet
    from colorama import init, Fore

# Initialize colorama for colored terminal output
init()

# Settings
settings = {
    "auto_stop": False,
    "lag_percent": 50,
    "auto_stop_sec": 30
}

# Global state
running = False
auto_stop_thread = None

def install_tc():
    """Ensure tc (traffic control) is installed for fake lag."""
    try:
        subprocess.run(["tc", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("[HEXW0UND] Installing tc for lag fuckery...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "iproute2"], check=True)

def animated_logo():
    """Display animated 3D HEXW0UND logo."""
    f = Figlet(font="slant")
    logo = f.renderText("HEXW0UND")
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
    
    for _ in range(3):  # Blink 3 times
        for color in colors:
            os.system("clear" if os.name != "nt" else "cls")
            print(color + logo)
            time.sleep(0.2)
    os.system("clear" if os.name != "nt" else "cls")
    print(Fore.RED + logo + Fore.RESET)

def simulate_download():
    """Simulate heavy network load by downloading 'air' (random data)."""
    sites = [
        "http://speedtest.ftp.otenet.gr/files/test100Mb.db",
        "http://ipv4.download.thinkbroadband.com/200MB.zip",
        "http://mirror.internode.on.net/pub/test/1000mb.bin"
    ]
    while running:
        site = random.choice(sites)
        size = random.randint(100 * 1024 * 1024, 1024 * 1024 * 1024)  # 100MB to 1TB
        try:
            print(f"[HEXW0UND] Downloading {size // 1024 // 1024}MB of pure air from {site}...")
            response = requests.get(site, stream=True, timeout=5)
            for _ in response.iter_content(chunk_size=1024 * 1024):
                if not running:
                    break
        except requests.RequestException:
            print("[HEXW0UND] Air packet dropped, grabbing another...")
        time.sleep(random.uniform(0.1, 1))

def apply_fake_lag():
    """Apply fake lag using tc (Linux only)."""
    try:
        lag_ms = settings["lag_percent"] * 10  # Scale lag to 0-1000ms
        subprocess.run(["sudo", "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "delay", f"{lag_ms}ms"], check=True)
        print(f"[HEXW0UND] Fake lag applied: {lag_ms}ms")
    except subprocess.CalledProcessError:
        print("[HEXW0UND] Failed to apply lag. Are you root? Falling back to soft lag...")
        time.sleep(settings["lag_percent"] / 100)  # Simulate soft lag

def remove_fake_lag():
    """Remove fake lag."""
    try:
        subprocess.run(["sudo", "tc", "qdisc", "del", "dev", "eth0", "root"], check=True)
        print("[HEXW0UND] Ping stabilized. Enemies can breathe again.")
    except subprocess.CalledProcessError:
        pass

def fake_vpn():
    """Simulate VPN-like behavior with random headers."""
    headers = {
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/91.0",
        ])
    }
    print(f"[HEXW0UND] Spoofing IP: {headers['X-Forwarded-For']}")
    return headers

def auto_stop_countdown():
    """Handle auto-stop countdown."""
    for i in range(settings["auto_stop_sec"], -1, -1):
        if not running:
            break
        print(f"[HEXW0UND] Auto-stop in {i} seconds", end="\r")
        time.sleep(1)
    if running:
        stop_clamsii()

def start_clamsii():
    """Start Clamsii."""
    global running, auto_stop_thread
    if not running:
        running = True
        print("[HEXW0UND] Clamsii ON")
        apply_fake_lag()
        threading.Thread(target=simulate_download, daemon=True).start()
        if settings["auto_stop"]:
            auto_stop_thread = threading.Thread(target=auto_stop_countdown, daemon=True)
            auto_stop_thread.start()

def stop_clamsii():
    """Stop Clamsii."""
    global running
    if running:
        running = False
        print("[HEXW0UND] Clamsii OFF")
        remove_fake_lag()

def configure_settings():
    """Configure settings via CLI."""
    os.system("clear" if os.name != "nt" else "cls")
    print("[HEXW0UND] SETTINGS MODE")
    print("1. Auto-stop (True/False):", settings["auto_stop"])
    print("2. Lag % (0-100):", settings["lag_percent"])
    print("3. Auto-stop seconds:", settings["auto_stop_sec"])
    print("Type 'хуйня' for lulz or number to change setting. Press Enter to exit.")

    while True:
        choice = input("> ").strip().lower()
        if choice == "":
            break
        elif choice == "хуйня":
            print("[HEXW0UND] Лол, ты серьёзно? Хуйня активирована! 😎")
        elif choice == "1":
            settings["auto_stop"] = not settings["auto_stop"]
            print(f"Auto-stop set to {settings['auto_stop']}")
        elif choice == "2":
            try:
                lag = int(input("Enter lag % (0-100): "))
                settings["lag_percent"] = max(0, min(100, lag))
                print(f"Lag % set to {settings['lag_percent']}")
            except ValueError:
                print("[HEXW0UND] Invalid input, dipshit.")
        elif choice == "3":
            try:
                sec = int(input("Enter auto-stop seconds: "))
                settings["auto_stop_sec"] = max(1, sec)
                print(f"Auto-stop seconds set to {settings['auto_stop_sec']}")
            except ValueError:
                print("[HEXW0UND] Numbers, not bullshit.")
        else:
            print("[HEXW0UND] Pick a valid option, genius.")

def main():
    """Main loop."""
    install_tc()
    animated_logo()
    print("[HEXW0UND] Clamsii ready to fuck shit up. Type 'SET' to configure, Enter to start/stop.")
    
    while True:
        cmd = input().strip().lower()
        if cmd == "set":
            configure_settings()
        elif cmd == "":
            if running:
                stop_clamsii()
            else:
                start_clamsii()
        else:
            print("[HEXW0UND] 'SET' or Enter, you fuckin' noob.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_clamsii()
        print("[HEXW0UND] Peace out, motherfucker!")
