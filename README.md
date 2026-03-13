# 🖥️ Termux Projects by flandreiii

> A collection of terminal tools for Android — built with Python, running entirely in Termux.

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/flandreiii)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Termux](https://img.shields.io/badge/Termux-Android-black?style=for-the-badge&logo=android&logoColor=white)](https://termux.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📦 Projects

| Project | Description | Stack |
|---------|-------------|-------|
| [TermuxDash](#-termuxdash) | Local web dashboard for system stats, weather & todos | Python, Flask, HTML/CSS/JS |
| [TermuxNotify](#-termuxnotify) | Smart background notification daemon | Python, schedule, termux-api |

---

---

# 🖥️ TermuxDash

> A dark, terminal-aesthetic local web dashboard — open it in your phone's browser at `localhost:5000`.

## 📸 Preview

```
┌──────────────────────────────────────┐
│  TERMUXDASH              21:34:55    │
├──────────────────────────────────────┤
│  // battery      │  // uptime        │
│  ██████░░  72%   │  4h 21m           │
│  CHARGING 38°C   │  RAM: 1.2/3.8GB   │
├──────────────────────────────────────┤
│  // storage                          │
│  ████████░░░  61%   free: 12GB       │
├──────────────────────────────────────┤
│  // weather                          │
│  24°C  Partly Cloudy  💧 60%         │
├──────────────────────────────────────┤
│  // todos & reminders                │
│  ☑ Buy groceries                     │
│  ☐ Push code to GitHub               │
└──────────────────────────────────────┘
```

## ✨ Features

- 🔋 **Battery** — level, charge status & temperature (via `termux-api`)
- 💾 **RAM** — live memory usage with color-coded progress bar
- 📁 **Storage** — disk usage at a glance
- ⏱️ **Uptime** — how long your device has been running
- 🌤️ **Weather** — live conditions, forecast & hourly temps (no API key needed)
- ✅ **Todos** — add, complete and delete tasks, saved locally
- 🕐 **Live clock** — updates every second in the header

## ⚡ Installation

```bash
# 1. Install dependencies
pkg update && pkg upgrade
pkg install python
pip install flask requests

# 2. (Optional) Real battery stats
pkg install termux-api
# → also install Termux:API app from F-Droid

# 3. Clone & run
git clone https://github.com/flandreiii/Useful-termux-tools.git
cd Useful-termux-tools
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## 🗂️ Project Structure

```
termuxdash/
├── app.py              # Flask backend
├── requirements.txt
├── todos.json          # auto-created
└── templates/
    └── index.html      # dashboard UI
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Backend logic |
| Flask | Web server |
| requests | Weather API calls |
| termux-api | Battery data |
| wttr.in | Free weather (no key needed) |
| HTML/CSS/JS | Frontend UI |

---

---

# 🔔 TermuxNotify

> A smart background notification daemon — sends you Android notifications on a schedule and based on triggers.

## 📸 Preview

```
╔══════════════════════════════════╗
║       TermuxNotify  v1.0         ║
║   Smart Notification Daemon      ║
╚══════════════════════════════════╝

📅 Setting up schedules...
  ✓ Water reminder: every 2h
  ✓ Battery warning: threshold 20%
  ✓ Weather alert: daily at 07:00
  ✓ Daily briefing: daily at 08:00
  ✓ Custom reminder: 22:30 → 😴 Time to wind down!

✅ TermuxNotify is running!
```

## ✨ Features

- 💧 **Water reminders** — get notified every X hours to drink water
- 🔋 **Battery warnings** — alert when battery drops below a threshold
- 🌤️ **Weather alerts** — daily weather notification at a set time
- 📋 **Daily briefing** — morning summary with weather + motivational message
- ⏰ **Custom reminders** — set any reminder at any time of day
- ⚙️ **JSON config** — enable/disable and customize everything in `config.json`

## ⚡ Installation

```bash
# 1. Install dependencies
pkg update && pkg upgrade
pkg install python termux-api
pip install schedule requests
# → also install Termux:API app from F-Droid

# 2. Clone & run
git clone https://github.com/flandreiii/Useful-termux-tools.git
cd termuxnotify
python notify_bot.py
```

## ⚙️ Configuration

Edit `config.json` to customize everything:

```json
{
  "water_reminder": {
    "enabled": true,
    "interval_hours": 2,
    "message": "💧 Time to drink water!"
  },
  "battery_warning": {
    "enabled": true,
    "threshold": 20
  },
  "weather_alert": {
    "enabled": true,
    "check_time": "07:00"
  },
  "custom_reminders": [
    {"enabled": true, "time": "22:30", "message": "😴 Time to sleep!"}
  ]
}
```

## 🚀 Run in Background

```bash
# Start in background
python notify_bot.py &

# Stop it
pkill -f notify_bot.py
```

## 🗂️ Project Structure

```
termuxnotify/
├── notify_bot.py       # main daemon
├── config.json         # all your settings
└── requirements.txt
```

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core logic |
| schedule | Task scheduling |
| requests | Weather API calls |
| termux-api | Android notifications |
| wttr.in | Free weather data |

---

---

## ☕ Support

If you find these projects useful, consider buying me a coffee — it keeps the projects going!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/flandreiii)

---

## 📄 License

MIT License — free to use, modify and distribute.

---

#termux #python #flask #android #linux #terminal #dashboard #notifications #selfhosted #archlinux #opensource #cli #pythonproject #termuxtools #webdashboard #mobiledev #scheduler #automation
