import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "data", "save.json")

DEFAULT_DATA = {
    "player": "",
    "xp": 0,
    "coins": 0
}

def load_data():
    if not os.path.exists(SAVE_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    with open(SAVE_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)