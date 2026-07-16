import json
import os

FILE = os.path.join(os.path.dirname(__file__), "data", "leaderboard.json")


def _load():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def save_score(name, xp):
    data = _load()

    data.append({
        "name": name,
        "xp": xp
    })

    data.sort(key=lambda x: x["xp"], reverse=True)
    data = data[:10]

    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_scores():
    return _load()
