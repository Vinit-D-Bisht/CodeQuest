import os


class _SilentSound:
    def play(self):
        pass


correct = _SilentSound()
wrong = _SilentSound()
win = _SilentSound()

try:
    import pygame

    pygame.mixer.init()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sounds_dir = os.path.join(BASE_DIR, "assets", "sounds")

    if os.path.isdir(sounds_dir):
        correct_path = os.path.join(sounds_dir, "correct.wav")
        wrong_path = os.path.join(sounds_dir, "wrong.wav")
        win_path = os.path.join(sounds_dir, "win.wav")

        if os.path.isfile(correct_path):
            correct = pygame.mixer.Sound(correct_path)
        if os.path.isfile(wrong_path):
            wrong = pygame.mixer.Sound(wrong_path)
        if os.path.isfile(win_path):
            win = pygame.mixer.Sound(win_path)
except Exception:
    pass
