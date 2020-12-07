import pygame
import random

pygame.init()
pygame.font.init()

WIDTH = 900
HEIGHT = 600
TITLE = "Ping Pong"
ICON = pygame.image.load("icon.png")
gameFont = pygame.font.SysFont("Comic Sans MS", 30)

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


class Game:
    def __init__(self, player1, player2, ball):
        self.running = True
        self.clock = pygame.time.Clock()
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        self.screen = "start"

    def start(self):
        while self.running:
            print(self.player1.score, self.player2.score)
            self.clock.tick(500)
            screen.fill(BLACK)
            self.end()
            self.ball.show()
            self.ball.move()
            self.ball.checkforEdges()

            self.player1.paddle.show()
            self.player2.paddle.show()

            self.player1.movePaddle()
            self.player2.movePaddle()

            self.player1.paddle.checkforBall(self.ball)
            self.player2.paddle.checkforBall(self.ball)

            self.player1.paddle.checkforEdges()
            self.player2.paddle.checkforEdges()

            self.checkforPoint()
            self.showScores()

            pygame.display.update()

    def end(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def checkforPoint(self):
        if self.ball.x - self.ball.size < 0:
            self.player2.score += 1
            self.ball.reset()
        elif self.ball.x + self.ball.size > WIDTH:
            self.player1.score += 1
            self.ball.reset()

    def showScores(self):
        self.player1.showScore()
        self.player2.showScore()


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
        self.x_speed *= -1
        self.y_speed *= -1
        self.x = random.randint(WIDTH//2-70, WIDTH//2+70)
        self.y = random.randint(HEIGHT//2 - 70, HEIGHT//2 + 70)

    def leaveScreen(self):
        if self.x > WIDTH or self.x < 0:
            self.reset()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.createPaddle()
        self.setKeys()
        self.setScorepos()

    def setScorepos(self):
        self.scorepos = (30, 0) if self.name == 1 else (WIDTH-50, 0)

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

    def showScore(self):
        score = gameFont.render(str(self.score), True, WHITE, BLACK)
        screen.blit(score, self.scorepos)


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

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    player1 = Player(1)
    player2 = Player(2)
    ball = Ball(GREEN)

    game = Game(player1, player2, ball)
    game.start()


main()
