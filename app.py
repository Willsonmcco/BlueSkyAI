import json
import os
import re
from flask import Flask, render_template, request, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# ✅ SAFE: API key pulled from environment (NOT hardcoded)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DATA_FILE = "progress.json"
LEADERBOARD_FILE = "leaderboard.json"

CATEGORY_RULES = {
    "general": {
        "name": "General",
        "allowed_topics": [
            "basic math",
            "basic physics",
            "basic electricity",
            "aircraft drawings",
            "weight and balance",
            "fluid lines and fittings",
            "materials and processes",
            "inspection concepts",
            "ground operations and servicing",
            "cleaning and corrosion control",
            "hand tools",
            "measuring tools",
            "maintenance forms and records",
            "FAA regulations",
            "aviation safety"
        ]
    },
    "airframe": {
        "name": "Airframe",
        "allowed_topics": [
            "aircraft structures",
            "sheet metal repair",
            "wood structures",
            "fabric covering",
            "composite materials",
            "welding basics",
            "assembly and rigging",
            "hydraulic systems",
            "pneumatic systems",
            "landing gear systems",
            "flight control systems",
            "airframe fuel systems",
            "aircraft electrical systems",
            "aircraft instrument systems",
            "cabin atmosphere systems",
            "ice and rain control systems",
            "fire protection systems",
            "airframe inspection and troubleshooting"
        ]
    },
    "powerplant": {
        "name": "Powerplant",
        "allowed_topics": [
            "reciprocating engines",
            "turbine engines",
            "engine theory",
            "ignition systems",
            "spark plugs",
            "magnetos",
            "fuel metering systems",
            "induction systems",
            "superchargers and turbochargers",
            "engine electrical systems",
            "lubrication systems",
            "engine cooling systems",
            "exhaust systems",
            "engine inspection",
            "engine troubleshooting",
            "propellers and propeller systems"
        ]
    }
}

def load_progress():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

BASE_PROMPT = (
    "You are an expert FAA A&P tutor helping students understand concepts. "
    "Stay strictly within FAA A&P subject matter."
)

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    question = request.form.get("question", "")

    if request.method == "POST" and question:
        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": BASE_PROMPT},
                    {"role": "user", "content": question},
                ],
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error: {str(e)}"

    return render_template("index.html", answer=answer, question=question)

if __name__ == "__main__":
    app.run(debug=True)
