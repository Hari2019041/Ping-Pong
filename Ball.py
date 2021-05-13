from config import *

class Ball:
    def __init__(self, color=WHITE):
        self.x = int(WIDTH / 2)
        self.y = int(HEIGHT / 2)
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
        self.x = randint(WIDTH // 2 - 70, WIDTH // 2 + 70)
        self.y = randint(HEIGHT // 2 - 70, HEIGHT // 2 + 70)

    def leaveScreen(self):
        self.reset() if self.x > WIDTH or self.x < 0 else ''
