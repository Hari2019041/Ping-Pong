import pygame
from random import randint, choice
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600
TITLE = 'Ping Pong'
ICON = pygame.image.load('icon.png')

mainScreenFont = pygame.font.SysFont('Comic Sans MS', 40)
gameFont = pygame.font.SysFont('Comic Sans MS', 30)

BOUNCE = pygame.mixer.Sound(os.path.join('sounds', 'bounce.wav'))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def setWindow(TITLE, ICON):
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(ICON)


class Game:
    def __init__(self, player1, player2):
        self.RUNNING = True
        self.clock = pygame.time.Clock()
        self.FPS = 500
        self.player1 = player1
        self.player2 = player2
        self.computer = Computer()
        self.ball = Ball()
        self.game_mode = 'computer'
        self.screen_mode = 'main'

    def paddleMethods(self):
        self.player1.paddle.show()
        self.player2.paddle.show()

        self.player1.movePaddle()
        self.player2.movePaddle()

        self.player1.paddle.checkforBall(self.ball)
        self.player2.paddle.checkforBall(self.ball)

        self.player1.paddle.checkforEdges()
        self.player2.paddle.checkforEdges()

    def computerMode(self):
        SCREEN.fill(BLACK)
        self.end()
        self.ball.show()
        self.ball.move()
        self.ball.checkforEdges()

        self.player2.paddle.show()
        self.player2.movePaddle()
        self.player2.paddle.checkforBall(self.ball)
        self.player2.paddle.checkforEdges()

        self.computer.paddle.show()
        self.computer.paddle.checkforEdges()
        self.computer.paddle.checkforBall(self.ball)
        self.computer.computerAI(self.ball)

        self.player2.showName()
        self.computer.showName()

        self.checkforPoint()
        self.showPlayerScores()
        self.showLine()
        pygame.display.update()

    def twoPlayerMode(self):
        SCREEN.fill(BLACK)
        self.end()
        self.ball.show()
        self.ball.move()
        self.ball.checkforEdges()

        self.paddleMethods()

        self.checkforPoint()
        self.showPlayerNames()
        self.showPlayerScores()
        self.showLine()

        pygame.display.update()

    def start(self):
        while self.RUNNING:
            self.mainPage() if self.screen_mode == 'main' else ''
            self.startGame() if self.screen_mode == 'game' else ''

    def mainPage(self):
        font = pygame.font.SysFont('Comic Sans MS', 40)
        SCREEN.fill(BLACK)
        self.end()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        startGameButton = font.render('START GAME', True, WHITE, BLACK)
        x_pos = WIDTH//2 - startGameButton.get_width()//2
        y_pos = HEIGHT//2 - startGameButton.get_height()//2

        startGamerect = pygame.Rect((x_pos, y_pos, 264, 57))
        SCREEN.blit(startGameButton, (x_pos, y_pos))

        temp = startGamerect.collidepoint((mouse_x, mouse_y))

        self.screen_mode = 'game' if temp else 'main'

        pygame.display.update()

    def startGame(self):
        while self.RUNNING:
            self.clock.tick(self.FPS)
            self.twoPlayerMode() if self.game_mode == 'twoplayer' else ''
            self.computerMode() if self.game_mode == 'computer' else ''

    def end(self):
        for event in pygame.event.get():
            self.RUNNING = False if event.type == pygame.QUIT else True

    def checkforPoint(self):
        player1win = self.ball.x + self.ball.size > WIDTH
        player2win = self.ball.x - self.ball.size < 0
        if player2win:
            self.player2.score += 1
            self.ball.reset()
        elif player1win:
            self.player1.score += 1
            self.ball.reset()

    def showPlayerNames(self):
        self.player1.showName()
        self.player2.showName()

    def showPlayerScores(self):
        self.player1.showScore()
        self.player2.showScore()

    def showLine(self):
        pygame.draw.line(SCREEN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))


class Ball:
    def __init__(self, color=WHITE):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.x_speed = choice([-1, 1])
        self.y_speed = choice([-1, 1])
        self.size = 10
        self.color = color
        self.shots = 0

    def show(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def checkforEdges(self):
        if self.y > HEIGHT or self.y < 0:
            pygame.mixer.Sound.play(BOUNCE)
            self.y_speed *= -1

    def reset(self):
        self.x_speed = choice([-1, 1])
        self.y_speed = choice([-1, 1])
        self.shots = 0
        self.x = randint(WIDTH//2-70, WIDTH//2+70)
        self.y = randint(HEIGHT//2 - 70, HEIGHT//2 + 70)

    def leaveScreen(self):
        self.reset() if self.x > WIDTH or self.x < 0 else ''


class Player:
    def __init__(self, no, name):
        self.no = no
        self.name = name
        self.score = 0
        self.createPaddle()
        self.setKeys()
        self.setScorepos()

    def setScorepos(self):
        self.namepos = (30, 0) if self.no == 1 else (WIDTH-100, 0)
        self.scorepos = (30, 50) if self.no == 1 else (WIDTH-100, 50)

    def createPaddle(self):
        self.paddle = Paddle(10) if self.no == 1 else Paddle(WIDTH-2*10)

    def setKeys(self):
        self.upKey = pygame.K_w if self.no == 1 else pygame.K_UP
        self.downKey = pygame.K_s if self.no == 1 else pygame.K_DOWN

    def movePaddle(self):
        keys = pygame.key.get_pressed()
        self.paddle.moveUp() if keys[self.upKey] else ''
        self.paddle.moveDown() if keys[self.downKey] else ''

    def showName(self):
        name_label = gameFont.render(str(self.name), True, WHITE, BLACK)
        SCREEN.blit(name_label, self.namepos)

    def showScore(self):
        score = gameFont.render(str(self.score), True, WHITE, BLACK)
        SCREEN.blit(score, self.scorepos)


class Computer(Player):
    def __init__(self):
        super().__init__(1, 'Computer')
        self.paddle = Paddle(10)
        self.paddle.speed = 1

    def computerAI(self, ball):
        if ball.x < WIDTH//2 and ball.x_speed < 0:
            if ball.y < self.paddle.y+self.paddle.length//2:
                self.paddle.moveUp()
            elif ball.y > self.paddle.y+self.paddle.length//2:
                self.paddle.moveDown()


class Paddle:
    def __init__(self, x):
        self.width = 12
        self.length = HEIGHT//5
        self.x = x
        self.y = int(HEIGHT/2 - self.length/2)
        self.speed = 1
        self.rect = (self.x, self.y, self.width, self.length)
        self.rally = 5

    def show(self):
        pygame.draw.rect(SCREEN, WHITE, self.rect)

    def moveUp(self):
        self.y -= self.speed
        self.rect = (self.x, self.y, self.width, self.length)

    def moveDown(self):
        self.y += self.speed
        self.rect = (self.x, self.y+self.speed, self.width, self.length)

    def checkforEdges(self):
        self.y = HEIGHT-self.length if self.y+self.length > HEIGHT else self.y
        self.y = 0 if self.y < 0 else self.y
        self.rect = (self.x, self.y, self.width, self.length)

    def checkforBall(self, ball):
        leftright = self.x < ball.x < self.x+self.width
        topbottom = self.y < ball.y < self.y+self.length
        if leftright and topbottom:
            pygame.mixer.Sound.play(BOUNCE)
            ball.x_speed *= -1
            ball.shots += 0.5


def main():
    setWindow(TITLE, ICON)

    player1 = Player(1, 'Ayushi')
    player2 = Player(2, 'Hari')

    game = Game(player1, player2)
    game.start()


if __name__ == '__main__':
    main()
