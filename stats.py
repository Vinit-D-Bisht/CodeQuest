import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "stats.json")

DEFAULT = {
    "games_played": 0,
    "questions_answered": 0,
    "correct_answers": 0
}


def load():
    if not os.path.exists(FILE):
        return DEFAULT.copy()

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT.copy()

    if not isinstance(data, dict):
        return DEFAULT.copy()

    merged = DEFAULT.copy()
    merged.update(data)
    return merged


def save(stats):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)

    with open(FILE, "w") as f:
        json.dump(stats, f, indent=4)


def add_game():
    stats = load()
    stats["games_played"] += 1
    save(stats)


def add_question(correct):
    stats = load()
    stats["questions_answered"] += 1

    if correct:
        stats["correct_answers"] += 1

    save(stats)


def accuracy():
    stats = load()

    if stats["questions_answered"] == 0:
        return 0

    return round(
        stats["correct_answers"] * 100 / stats["questions_answered"],
        2
    )
