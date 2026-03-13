from flask import Flask, render_template, jsonify, request
import subprocess
import json
import os
import datetime
import requests

app = Flask(__name__)
TODOS_FILE = os.path.join(os.path.dirname(__file__), "todos.json")
WEATHER_API = "https://wttr.in/?format=j1"  # free, no key needed

# ── Todos helpers ──────────────────────────────────────────────────────────────
def load_todos():
    if not os.path.exists(TODOS_FILE):
        return []
    with open(TODOS_FILE) as f:
        return json.load(f)

def save_todos(todos):
    with open(TODOS_FILE, "w") as f:
        json.dump(todos, f, indent=2)

# ── System stats ───────────────────────────────────────────────────────────────
def get_battery():
    try:
        result = subprocess.run(
            ["termux-battery-status"], capture_output=True, text=True, timeout=5
        )
        return json.loads(result.stdout)
    except Exception:
        # fallback for non-Termux / testing
        return {"percentage": 72, "status": "CHARGING", "temperature": 38.5}

def get_storage():
    try:
        result = subprocess.run(
            ["df", "-h", "/data/data/com.termux"],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            return {"total": parts[1], "used": parts[2], "free": parts[3], "percent": parts[4]}
    except Exception:
        pass
    # general fallback
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split("\n")
        parts = lines[1].split()
        return {"total": parts[1], "used": parts[2], "free": parts[3], "percent": parts[4]}
    except Exception:
        return {"total": "?", "used": "?", "free": "?", "percent": "?%"}

def get_memory():
    try:
        with open("/proc/meminfo") as f:
            mem = {}
            for line in f:
                key, val = line.split(":")
                mem[key.strip()] = int(val.strip().split()[0])
        total = mem.get("MemTotal", 1)
        free  = mem.get("MemAvailable", 0)
        used  = total - free
        pct   = round(used / total * 100)
        def kb_to_mb(kb): return f"{round(kb/1024)}MB"
        return {"total": kb_to_mb(total), "used": kb_to_mb(used), "free": kb_to_mb(free), "percent": pct}
    except Exception:
        return {"total": "?", "used": "?", "free": "?", "percent": 0}

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            secs = float(f.read().split()[0])
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        return f"{h}h {m}m"
    except Exception:
        return "?"

# ── Weather ────────────────────────────────────────────────────────────────────
def get_weather():
    try:
        r = requests.get(WEATHER_API, timeout=6)
        data = r.json()
        current = data["current_condition"][0]
        today   = data["weather"][0]
        desc    = current["weatherDesc"][0]["value"]
        temp_c  = current["temp_C"]
        feels   = current["FeelsLikeC"]
        humidity= current["humidity"]
        max_t   = today["maxtempC"]
        min_t   = today["mintempC"]
        sunrise = today["astronomy"][0]["sunrise"]
        sunset  = today["astronomy"][0]["sunset"]
        hourly  = []
        for h in today["hourly"]:
            hourly.append({
                "time": h["time"].zfill(4)[:2] + ":00",
                "temp": h["tempC"],
                "desc": h["weatherDesc"][0]["value"]
            })
        return {
            "desc": desc, "temp": temp_c, "feels": feels,
            "humidity": humidity, "max": max_t, "min": min_t,
            "sunrise": sunrise, "sunset": sunset,
            "hourly": hourly[:6], "error": None
        }
    except Exception as e:
        return {"error": str(e), "desc": "Unavailable", "temp": "--", "feels": "--",
                "humidity": "--", "max": "--", "min": "--",
                "sunrise": "--", "sunset": "--", "hourly": []}

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def api_stats():
    return jsonify({
        "battery": get_battery(),
        "storage": get_storage(),
        "memory":  get_memory(),
        "uptime":  get_uptime(),
        "time":    datetime.datetime.now().strftime("%H:%M:%S"),
        "date":    datetime.datetime.now().strftime("%A, %B %d %Y"),
    })

@app.route("/api/weather")
def api_weather():
    return jsonify(get_weather())

@app.route("/api/todos", methods=["GET"])
def api_todos_get():
    return jsonify(load_todos())

@app.route("/api/todos", methods=["POST"])
def api_todos_add():
    todos = load_todos()
    text = request.json.get("text", "").strip()
    if text:
        todos.append({"id": int(datetime.datetime.now().timestamp() * 1000),
                      "text": text, "done": False,
                      "created": datetime.datetime.now().strftime("%b %d, %H:%M")})
        save_todos(todos)
    return jsonify(todos)

@app.route("/api/todos/<int:todo_id>/toggle", methods=["POST"])
def api_todos_toggle(todo_id):
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
    save_todos(todos)
    return jsonify(todos)

@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_todos_delete(todo_id):
    todos = [t for t in load_todos() if t["id"] != todo_id]
    save_todos(todos)
    return jsonify(todos)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
