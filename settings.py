import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "settings.json")

DEFAULT = {
    "sound": True,
    "timer": True
}


def load():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(FILE):
        save(DEFAULT.copy())
        return DEFAULT.copy()

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        save(DEFAULT.copy())
        return DEFAULT.copy()

    if not isinstance(data, dict):
        data = {}

    merged = DEFAULT.copy()
    merged.update(data)
    return merged


def save(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)
