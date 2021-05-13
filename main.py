from config import *
from Paddle import Paddle
from Player import Player, Computer
from Ball import Ball

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

    def playGame(self):
        SCREEN.fill(BLACK)
        self.end()
        self.ball.show()
        self.ball.move()
        self.ball.checkforEdges()

        self.player1.usePaddle(self.ball)
        self.player2.usePaddle(self.ball)

        self.gameMethods()
        pygame.display.update()

    def start(self):
        while self.RUNNING:
            self.mainPage() if self.screen_mode == 'main' else ''
            self.startGame() if self.screen_mode == 'game' else ''

    def mainPage(self):
        font = mainScreenFont
        SCREEN.fill(BLACK)

        def startGameButton():
            text = font.render('START GAME', True, BLACK, WHITE)
            x_pos = WIDTH // 2 - text.get_width() // 2
            y_pos = HEIGHT // 2 - text.get_height() // 2 - 150
            startGameRect = pygame.Rect((x_pos, y_pos, text.get_width(), text.get_height()))
            SCREEN.blit(text, (x_pos, y_pos))

            return startGameRect

        mouse_x, mouse_y = pygame.mouse.get_pos()

        clicked = False
        for event in pygame.event.get():
            self.RUNNING = False if event.type == pygame.QUIT else True
            clicked = True if event.type == pygame.MOUSEBUTTONDOWN else False

        startGame = startGameButton().collidepoint((mouse_x, mouse_y))
        self.screen_mode = 'game' if startGame and clicked else 'main'

        pygame.display.update()

    def startGame(self):
        while self.RUNNING:
            self.clock.tick(self.FPS)
            self.player1 = self.computer if self.game_mode == 'computer' else self.player1
            self.playGame()

    def end(self):
        for event in pygame.event.get():
            self.RUNNING = False if event.type == pygame.QUIT else True

    def checkforPoint(self):
        player1win = self.ball.x + self.ball.size > WIDTH
        player2win = self.ball.x - self.ball.size < 0
        self.player2.score += 1 if player2win else 0
        self.player1.score += 1 if player1win else 0
        self.ball.reset() if player1win or player2win else ''

    def showPlayerNames(self):
        self.player1.showName()
        self.player2.showName()

    def showPlayerScores(self):
        self.player1.showScore()
        self.player2.showScore()

    def showLine(self):
        pygame.draw.line(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    def gameMethods(self):
        self.checkforPoint()
        self.showPlayerNames()
        self.showPlayerScores()
        self.showLine()

def main():
    setWindow(TITLE, ICON)

    player1 = Player(1, 'Jyoti')
    player2 = Player(2, 'Hari')

    game = Game(player1, player2)
    game.start()


if __name__ == '__main__':
    main()
