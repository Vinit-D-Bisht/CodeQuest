import tkinter as tk
from tkinter import ttk, messagebox
import game,save,achievements,leaderboard,stats,shop,sound,rank,splash,settings
from constants import *

root = tk.Tk()
root.title("CodeQuest")
root.attributes("-fullscreen", True)
root.configure(bg=BG)

# Press ESC to exit fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

selected_language = ""
level = 1
score = 0
current_question = 0
questions = []

selected_option = tk.StringVar()

timer = 30
timer_job = None

player_name = ""

def clear():
    for widget in root.winfo_children():
        widget.destroy()

def hover_effect(button, normal, hover):
    button.bind("<Enter>", lambda e: button.config(bg=hover))
    button.bind("<Leave>", lambda e: button.config(bg=normal))

def name_screen():
    clear()

    tk.Label(
        root,
        text="⚔ Welcome to CodeQuest ⚔",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=GREEN
    ).pack(pady=30)

    tk.Label(
        root,
        text="Enter your name to begin your coding adventure",
        font=("Arial", 15),
        bg=BG,
        fg=WHITE
    ).pack(pady=10)

    name_entry = tk.Entry(
        root,
        font=("Arial", 18),
        width=20,
        justify="center"
    )
    name_entry.pack(pady=20)

    def save_name():
        global player_name

        player_name = name_entry.get().strip()

        if player_name == "":
            messagebox.showwarning(
                "Warning",
                "Please enter your name."
            )
            return

        player = save.load_data()
        player["player"] = player_name
        save.save_data(player)

        language_screen()

    continue_btn = tk.Button(
        root,
        text="Continue ➜",
        font=("Arial", 16, "bold"),
        bg=GREEN,
        fg=WHITE,
        width=15,
        command=save_name
    )

    hover_effect(continue_btn, GREEN, "#2ECC71")
    continue_btn.pack(pady=25)

