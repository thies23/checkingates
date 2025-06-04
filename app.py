from flask import Flask, render_template
import requests
import configparser
from dateutil import parser
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")
API_URL = config["API"]["url"]
AUTH_TOKEN = config["API"]["token"]

def load_gates():
    gates = {}
    with open("gates.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ";" not in line:
                continue
            try:
                gate_id, name = line.split(";", 1)
                gates[int(gate_id)] = name
            except ValueError:
                print(f"Ungültige Zeile in gates.txt: {line}")
    return gates

def fetch_checkins():
    headers = {"Authorization": f"Token {AUTH_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        print("API-Fehler:", response.status_code, response.text)
        return {}

    data = response.json()
    gates = load_gates()
    result = defaultdict(list)

    for gate_name in gates.values():
        result[gate_name] = []

    for pos in data.get("results", []):
        name = pos.get("attendee_name", "Unbekannt")
        checkins = pos.get("checkins", [])
        if checkins:
            latest = max(checkins, key=lambda c: c["datetime"])
            gate_id = latest.get("gate")
            location = gates.get(gate_id, f"Unbekannt ({gate_id})")
            time_obj = parser.isoparse(latest["datetime"])
            is_old = datetime.now(time_obj.tzinfo) - time_obj > timedelta(hours=12)

            result[location].append({
                "name": name,
                "time": time_obj.strftime("%d.%m.%Y %H:%M:%S"),
                "is_old": is_old
            })

    return dict(sorted(result.items())) 

@app.route("/")
def index():
    grouped_checkins = fetch_checkins()
    return render_template("index.html", checkins=grouped_checkins)

if __name__ == "__main__":
    app.run(debug=True)
