import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "leaderboard.json")


def load():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def save_all(board):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(board, f, indent=4)


def save(name, score):
    if not name:
        return

    board = load()

    board.append({
        "name": name,
        "score": score
    })

    board.sort(key=lambda x: x["score"], reverse=True)
    board = board[:10]

    save_all(board)
