import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 600
TITLE = "Ping Pong"
ICON = pygame.image.load("icon.png")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


def setTitle(TITLE):
    pygame.display.set_caption(TITLE)


def setIcon(ICON):
    pygame.display.set_icon(ICON)


class Ball:
    def __init__(self):
        pass


class Player:
    def ___init__(self):
        pass


class Paddle:
    def __init__(self):
        pass


def main():

    setTitle(TITLE)
    setIcon(ICON)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)


main()
