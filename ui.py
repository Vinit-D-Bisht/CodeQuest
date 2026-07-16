import tkinter as tk
from tkinter import ttk, messagebox
import game,save,achievements,leaderboard,stats,shop,sound,rank,splash,settings,random
from datetime import date
from constants import *

root = tk.Tk()
root.title("CodeQuest")
root.attributes("-fullscreen", True)
root.configure(bg=BG)

# Press ESC to exit fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
lifeline_used = False
question_locked = False
selected_language = ""
level = 1
score = 0
current_question = 0
questions = []
player = {}

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

def create_card(parent):
    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=CARD2,
        highlightthickness=2,
        bd=0
    )
    return card

def menu_button(parent, text, color, command):

    b = tk.Button(
        parent,
        text=text,
        font=("Segoe UI",16,"bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        bd=0,
        width=18,
        height=2,
        cursor="hand2",
        command=command
    )

    b.bind("<Enter>",lambda e:b.config(font=("Segoe UI",17,"bold")))
    b.bind("<Leave>",lambda e:b.config(font=("Segoe UI",16,"bold")))

    return b

def name_screen():
    clear()

    # If a player name is already saved, skip the name screen.
    global player_name
    try:
        saved_player = save.load_data().get("player", "")
    except Exception:
        saved_player = ""
    if saved_player:
        player_name = saved_player
        return language_screen()

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

        if not player_name:
            messagebox.showwarning("Warning", "Please enter your name.")
            return

        player = save.load_data()
        player["player"] = player_name
        save.save_data(player)

        language_screen()

    continue_btn = tk.Button(
        root,
        text="Continue ➜",
        command=save_name
    )
    continue_btn.pack(pady=20)


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

    # Always create timer_label so game.countdown() never crashes.
    timer_label = tk.Label(
        root,
        text="⏳ 30s" if settings.load()["timer"] else "⏳ OFF",
        font=("Arial", 16, "bold"),
        fg=YELLOW,
        bg=BG
    )
    if settings.load()["timer"]:
        timer_label.pack()

    tk.Label(
        root,
        text=f"Category : {selected_language}",
        font=("Arial",12),
        bg=BG,
        fg="cyan"
        ).pack()
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
        command=game.submit_answer
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
        # Ensure timer is initialized before countdown starts
        game.countdown()

    
    tk.Button(
        root,
        text="50-50",
        font=("Arial",12,"bold"),
        bg="purple",
        fg="white",
        command=game.fifty_fifty
    ).pack()
    tk.Button(
        root,
        text="Skip",
        font=("Arial",12,"bold"),
        bg="orange",
        fg="white",
        command=game.skip_question
    ).pack()

def show_result():
    clear()

    percentage = score * 20
    wrong = 5 - score

    player = save.load_data()
    player_rank = rank.get_rank(player["xp"])

    if settings.load()["sound"]:
        sound.win.play()

    if score == 5:
        player["xp"] += 50
        save.save_data(player)

    if player_name:
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
    stars="⭐"*score

    tk.Label(
        root,
        text=stars,
        font=("Arial",30),
        bg=BG,
        fg="gold"
    ).pack()

    tk.Label(
        root,
        text=f"⭐ Score: {score}/5",
        font=("Arial", 24, "bold"),
        fg=YELLOW,
        bg=BG
    ).pack(pady=15)
    coins = score * 5

    tk.Label(
        root,
        text=f"🪙 +{coins} Coins Earned",
        font=("Arial",18,"bold"),
        bg=BG,
        fg="gold"
    ).pack()

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
    if score==5:
        tk.Label(
            root,
            text="🔥 PERFECT SCORE BONUS +50 XP",
            font=("Arial",18,"bold"),
            fg="orange",
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

        for badge in badges[:3]:
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
    text=random.choice([
        f"Welcome {player_name} 👋",
        f"Good Luck {player_name} 🔥",
        f"Ready To Code {player_name}? 🚀",
        f"Let's Win {player_name}! ⚔"
        ]),
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
    global player_name
    player = save.load_data()
    player_name = player.get("player", "")
    today = str(date.today())

    if player.get("last_reward") != today:
        player["last_reward"] = today
        player["coins"] += 20
        save.save_data(player)

    game_stats = stats.load()
    accuracy = stats.accuracy()
    player_rank = rank.get_rank(player["xp"])

    root.configure(bg=DARK)

    # ---------------- TITLE ----------------

    tk.Label(
        root,
        text="⚔ CODEQUEST ⚔",
        font=("Segoe UI",36,"bold"),
        fg=GREEN,
        bg=DARK
    ).pack(pady=15)

    tk.Label(
        root,
        text="Master The Code • Conquer The Quest",
        font=("Segoe UI",15),
        fg="white",
        bg=DARK
    ).pack()

    # ================= MAIN =================

    body = tk.Frame(root,bg=DARK)
    body.pack(pady=25)

    # ========= LEFT =========

    left = tk.Frame(body,bg=DARK)
    left.grid(row=0,column=0,padx=30)

    card = create_card(left)
    card.pack()

    tk.Label(
        card,
        text=f"{player.get('avatar', '😎')}  {player.get('player', 'Player')}",
        font=("Segoe UI",22,"bold"),
        bg=CARD,
        fg="white"
    ).pack(pady=(15,5))

    tk.Label(
        card,
        text=player_rank,
        font=("Segoe UI",15,"bold"),
        fg=GREEN,
        bg=CARD
    ).pack()

    tk.Label(
        card,
        text=f"⭐ XP {player['xp']}      🪙 {player['coins']}",
        font=("Segoe UI",15),
        bg=CARD,
        fg="gold"
    ).pack(pady=5)

    ttk.Progressbar(
        card,
        length=300,
        maximum=1000,
        value=player["xp"]
    ).pack(pady=10)

    tk.Label(
        card,
        text=f"🎮 {game_stats['games_played']} Games",
        font=("Segoe UI",13),
        bg=CARD,
        fg="white"
    ).pack()

    tk.Label(
        card,
        text=f"🎯 {accuracy}% Accuracy",
        font=("Segoe UI",13),
        bg=CARD,
        fg="white"
    ).pack(pady=(0,15))

    # ========= MENU =========

    menu = tk.Frame(left,bg=DARK)
    menu.pack(pady=25)

    menu_button(menu,"▶ START QUEST",GREEN,name_screen).grid(row=0,column=0,padx=10,pady=10)

    menu_button(menu,"📊 Statistics",BLUE,stats_screen).grid(row=0,column=1,padx=10,pady=10)

    menu_button(menu,"🏆 Leaderboard",ORANGE,leaderboard_screen).grid(row=1,column=0,padx=10,pady=10)

    menu_button(menu,"🛒 Shop","#8B5CF6",shop_screen).grid(row=1,column=1,padx=10,pady=10)

    menu_button(menu,"⚙ Settings","#555555",settings_screen).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=10
    )

    # Exit button: keep it inside left column below the menu.
    # This avoids mixed pack/grid layout + fullscreen clipping issues.
    exit_btn = tk.Button(
        left,
        text="❌ Exit",
        bg="red",
        fg="white",
        font=("Segoe UI",13,"bold"),
        width=18,
        command=root.destroy
    )
    exit_btn.pack(pady=10)


    # ========= RIGHT =========


    right = create_card(body)
    right.grid(row=0,column=1,padx=25,sticky="n")

    tk.Label(
        right,
        text="🏆 TOP PLAYERS",
        font=("Segoe UI",18,"bold"),
        fg=GREEN,
        bg=CARD
    ).pack(pady=10)

    board = leaderboard.load()[:5]

    medals=["🥇","🥈","🥉","4️⃣","5️⃣"]

    if board:

        for i,p in enumerate(board):

            tk.Label(
                right,
                text=f"{medals[i]}  {p['name']}",
                font=("Segoe UI",13,"bold"),
                bg=CARD,
                fg="white"
            ).pack(anchor="w",padx=20)

            tk.Label(
                right,
                text=f"Score : {p['score']}/5",
                font=("Segoe UI",11),
                bg=CARD,
                fg="gold"
            ).pack(anchor="w",padx=45,pady=(0,8))

    else:

        tk.Label(
            right,
            text="No scores yet",
            font=("Segoe UI",13),
            bg=CARD,
            fg="white"
        ).pack(pady=20)

    tips = [
        "💡 Practice daily",
        "💡 Debug patiently",
        "💡 Build projects",
        "💡 Read errors carefully"
    ]

    tk.Label(
        root,
        text=random.choice(tips),
        font=("Segoe UI",12),
        fg="cyan",
        bg=DARK
    ).pack(pady=10)

    tk.Label(
        root,
        text="CodeQuest v1.0",
        font=("Segoe UI",10),
        fg="gray",
        bg=DARK
    ).pack(side="bottom",pady=8)


def game_complete():
    clear()

    player = save.load_data()
    if "avatar" not in player:
        player["avatar"] = "😎"
        save.save_data(player)
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
    ttk.Progressbar(
        root,
        length=350,
        maximum=1000,
        value=player["xp"]
    ).pack(pady=10)

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

    tk.Label(
        root,
        text="🏅 Certified CodeQuest Explorer",
        font=("Arial",22,"bold"),
        fg="gold",
        bg=BG
    ).pack(pady=20)

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

    if "Golden Badge" in item["name"]:
        player["avatar"] = "👑"
    elif "XP Booster" in item["name"]:
        player["xp"] += 50

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
    ).pack(pady=10)

    tk.Checkbutton(
        root,
        text="Enable Sound",
        variable=sound_var,
        font=("Arial", 15),
        bg=BG,
        fg=WHITE,
        selectcolor=BG
    ).pack(pady=5)

    tk.Checkbutton(
        root,
        text="Enable Timer",
        variable=timer_var,
        font=("Arial", 15),
        bg=BG,
        fg=WHITE,
        selectcolor=BG
    ).pack(pady=5)

    def save_settings():
        settings.save({
            "sound": sound_var.get(),
            "timer": timer_var.get()
        })
        messagebox.showinfo("Settings", "Settings saved!")
    def reset_game():
        if messagebox.askyesno("Reset", "Delete all progress?"):
            save.save_data(save.DEFAULT.copy())
            stats.save(stats.DEFAULT.copy())
            leaderboard.save_all([])
            settings.save(settings.DEFAULT.copy())
            global player_name
            player_name = ""
            home()
    tk.Button(
        root,
        text="Reset Progress",
        bg="red",
        fg="white",
        command=reset_game
    ).pack(pady=10)
   
    tk.Button(
        root,
        text="Save",
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 14, "bold"),
        command=save_settings
    ).pack(pady=10)

    tk.Button(
        root,
        text="⬅ Back to Home",
        font=("Arial",14,"bold"),
        bg=BLUE,
        fg=WHITE,
        width=20,
        height=2,
        command=home
    ).pack(pady=10)

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