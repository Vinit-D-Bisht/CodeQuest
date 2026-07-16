import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "data", "save.json")

DEFAULT = {
    "player": "",
    "xp": 0,
    "coins": 0,
    "avatar": "😎",
    "last_reward": ""
}


def load_data():
    if not os.path.exists(SAVE_FILE):
        save_data(DEFAULT.copy())
        return DEFAULT.copy()

    with open(SAVE_FILE, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            save_data(DEFAULT.copy())
            return DEFAULT.copy()

    if not isinstance(data, dict):
        data = {}

    for k, v in DEFAULT.items():
        data.setdefault(k, v)

    if not data.get("avatar"):
        data["avatar"] = DEFAULT["avatar"]

    return data


def save_data(data):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)
