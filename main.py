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
    def __init__(self, name):
        self.name = name
        self.score = 0

    def createPaddle(self):
        self.paddle = Paddle(10) if self.name == 1 else Paddle(WIDTH-2*10)

    def setKeys(self):
        if self.name == 1:
            self.upKey = pygame.K_w
            self.downKey = pygame.K_s
        else:
            self.upKey = pygame.K_UP
            self.downKey = pygame.K_DOWN

    def movePaddle(self):
        keys = pygame.key.get_pressed()
        if keys[self.upKey]:
            self.paddle.moveUp()
        if keys[self.downKey]:
            self.paddle.moveDown()


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

    def hitBall(self, ball):
        leftright = self.x < ball.x < self.x+self.width
        topbottom = self.y < ball.y < self.y+self.length
        if leftright and topbottom:
            ball.x_speed *= -1


def main():

    setTitle(TITLE)
    setIcon(ICON)

    clock = pygame.time.Clock()
    player1 = Player(1)
    player1.createPaddle()
    player2 = Player(2)
    player2.createPaddle()
    player1.setKeys()
    player2.setKeys()

    ball = Ball()
    running = True
    while running:
        clock.tick(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        ball.show()
        ball.move()
        ball.hitEdges()
        player1.paddle.show()
        player1.paddle.hitEdges()
        player1.movePaddle()
        player1.paddle.hitBall(ball)
        player2.paddle.show()
        player2.movePaddle()
        player2.paddle.hitEdges()
        player2.paddle.hitBall(ball)
        # ball.leaveScreen()
        keys = pygame.key.get_pressed()

        pygame.display.update()


main()
