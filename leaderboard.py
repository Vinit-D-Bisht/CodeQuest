import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "leaderboard.json")

def load():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save(name, score):
    board = load()

    board.append({
        "name": name,
        "score": score
    })

    board.sort(key=lambda x: x["score"], reverse=True)

    board = board[:10]

    with open(FILE, "w") as f:
        json.dump(board, f, indent=4)