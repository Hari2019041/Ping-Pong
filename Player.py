from config import *
from Paddle import Paddle

class Player:
    def __init__(self, no, name):
        self.no = no
        self.name = name
        self.score = 0
        self.createPaddle()
        self.setKeys()
        self.setScorepos()

    def setScorepos(self):
        self.namepos = (30, 0) if self.no == 1 else (WIDTH - 100, 0)
        self.scorepos = (30, 50) if self.no == 1 else (WIDTH - 100, 50)

    def createPaddle(self):
        self.paddle = Paddle(10) if self.no == 1 else Paddle(WIDTH - 2 * 10)

    def setKeys(self):
        self.upKey = pygame.K_w if self.no == 1 else pygame.K_UP
        self.downKey = pygame.K_s if self.no == 1 else pygame.K_DOWN

    def movePaddle(self):
        keys = pygame.key.get_pressed()
        self.paddle.moveUp() if keys[self.upKey] else ''
        self.paddle.moveDown() if keys[self.downKey] else ''

    def usePaddle(self, ball):
        self.movePaddle()
        self.paddle.show()
        self.paddle.checkforBall(ball)
        self.paddle.checkforEdges()

    def showName(self):
        nameLabel = gameFont.render(str(self.name), True, WHITE, BLACK)
        SCREEN.blit(nameLabel, self.namepos)

    def showScore(self):
        scoreLabel = gameFont.render(str(self.score), True, WHITE, BLACK)
        SCREEN.blit(scoreLabel, self.scorepos)

class Computer(Player):
    def __init__(self, no=1, name='Computer'):
        super().__init__(no, name)

    def computerAI(self, ball):
        if ball.x < WIDTH // 2 and ball.x_speed < 0:
            if ball.y < self.paddle.y + self.paddle.length // 2:
                self.paddle.moveUp()
            if ball.y > self.paddle.y + self.paddle.length // 2:
                self.paddle.moveDown()

    def usePaddle(self, ball):
        self.paddle.show()
        self.paddle.checkforEdges()
        self.paddle.checkforBall(ball)
        self.computerAI(ball)
