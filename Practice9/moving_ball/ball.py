import sys
import pygame


class MovingBallGame:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Moving Ball")
        self.clock = pygame.time.Clock()

        self.white = (255, 255, 255)
        self.red = (255, 0, 0)

        self.radius = 25
        self.step = 20

        self.x = self.width // 2
        self.y = self.height // 2

    def move_left(self):
        if self.x - self.step - self.radius >= 0:
            self.x -= self.step

    def move_right(self):
        if self.x + self.step + self.radius <= self.width:
            self.x += self.step

    def move_up(self):
        if self.y - self.step - self.radius >= 0:
            self.y -= self.step

    def move_down(self):
        if self.y + self.step + self.radius <= self.height:
            self.y += self.step

    def draw_ball(self):
        self.screen.fill(self.white)
        pygame.draw.circle(self.screen, self.red, (self.x, self.y), self.radius)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_UP:
                        self.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()

            self.draw_ball()
            pygame.display.flip()
            self.clock.tick(60)