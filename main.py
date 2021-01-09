import pygame
import random
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

# GLOBAL VARIABLES
WIDTH = 900
HEIGHT = 600
TITLE = "Ping Pong"
ICON = pygame.image.load("icon.png")

# FONTS
mainScreenFont = pygame.font.SysFont("Comic Sans MS", 40)
gameFont = pygame.font.SysFont("Comic Sans MS", 30)

# SOUNDS
bounce = pygame.mixer.Sound(os.path.join("sounds", 'bounce.wav'))

# COLORS
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
        self.computer = Computer()
        self.ball = ball
        self.game_mode = "computer"
        self.screen_mode = "main"

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
        screen.fill(BLACK)
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
        self.checkforPoint()
        self.player2.showName()
        self.computer.showName()
        self.showPlayerScores()
        self.showLine()
        pygame.display.update()

    def twoPlayerMode(self):
        screen.fill(BLACK)
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
        while self.running:
            if self.screen_mode == "main":
                self.mainPage()
            elif self.screen_mode == "game":
                self.startGame()

    def mainPage(self):
        font = pygame.font.SysFont("Comic Sans MS", 40)
        screen.fill(BLACK)
        self.end()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        startGameButton = font.render("START GAME", True, WHITE, BLACK)
        screen.blit(startGameButton, (WIDTH//2 - 130, HEIGHT//2-100))

        is_mouse_x = mouse_x >= WIDTH//2 - 130 and mouse_x <= WIDTH//2 - 130 + startGameButton.get_width()
        is_mouse_y = mouse_y >= HEIGHT//2 - 100 and mouse_y <= HEIGHT//2 - 100 + startGameButton.get_height()
        if is_mouse_x and is_mouse_y:
            self.screen_mode = "game"
        pygame.display.update()

    def startGame(self):
        while self.running:
            self.clock.tick(500)
            if self.game_mode == "twoplayer":
                self.twoPlayerMode()
            elif self.game_mode == "computer":
                self.computerMode()

    def end(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def checkforPoint(self):
        player1win = self.ball.x + self.ball.size
        player2win = self.ball.x - self.ball.size
        if player2win < 0:
            self.player2.score += 1
            self.ball.reset()
        elif player1win > WIDTH:
            self.player1.score += 1
            self.ball.reset()

    def showPlayerNames(self):
        self.player1.showName()
        self.player2.showName()

    def showPlayerScores(self):
        self.player1.showScore()
        self.player2.showScore()

    def showLine(self):
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))


class Ball:
    def __init__(self, color):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        self.x_speed = random.choice([-1, 1])
        self.y_speed = random.choice([-1, 1])
        self.size = 10
        self.color = color
        self.shots = 0

    def show(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def checkforEdges(self):
        if self.y > HEIGHT or self.y < 0:
            pygame.mixer.Sound.play(bounce)
            self.y_speed *= -1

    def reset(self):
        self.x_speed = random.choice([-1, 1])
        self.y_speed = random.choice([-1, 1])
        self.shots = 0
        self.x = random.randint(WIDTH//2-70, WIDTH//2+70)
        self.y = random.randint(HEIGHT//2 - 70, HEIGHT//2 + 70)

    def leaveScreen(self):
        if self.x > WIDTH or self.x < 0:
            self.reset()


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
        if self.no == 1:
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

    def showName(self):
        name_label = gameFont.render(str(self.name), True, WHITE, BLACK)
        screen.blit(name_label, self.namepos)

    def showScore(self):
        score = gameFont.render(str(self.score), True, WHITE, BLACK)
        screen.blit(score, self.scorepos)


class Computer(Player):
    def __init__(self):
        super().__init__(1, "Computer")
        self.paddle = Paddle(10)
        self.paddle.speed = 2

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
        self.speed = 3
        self.rect = (self.x, self.y, self.width, self.length)
        self.rally = 5

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
            pygame.mixer.Sound.play(bounce)
            ball.x_speed *= -1
            ball.shots += 0.5


def main():
    setTitle(TITLE)
    setIcon(ICON)

    player1 = Player(1, "Hari")
    player2 = Player(2, "Jyoti")
    ball = Ball(GREEN)

    game = Game(player1, player2, ball)
    game.start()


if __name__ == "__main__":
    main()
