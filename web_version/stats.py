import json
import os

FILE = os.path.join(os.path.dirname(__file__), "data", "player.json")

DEFAULT = {
    "name": "Player",
    "xp": 0,
    "rank": "Beginner"
}


def load_stats():
    if not os.path.exists(FILE):
        _save(DEFAULT.copy())
        return DEFAULT.copy()

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        _save(DEFAULT.copy())
        return DEFAULT.copy()

    merged = DEFAULT.copy()
    merged.update(data)
    return merged


def _save(data):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_xp(amount):
    data = load_stats()
    data["xp"] += amount

    if data["xp"] >= 500:
        data["rank"] = "Master"
    elif data["xp"] >= 250:
        data["rank"] = "Advanced"
    elif data["xp"] >= 100:
        data["rank"] = "Coder"
    else:
        data["rank"] = "Beginner"

    _save(data)
    return data
