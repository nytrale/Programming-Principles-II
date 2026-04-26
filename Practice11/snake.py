"""
Snake Game - Practice 11

Food has different weights and disappears after a timer. Higher levels make the
snake faster.
"""
import random
import sys

import pygame

CELL = 20
COLS, ROWS = 30, 24
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
FOOD_LIFETIME_MS = 5000

BLACK = (18, 18, 24)
WHITE = (245, 245, 245)
GREEN = (52, 168, 83)
DARK_GREEN = (29, 110, 55)
RED = (230, 72, 72)
ORANGE = (255, 170, 40)
PURPLE = (157, 78, 221)
GRAY = (60, 60, 70)

FOODS = [(1, RED), (2, ORANGE), (3, PURPLE)]


def random_free_cell(snake):
    occupied = set(snake)
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in occupied]
    return random.choice(free)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Practice 11 - Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.reset()

    def reset(self):
        self.snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.spawn_food()

    def spawn_food(self):
        self.food_pos = random_free_cell(self.snake)
        self.food_weight, self.food_color = random.choice(FOODS)
        self.food_spawn_time = pygame.time.get_ticks()

    def handle_key(self, key):
        if key == pygame.K_q:
            pygame.quit()
            sys.exit()
        if self.game_over and key == pygame.K_r:
            self.reset()
            return
        directions = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
        }
        if key in directions:
            new_direction = directions[key]
            if new_direction != (-self.direction[0], -self.direction[1]):
                self.next_direction = new_direction

    def update(self):
        if self.game_over:
            return

        if pygame.time.get_ticks() - self.food_spawn_time > FOOD_LIFETIME_MS:
            self.spawn_food()

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS) or new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food_pos:
            self.score += self.food_weight
            self.level = self.score // 5 + 1
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

        food_rect = pygame.Rect(self.food_pos[0] * CELL, self.food_pos[1] * CELL, CELL, CELL)
        pygame.draw.rect(self.screen, self.food_color, food_rect.inflate(-4, -4), border_radius=6)
        label = self.small_font.render(str(self.food_weight), True, WHITE)
        self.screen.blit(label, (food_rect.centerx - label.get_width() // 2, food_rect.centery - label.get_height() // 2))

        time_left = max(0, FOOD_LIFETIME_MS - (pygame.time.get_ticks() - self.food_spawn_time))
        hud = self.font.render(f"Score: {self.score}  Level: {self.level}  Food timer: {time_left // 1000 + 1}", True, WHITE)
        self.screen.blit(hud, (10, 8))

        for index, part in enumerate(self.snake):
            rect = pygame.Rect(part[0] * CELL, part[1] * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, GREEN if index == 0 else DARK_GREEN, rect.inflate(-2, -2), border_radius=5)

        if self.game_over:
            over = self.font.render("GAME OVER", True, RED)
            hint = self.small_font.render("R - restart, Q - quit", True, WHITE)
            self.screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 28))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 8))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
            self.update()
            self.draw()
            self.clock.tick(8 + self.level * 2)


if __name__ == "__main__":
    SnakeGame().run()