import schedule
import time
import subprocess
import json
import os
import requests
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# ── Default config ─────────────────────────────────────────────────────────────
DEFAULT_CONFIG = {
    "water_reminder": {
        "enabled": True,
        "interval_hours": 2,
        "message": "💧 Time to drink water!"
    },
    "battery_warning": {
        "enabled": True,
        "threshold": 20,
        "message": "🔋 Battery low! Plug in your charger."
    },
    "weather_alert": {
        "enabled": True,
        "check_time": "07:00",
        "message": "🌤 Good morning! Here's your weather:"
    },
    "daily_briefing": {
        "enabled": True,
        "time": "08:00",
        "message": "📋 Good morning! Start your day strong."
    },
    "custom_reminders": [
        {"enabled": True, "time": "09:00", "message": "🧘 Morning stretch time!"},
        {"enabled": True, "time": "18:00", "message": "🏃 Time for your evening walk!"},
        {"enabled": True, "time": "22:30", "message": "😴 Time to wind down and sleep."}
    ]
}

# ── Config helpers ──────────────────────────────────────────────────────────────
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# ── Termux notification ─────────────────────────────────────────────────────────
def notify(title, message, vibrate=True):
    try:
        cmd = ["termux-notification",
               "--title", title,
               "--content", message,
               "--priority", "high"]
        if vibrate:
            cmd += ["--vibrate", "500"]
        subprocess.run(cmd, timeout=5)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔔 {title}: {message}")
    except FileNotFoundError:
        # fallback if termux-api not installed
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔔 {title}: {message}")
        print("  ⚠ termux-api not found. Install: pkg install termux-api")
    except Exception as e:
        print(f"[!] Notification error: {e}")

# ── Battery check ───────────────────────────────────────────────────────────────
def check_battery():
    cfg = load_config()
    if not cfg["battery_warning"]["enabled"]:
        return
    try:
        result = subprocess.run(
            ["termux-battery-status"], capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout)
        pct = data.get("percentage", 100)
        status = data.get("status", "")
        threshold = cfg["battery_warning"]["threshold"]

        if pct <= threshold and status != "CHARGING":
            notify("⚡ TermuxNotify", f"{cfg['battery_warning']['message']} ({pct}%)")
    except Exception as e:
        print(f"[!] Battery check error: {e}")

# ── Water reminder ──────────────────────────────────────────────────────────────
def water_reminder():
    cfg = load_config()
    if not cfg["water_reminder"]["enabled"]:
        return
    notify("💧 TermuxNotify", cfg["water_reminder"]["message"])

# ── Weather alert ───────────────────────────────────────────────────────────────
def weather_alert():
    cfg = load_config()
    if not cfg["weather_alert"]["enabled"]:
        return
    try:
        r = requests.get("https://wttr.in/?format=3", timeout=6)
        weather = r.text.strip()
        notify("🌤 TermuxNotify", f"{cfg['weather_alert']['message']} {weather}")
    except Exception:
        notify("🌤 TermuxNotify", cfg["weather_alert"]["message"] + " (couldn't fetch weather)")

# ── Daily briefing ──────────────────────────────────────────────────────────────
def daily_briefing():
    cfg = load_config()
    if not cfg["daily_briefing"]["enabled"]:
        return
    try:
        r = requests.get("https://wttr.in/?format=%C+%t", timeout=6)
        weather = r.text.strip()
    except Exception:
        weather = "weather unavailable"

    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    msg = f"{greeting}! Today: {weather}. {cfg['daily_briefing']['message']}"
    notify("📋 TermuxNotify — Daily Briefing", msg)

# ── Custom reminders ─────────────────────────────────────────────────────────────
def fire_custom_reminder(message):
    notify("⏰ TermuxNotify", message)

# ── Scheduler setup ──────────────────────────────────────────────────────────────
def setup_schedules():
    cfg = load_config()

    # Water reminder — every N hours
    if cfg["water_reminder"]["enabled"]:
        interval = cfg["water_reminder"].get("interval_hours", 2)
        schedule.every(interval).hours.do(water_reminder)
        print(f"  ✓ Water reminder: every {interval}h")

    # Battery check — every 15 minutes
    if cfg["battery_warning"]["enabled"]:
        schedule.every(15).minutes.do(check_battery)
        print(f"  ✓ Battery warning: threshold {cfg['battery_warning']['threshold']}%")

    # Weather alert
    if cfg["weather_alert"]["enabled"]:
        t = cfg["weather_alert"]["check_time"]
        schedule.every().day.at(t).do(weather_alert)
        print(f"  ✓ Weather alert: daily at {t}")

    # Daily briefing
    if cfg["daily_briefing"]["enabled"]:
        t = cfg["daily_briefing"]["time"]
        schedule.every().day.at(t).do(daily_briefing)
        print(f"  ✓ Daily briefing: daily at {t}")

    # Custom reminders
    for reminder in cfg.get("custom_reminders", []):
        if reminder.get("enabled"):
            t = reminder["time"]
            msg = reminder["message"]
            schedule.every().day.at(t).do(fire_custom_reminder, message=msg)
            print(f"  ✓ Custom reminder: {t} → {msg}")

# ── Main ─────────────────────────────────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════╗")
    print("║       TermuxNotify  v1.0         ║")
    print("║   Smart Notification Daemon      ║")
    print("╚══════════════════════════════════╝")
    print()
    print("📋 Loading config...")
    cfg = load_config()
    print(f"   Config loaded from: {CONFIG_FILE}")
    print()
    print("📅 Setting up schedules...")
    setup_schedules()
    print()
    print("✅ TermuxNotify is running! Press Ctrl+C to stop.")
    print("─" * 40)

    notify("✅ TermuxNotify", "Notification bot started successfully!")

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] TermuxNotify stopped.")
