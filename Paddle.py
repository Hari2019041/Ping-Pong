from config import *

class Paddle:
    def __init__(self, x):
        self.width = 10
        self.length = HEIGHT // 5
        self.x = x
        self.y = int(HEIGHT / 2 - self.length / 2)
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
        self.rect = (self.x, self.y + self.speed, self.width, self.length)

    def checkforEdges(self):
        self.y = HEIGHT - self.length if self.y + self.length > HEIGHT else self.y
        self.y = 0 if self.y < 0 else self.y
        self.rect = (self.x, self.y, self.width, self.length)

    def checkforBall(self, ball):
        leftright = self.x < ball.x < self.x + self.width
        topbottom = self.y < ball.y < self.y + self.length
        if leftright and topbottom:
            pygame.mixer.Sound.play(BOUNCE)
            ball.x_speed *= -1
            ball.shots += 0.5
