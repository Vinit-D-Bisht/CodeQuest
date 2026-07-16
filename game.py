import random,sound
from tkinter import messagebox
import ui,stats,settings
from constants import *
from question_loader import QUESTION_BANK
import save

def start_game(language, current_level=1):

    if current_level == 1:
        stats.add_game()

    ui.selected_language = language
    ui.current_question = 0
    ui.score = 0
    ui.level = current_level
    ui.player = save.load_data()

    ui.questions = random.sample(
        QUESTION_BANK[language][ui.level],
        5
    )

    ui.show_question()
    
def next_question(time_up=False):

    if ui.timer_job:
        ui.root.after_cancel(ui.timer_job)
        ui.timer_job = None

    if not time_up:
        if ui.selected_option.get() == "":
            messagebox.showwarning("Warning", "Please select an option.")
            return

    correct = ui.questions[ui.current_question]["answer"]

    if ui.selected_option.get() == correct:
        ui.score += 1

        ui.player["xp"] += 10
        ui.player["coins"] += 5

        save.save_data(ui.player)

        stats.add_question(True)

        ui.feedback_label.config(
            text="✔ Correct!  +10 XP  +5 Coins",
            fg=GREEN
        )

        if settings.load()["sound"]:
            sound.correct.play()

    else:

        stats.add_question(False)

        ui.feedback_label.config(
            text="✖ Wrong!",
            fg=RED
        )

        if settings.load()["sound"]:
            sound.wrong.play()

    def load_next():
        ui.current_question += 1

        if ui.current_question < len(ui.questions):
            ui.show_question()
        else:
            ui.show_result()

    ui.root.after(300, load_next)

def next_level():

    if ui.score < 3:
        messagebox.showinfo(
            "Level Failed",
            "You need at least 3/5 to unlock the next level."
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

    data = settings.load()

    if not data["timer"]:
        ui.timer_label.config(text="⏳ Timer Off")
        return

    ui.timer_label.config(text=f"⏳ {ui.timer}s")

    if ui.timer > 0:
        ui.timer -= 1
        ui.timer_job = ui.root.after(1000, countdown)
    else:
        next_question(time_up=True)