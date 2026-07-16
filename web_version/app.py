from flask import Flask, render_template, request, session
import random
from stats import add_xp, load_stats
from leaderboard import save_score, get_scores
from questions.python import python_questions
from questions.java import java_questions
from questions.C import c_questions
from questions.Cpp import cpp_questions
from questions.Csharp import csharp_questions


app = Flask(__name__)
app.secret_key = "codequest-secret"


def flatten_questions(question_dict):
    questions = []

    for level in question_dict:
        questions.extend(question_dict[level])

    return questions


QUESTION_BANK = {
    "Python": python_questions,
    "Java": java_questions,
    "C": c_questions,
    "C++": cpp_questions,
    "C#": csharp_questions,
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        languages=QUESTION_BANK.keys()
    )


@app.route("/quiz", methods=["POST"])
def start_quiz():
    language = request.form["language"]
    session["language"] = language
    levels = list(QUESTION_BANK[language].keys())

    return render_template(
        "level.html",
        language=language,
        levels=levels
    )


@app.route("/start", methods=["POST"])
def start_level():
    language = session["language"]
    level = int(request.form["level"])
    bank = QUESTION_BANK[language]
    level_questions = bank[level]

    questions = random.sample(
        level_questions,
        min(5, len(level_questions))
    )

    session["questions"] = questions
    session["level"] = level

    return render_template(
        "quiz.html",
        questions=questions,
        language=language,
        level=level
    )


@app.route("/submit", methods=["POST"])
def submit():
    questions = session.get("questions", [])
    score = 0

    for q in questions:
        if request.form.get(q["question"]) == q["answer"]:
            score += 1

    xp = score * 20
    player = add_xp(xp)

    player_name = player.get("name", "Player")
    save_score(player_name, xp)

    return render_template(
        "result.html",
        score=score,
        total=len(questions),
        xp=xp,
        player=player
    )


@app.route("/leaderboard")
def leaderboard():
    scores = get_scores()

    return render_template(
        "leaderboard.html",
        scores=scores
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
