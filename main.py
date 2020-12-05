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

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def setTitle(TITLE):
    pygame.display.set_caption(TITLE)


def setIcon(ICON):
    pygame.display.set_icon(ICON)


class Ball:
    def __init__(self):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.x_speed = 1
        self.y_speed = 1
        self.size = 8

    def start(self):
        self.x_speed = 1
        self.y_speed = 1

    def show(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def hitEdges(self):
        if self.y > HEIGHT or self.y < 0:
            self.y_speed *= -1

    def hitPaddle(self, paddle):
        leftright = self.x > paddle.x or self.x < paddle.x - paddle.width
        topbottom = self.y > paddle.y and self.y < paddle.y + paddle.length
        if topbottom and leftright:
            self.x_speed *= -1

    def reset(self):
        self.x_speed = 0
        self.y_speed = 0
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.start()

    def leaveScreen(self):
        if self.x > WIDTH or self.x < 0:
            self.reset()


class Player:
    def ___init__(self):
        pass


class Paddle:
    def __init__(self, x):
        self.width = 10
        self.length = 80
        self.x = x
        self.y = int(HEIGHT/2 - self.length/2)
        self.speed = 2
        self.rect = (self.x, self.y, self.width, self.length)

    def show(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def moveUp(self):
        self.y -= self.speed
        self.rect = (self.x, self.y, self.width, self.length)

    def moveDown(self):
        self.y += self.speed
        self.rect = (self.x, self.y, self.width, self.length)

    def hitEdges(self):
        if self.y + self.length > HEIGHT:
            self.y = HEIGHT-self.length
        elif self.y < 0:
            self.y = 0
        self.rect = (self.x, self.y, self.width, self.length)


def main():

    setTitle(TITLE)
    setIcon(ICON)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        pygame.display.update()


main()
