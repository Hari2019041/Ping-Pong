import pygame
import os
from random import randint, choice

pygame.init()
pygame.font.init()
pygame.mixer.init()

# WINDOW
WIDTH = 900
HEIGHT = 600
TITLE = 'Ping Pong'
ICON = pygame.image.load('icon.png')

# FONTS
mainScreenFont = pygame.font.SysFont('Comic Sans MS', 40)
gameFont = pygame.font.SysFont('Comic Sans MS', 30)

# SOUNDS
BOUNCE = pygame.mixer.Sound(os.path.join('sounds', 'bounce.wav'))

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# SCREEN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
