import tkinter as tk
from constants import *

def show(root, callback):
    splash = tk.Frame(root, bg=BG)
    splash.place(relwidth=1, relheight=1)

    tk.Label(
        splash,
        text="⚔ CODEQUEST ⚔",
        font=("Arial", 34, "bold"),
        fg=GREEN,
        bg=BG
    ).pack(pady=120)

    tk.Label(
        splash,
        text="Learn • Play • Level Up",
        font=("Arial", 18),
        fg=WHITE,
        bg=BG
    ).pack()

    loading = tk.Label(
        splash,
        text="Loading...",
        font=("Arial", 16),
        fg=YELLOW,
        bg=BG
    )
    loading.pack(pady=40)

    def animate(count=0):
        dots = "." * (count % 4)
        loading.config(text=f"Loading{dots}")
        if count < 20:
            root.after(150, animate, count + 1)

    animate()

    def finish():
        splash.destroy()
        callback()

    root.after(3000, finish)