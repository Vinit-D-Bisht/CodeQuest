import random
from tkinter import messagebox

import ui
import save
import stats
import sound
import settings

from constants import *
from question_loader import QUESTION_BANK

skip_used = False


def _cancel_timer():
    if ui.timer_job:
        ui.root.after_cancel(ui.timer_job)
        ui.timer_job = None


def _lock_question():
    ui.question_locked = True


def _unlock_question():
    ui.question_locked = False


def start_game(language, current_level=1):
    global skip_used

    skip_used = False
    ui.lifeline_used = False
    _unlock_question()

    if current_level == 1:
        stats.add_game()

    ui.selected_language = language
    ui.level = current_level
    ui.current_question = 0
    ui.score = 0

    ui.player = save.load_data()

    questions = QUESTION_BANK.get(language, {}).get(current_level, [])
    if len(questions) < 5:
        messagebox.showerror(
            "Error",
            f"Not enough questions for {language} Level {current_level}."
        )
        ui.home()
        return

    ui.questions = random.sample(questions, 5)
    ui.show_question()


def _get_explanation(q):
    return q.get("explanation") or q.get("explanation_text") or q.get("reason") or ""


def submit_answer():
    if ui.question_locked:
        return

    _cancel_timer()
    _lock_question()

    answer = ui.selected_option.get()

    if answer == "":
        _unlock_question()
        messagebox.showwarning("Warning", "Select an option.")
        return

    q = ui.questions[ui.current_question]

    if answer == q["answer"]:
        ui.score += 1

        ui.player["xp"] += 10
        ui.player["coins"] += 5
        save.save_data(ui.player)

        stats.add_question(True)

        explanation = _get_explanation(q)
        ui.feedback_label.config(
            fg="lime",
            text=(f"✅ Correct\n\n💡 {explanation}" if explanation else "✅ Correct")
        )

        if settings.load()["sound"]:
            sound.correct.play()

    else:
        stats.add_question(False)

        explanation = _get_explanation(q)
        ui.feedback_label.config(
            fg="orange",
            text=(
                f"❌ Wrong\n\n✅ {q['answer']}\n\n💡 {explanation}"
                if explanation
                else f"❌ Wrong\n\n✅ {q['answer']}"
            )
        )

        if settings.load()["sound"]:
            sound.wrong.play()

    ui.root.after(1800, load_next)


def load_next():
    _cancel_timer()
    ui.current_question += 1

    if ui.current_question < len(ui.questions):
        _unlock_question()
        ui.show_question()
    else:
        _unlock_question()
        ui.show_result()


def next_question(time_up=False):
    load_next()


def next_level():
    if ui.score < 3:
        messagebox.showinfo(
            "Level Failed",
            "Need at least 3 correct answers."
        )
        start_game(ui.selected_language, ui.level)
        return

    if ui.level == 1:
        start_game(ui.selected_language, 2)
    elif ui.level == 2:
        start_game(ui.selected_language, 3)
    else:
        ui.game_complete()


def countdown():
    if ui.question_locked:
        return

    if not settings.load()["timer"]:
        ui.timer_label.config(text="⏳ OFF")
        return

    ui.timer_label.config(text=f"⏳ {ui.timer}s")

    if ui.timer > 0:
        ui.timer -= 1
        ui.timer_job = ui.root.after(1000, countdown)
    else:
        _lock_question()
        q = ui.questions[ui.current_question]
        stats.add_question(False)

        explanation = _get_explanation(q)
        ui.feedback_label.config(
            fg="red",
            text=(
                f"⏰ Time Up!\n\n✅ {q['answer']}\n\n💡 {explanation}"
                if explanation
                else f"⏰ Time Up!\n\n✅ {q['answer']}"
            )
        )

        ui.root.after(1800, load_next)


def skip_question():
    global skip_used

    if skip_used or ui.question_locked:
        return

    skip_used = True
    _cancel_timer()
    stats.add_question(False)
    load_next()


def fifty_fifty():
    if ui.lifeline_used or ui.question_locked:
        return

    ui.lifeline_used = True

    q = ui.questions[ui.current_question]

    wrong = [o for o in q["options"] if o != q["answer"]]
    if len(wrong) < 2:
        return

    remove = random.sample(wrong, 2)

    for widget in ui.root.winfo_children():
        if widget.winfo_class() == "Radiobutton":
            if widget.cget("text") in remove:
                widget.destroy()