def show_question():
    clear()

    global feedback_label, timer_label, timer, timer_job

    q = questions[current_question]

    selected_option.set("")

    if timer_job:
        root.after_cancel(timer_job)
        timer_job = None

    timer = 30

    tk.Label(
        root,
        text=f"👋 {player_name}",
        font=("Arial", 14),
        fg=WHITE,
        bg=BG
    ).pack(pady=(10, 0))

    tk.Label(
        root,
        text=f"{selected_language} | Level {level}",
        font=("Arial", 22, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=10)

    if settings.load()["timer"]:
        timer_label = tk.Label(
            root,
            text="⏳ 30s",
            font=("Arial", 16, "bold"),
            fg=YELLOW,
            bg=BG
        )
        timer_label.pack()

    tk.Label(
        root,
        text=f"Question {current_question + 1}/5",
        font=("Arial", 15),
        fg=WHITE,
        bg=BG
    ).pack(pady=5)

    tk.Label(
        root,
        text=q["question"],
        font=("Arial", 18),
        wraplength=700,
        fg=WHITE,
        bg=BG
    ).pack(pady=25)

    for option in q["options"]:
        tk.Radiobutton(
            root,
            text=option,
            variable=selected_option,
            value=option,
            font=("Arial", 15),
            fg=WHITE,
            bg=BG,
            selectcolor="#1E293B",
            activebackground=BG,
            activeforeground=WHITE
        ).pack(anchor="w", padx=250)

    next_btn = tk.Button(
        root,
        text="Next ➜",
        font=("Arial", 15, "bold"),
        bg=GREEN,
        fg=WHITE,
        width=15,
        command=game.next_question
    )

    hover_effect(next_btn, GREEN, "#2ECC71")
    next_btn.pack(pady=25)

    progress = ttk.Progressbar(
        root,
        orient="horizontal",
        length=500,
        mode="determinate",
        maximum=5
    )
    progress["value"] = current_question + 1
    progress.pack(pady=10)

    feedback_label = tk.Label(
        root,
        text="",
        font=("Arial", 22, "bold"),
        bg=BG
    )
    feedback_label.pack(pady=10)

    if settings.load()["timer"]:
        game.countdown()

def show_result():
    clear()

    percentage = score * 20
    wrong = 5 - score

    player = save.load_data()
    player_rank = rank.get_rank(player["xp"])

    if settings.load()["sound"]:
        sound.win.play()

    leaderboard.save(player_name, score)
    badges = achievements.check(player, score, level)

    tk.Label(
        root,
        text=f"🎉 LEVEL {level} COMPLETE",
        font=("Arial", 28, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=25)

    tk.Label(
        root,
        text=f"Great Job, {player_name}!",
        font=("Arial", 18, "bold"),
        fg=WHITE,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text=f"⭐ Score: {score}/5",
        font=("Arial", 24, "bold"),
        fg=YELLOW,
        bg=BG
    ).pack(pady=15)

    tk.Label(
        root,
        text=f"✅ Correct: {score}",
        font=("Arial", 16),
        fg=GREEN,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text=f"❌ Wrong: {wrong}",
        font=("Arial", 16),
        fg=RED,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text=f"🎯 Accuracy: {percentage}%",
        font=("Arial", 16),
        fg=WHITE,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text=f"🏆 Rank: {player_rank}",
        font=("Arial", 16, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=10)

    if badges:
        tk.Label(
            root,
            text="🏅 Achievements Unlocked",
            font=("Arial", 18, "bold"),
            fg=GREEN,
            bg=BG
        ).pack(pady=(15, 5))

        for badge in badges:
            tk.Label(
                root,
                text=badge,
                font=("Arial", 14),
                fg=YELLOW,
                bg=BG
            ).pack()

    if level < 3:
        continue_btn = tk.Button(
            root,
            text="Continue ➜",
            font=("Arial", 16, "bold"),
            width=18,
            bg=BLUE,
            fg=WHITE,
            command=game.next_level
        )
    else:
        continue_btn = tk.Button(
            root,
            text="Finish Quest 🏆",
            font=("Arial", 16, "bold"),
            width=18,
            bg=GREEN,
            fg=WHITE,
            command=game.next_level
        )

    hover_effect(
        continue_btn,
        continue_btn["bg"],
        "#2ECC71"
    )
    continue_btn.pack(pady=20)

    restart_btn = tk.Button(
        root,
        text="Restart Level",
        font=("Arial", 16, "bold"),
        width=18,
        bg=ORANGE,
        fg=WHITE,
        command=lambda: game.start_game(selected_language, level)
    )
    hover_effect(restart_btn, ORANGE, "#F39C12")
    restart_btn.pack(pady=8)

    home_btn = tk.Button(
        root,
        text="Home",
        font=("Arial", 14),
        width=18,
        bg=GRAY,
        fg=WHITE,
        command=home
    )
    hover_effect(home_btn, GRAY, "#7F8C8D")
    home_btn.pack(pady=8)

def language_screen():
    clear()

    tk.Label(
        root,
        text=f"Welcome, {player_name} 👋",
        font=("Arial", 16, "bold"),
        fg=WHITE,
        bg=BG
    ).pack(pady=(20, 5))

    tk.Label(
        root,
        text="Choose Your Programming Language",
        font=("Arial", 26, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=15)

    tk.Label(
        root,
        text="Each language has 3 Levels • 5 Random Questions per Level",
        font=("Arial", 13),
        fg=WHITE,
        bg=BG
    ).pack(pady=(0, 25))

    languages = [
        ("🐍 Python", "Python"),
        ("☕ Java", "Java"),
        ("⚙ C", "C"),
        ("🚀 C++", "C++"),
        ("💎 C#", "C#")
    ]

    for text, value in languages:
        btn = tk.Button(
            root,
            text=text,
            font=("Arial", 16, "bold"),
            width=20,
            height=2,
            bg=BLUE,
            fg=WHITE,
            command=lambda lang=value: game.start_game(lang)
        )

        hover_effect(btn, BLUE, "#4A90E2")
        btn.pack(pady=8)

    back_btn = tk.Button(
        root,
        text="⬅ Back",
        font=("Arial", 13, "bold"),
        width=12,
        bg=GRAY,
        fg=WHITE,
        command=home
    )

    hover_effect(back_btn, GRAY, "#7F8C8D")
    back_btn.pack(pady=20)

def home():
    clear()

    player = save.load_data()
    badges = achievements.check(player)
    player_rank = rank.get_rank(player["xp"])
    game_stats = stats.load()
    accuracy = stats.accuracy()
    board = leaderboard.load()

    tk.Label(
        root,
        text="⚔ CODEQUEST ⚔",
        font=("Arial", 34, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=25)

    tk.Label(
        root,
        text="Master the Code. Conquer the Quest.",
        font=("Arial", 16),
        fg=WHITE,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text=f"👤 {player['player']}",
        font=("Arial", 15, "bold"),
        fg=WHITE,
        bg=BG
    ).pack(pady=(20, 5))

    tk.Label(
        root,
        text=f"🏆 Rank: {player_rank}\n⭐ XP: {player['xp']}    🪙 Coins: {player['coins']}",
        font=("Arial", 14),
        fg=YELLOW,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        root,
        text="🏅 Achievements",
        font=("Arial", 15, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=(15, 5))

    if badges:
        for badge in badges:
            tk.Label(
                root,
                text=badge,
                font=("Arial", 13),
                fg=YELLOW,
                bg=BG
            ).pack()
    else:
        tk.Label(
            root,
            text="No achievements yet.",
            font=("Arial", 13),
            fg=WHITE,
            bg=BG
        ).pack()

    tk.Label(
        root,
        text=f"🎮 Games Played: {game_stats['games_played']}",
        font=("Arial", 13),
        fg=WHITE,
        bg=BG
    ).pack(pady=(15, 2))

    tk.Label(
        root,
        text=f"🎯 Accuracy: {accuracy}%",
        font=("Arial", 13),
        fg=WHITE,
        bg=BG
    ).pack()

    tk.Label(
        root,
        text="🏆 Top Players",
        font=("Arial", 18, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=(20, 10))

    if board:
        for i, entry in enumerate(board[:3], start=1):
            tk.Label(
                root,
                text=f"{i}. {entry['name']} - {entry['score']}/5",
                font=("Arial", 13),
                fg=WHITE,
                bg=BG
            ).pack()
    else:
        tk.Label(
            root,
            text="No scores yet.",
            font=("Arial", 13),
            fg=WHITE,
            bg=BG
        ).pack()

    start_btn = tk.Button(
        root,
        text="START",
        font=("Arial", 18, "bold"),
        width=15,
        height=2,
        bg=GREEN,
        fg=WHITE,
        command=name_screen
    )
    hover_effect(start_btn, GREEN, "#2ECC71")
    start_btn.pack(pady=25)

    stats_btn = tk.Button(
        root,
        text="📊 Statistics",
        font=("Arial", 14, "bold"),
        width=15,
        bg=BLUE,
        fg=WHITE,
        command=stats_screen
    )
    hover_effect(stats_btn, BLUE, "#4A90E2")
    stats_btn.pack(pady=5)

    leader_btn = tk.Button(
        root,
        text="🏆 Leaderboard",
        font=("Arial", 14, "bold"),
        width=15,
        bg=ORANGE,
        fg=WHITE,
        command=leaderboard_screen
    )
    hover_effect(leader_btn, ORANGE, "#F39C12")
    leader_btn.pack(pady=5)

    shop_btn = tk.Button(
        root,
        text="🛒 Shop",
        font=("Arial", 14, "bold"),
        width=15,
        bg=BLUE,
        fg=WHITE,
        command=shop_screen
    )
    hover_effect(shop_btn, BLUE, "#4A90E2")
    shop_btn.pack(pady=5)

    settings_btn = tk.Button(
        root,
        text="⚙ Settings",
        font=("Arial", 14, "bold"),
        width=15,
        bg=GRAY,
        fg=WHITE,
        command=settings_screen
    )
    hover_effect(settings_btn, GRAY, "#7F8C8D")
    settings_btn.pack(pady=5)

def game_complete():
    clear()

    player = save.load_data()
    player_rank = rank.get_rank(player["xp"])

    tk.Label(
        root,
        text="🏆 QUEST COMPLETE 🏆",
        font=("Arial", 30, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=25)

    tk.Label(
        root,
        text=f"Congratulations, {player['player']}!",
        font=("Arial", 20, "bold"),
        fg=WHITE,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"🏆 Final Rank: {player_rank}",
        font=("Arial", 18, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"⭐ Total XP: {player['xp']}",
        font=("Arial", 18),
        fg=YELLOW,
        bg=BG
    ).pack(pady=5)

    tk.Label(
        root,
        text=f"🪙 Total Coins: {player['coins']}",
        font=("Arial", 18),
        fg=YELLOW,
        bg=BG
    ).pack(pady=5)

    home_btn = tk.Button(
        root,
        text="🏠 Home",
        font=("Arial", 16, "bold"),
        bg=BLUE,
        fg=WHITE,
        width=15,
        command=home
    )
    hover_effect(home_btn, BLUE, "#4A90E2")
    home_btn.pack(pady=20)

    play_btn = tk.Button(
        root,
        text="🔄 Play Again",
        font=("Arial", 16, "bold"),
        bg=GREEN,
        fg=WHITE,
        width=15,
        command=lambda: game.start_game(selected_language)
    )
    hover_effect(play_btn, GREEN, "#2ECC71")
    play_btn.pack(pady=10)

    exit_btn = tk.Button(
        root,
        text="Exit",
        font=("Arial", 14, "bold"),
        bg=GRAY,
        fg=WHITE,
        width=15,
        command=root.destroy
    )
    hover_effect(exit_btn, GRAY, "#7F8C8D")
    exit_btn.pack(pady=10)

def shop_screen():
    clear()

    player = save.load_data()

    tk.Label(
        root,
        text="🛒 SHOP",
        font=("Arial", 28, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=20)

    tk.Label(
        root,
        text=f"🪙 Coins: {player['coins']}",
        font=("Arial", 18, "bold"),
        fg=YELLOW,
        bg=BG
    ).pack(pady=10)

    for item in shop.items:
        btn = tk.Button(
            root,
            text=f"{item['name']} - {item['price']} 🪙",
            font=("Arial", 14, "bold"),
            width=28,
            bg=BLUE,
            fg=WHITE,
            command=lambda i=item: buy_item(i)
        )

        hover_effect(btn, BLUE, "#4A90E2")
        btn.pack(pady=6)

    home_btn = tk.Button(
        root,
        text="⬅ Home",
        font=("Arial", 14, "bold"),
        width=15,
        bg=GRAY,
        fg=WHITE,
        command=home
    )

    hover_effect(home_btn, GRAY, "#7F8C8D")
    home_btn.pack(pady=20)

def buy_item(item):
    player = save.load_data()

    if player["coins"] < item["price"]:
        messagebox.showinfo("Shop", "Not enough coins.")
        return

    player["coins"] -= item["price"]
    save.save_data(player)

    messagebox.showinfo(
        "Shop",
        f"You bought {item['name']}!"
    )

    shop_screen()

def settings_screen():
    clear()

    data = settings.load()

    sound_var = tk.BooleanVar(value=data["sound"])
    timer_var = tk.BooleanVar(value=data["timer"])

    tk.Label(
        root,
        text="⚙ SETTINGS",
        font=("Arial", 28, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=30)

    tk.Checkbutton(
        root,
        text="Enable Sound",
        variable=sound_var,
        font=("Arial", 15),
        bg=BG,
        fg=WHITE,
        selectcolor=BG
    ).pack(pady=10)

    tk.Checkbutton(
        root,
        text="Enable Timer",
        variable=timer_var,
        font=("Arial", 15),
        bg=BG,
        fg=WHITE,
        selectcolor=BG
    ).pack(pady=10)

    def save_settings():
        settings.save({
            "sound": sound_var.get(),
            "timer": timer_var.get()
        })
        messagebox.showinfo("Settings", "Settings saved!")

    tk.Button(
        root,
        text="Save",
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 14, "bold"),
        command=save_settings
    ).pack(pady=20)

    tk.Button(
        root,
        text="⬅ Home",
        bg=GRAY,
        fg=WHITE,
        command=home
    ).pack()

def stats_screen():
    clear()

    game_stats = stats.load()
    accuracy = stats.accuracy()

    tk.Label(
        root,
        text="📊 STATISTICS",
        font=("Arial", 28, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=30)

    tk.Label(
        root,
        text=f"🎮 Games Played: {game_stats['games_played']}",
        font=("Arial", 16),
        fg=WHITE,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"❓ Questions Answered: {game_stats['questions_answered']}",
        font=("Arial", 16),
        fg=WHITE,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"✅ Correct Answers: {game_stats['correct_answers']}",
        font=("Arial", 16),
        fg=GREEN,
        bg=BG
    ).pack(pady=10)

    tk.Label(
        root,
        text=f"🎯 Accuracy: {accuracy}%",
        font=("Arial", 16, "bold"),
        fg=YELLOW,
        bg=BG
    ).pack(pady=20)

    home_btn = tk.Button(
        root,
        text="⬅ Home",
        font=("Arial", 14, "bold"),
        bg=GRAY,
        fg=WHITE,
        width=15,
        command=home
    )

    hover_effect(home_btn, GRAY, "#7F8C8D")
    home_btn.pack(pady=30)

def leaderboard_screen():
    clear()

    board = leaderboard.load()

    tk.Label(
        root,
        text="🏆 LEADERBOARD",
        font=("Arial", 28, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=25)

    if not board:
        tk.Label(
            root,
            text="No scores yet.",
            font=("Arial", 18),
            fg=WHITE,
            bg=BG
        ).pack(pady=30)
    else:
        for i, player in enumerate(board, start=1):
            color = YELLOW if i == 1 else WHITE

            tk.Label(
                root,
                text=f"{i}. {player['name']} - {player['score']}/5",
                font=("Arial", 16, "bold" if i <= 3 else "normal"),
                fg=color,
                bg=BG
            ).pack(pady=4)

    home_btn = tk.Button(
        root,
        text="⬅ Home",
        font=("Arial", 14, "bold"),
        bg=GRAY,
        fg=WHITE,
        width=15,
        command=home
    )

    hover_effect(home_btn, GRAY, "#7F8C8D")
    home_btn.pack(pady=30)