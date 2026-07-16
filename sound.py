import os
import pygame

pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

correct = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "correct.wav"))
wrong = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "wrong.wav"))
win = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "win.wav"))