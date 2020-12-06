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
    def __init__(self, color):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.x_speed = 1
        self.y_speed = 1
        self.size = 10
        self.color = color

    def start(self):
        self.x_speed = 1
        self.y_speed = 1

    def show(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def checkforEdges(self):
        if self.y > HEIGHT or self.y < 0:
            self.y_speed *= -1

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
        self.createPaddle()
        self.setKeys()

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
        self.length = 100
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

    def checkforEdges(self):
        if self.y + self.length > HEIGHT:
            self.y = HEIGHT-self.length
        elif self.y < 0:
            self.y = 0
        self.rect = (self.x, self.y, self.width, self.length)

    def checkforBall(self, ball):
        leftright = self.x < ball.x < self.x+self.width
        topbottom = self.y < ball.y < self.y+self.length
        if leftright and topbottom:
            ball.x_speed *= -1


def main():
    setTitle(TITLE)
    setIcon(ICON)

    clock = pygame.time.Clock()
    player1 = Player(1)
    player2 = Player(2)

    ball = Ball(GREEN)
    running = True
    while running:
        clock.tick(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        ball.show()
        ball.move()
        ball.checkforEdges()
        player1.paddle.show()
        player1.paddle.checkforEdges()
        player1.movePaddle()
        player1.paddle.checkforBall(ball)

        player2.paddle.show()
        player2.paddle.checkforEdges()
        player2.movePaddle()
        player2.paddle.checkforBall(ball)

        # ball.leaveScreen()

        pygame.display.update()


main()
