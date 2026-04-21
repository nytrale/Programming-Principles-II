import pygame
import random
import sys


pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


font_small = pygame.font.SysFont("Arial", 24)
font_medium = pygame.font.SysFont("Arial", 36)
font_large = pygame.font.SysFont("Arial", 56)


BG_COLOR = (20, 20, 30)
GRID_COLOR = (35, 35, 50)
SNAKE_HEAD_COLOR = (0, 220, 120)
SNAKE_BODY_COLOR = (0, 170, 90)
FOOD_COLOR = (220, 70, 70)
TEXT_COLOR = (240, 240, 240)
WALL_COLOR = (90, 90, 110)
PANEL_COLOR = (30, 30, 45)


START_SPEED = 8



def draw_text(text, font, color, x, y, center=False):
    """Draw text on the screen."""
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def draw_grid():
    """Draw background grid."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_walls(walls):
    """Draw wall blocks."""
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall, border_radius=4)


def draw_snake(snake):
    """Draw snake head and body."""
    for i, segment in enumerate(snake):
        rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
        if i == 0:
            pygame.draw.rect(screen, SNAKE_HEAD_COLOR, rect, border_radius=6)
        else:
            pygame.draw.rect(screen, SNAKE_BODY_COLOR, rect, border_radius=6)


def draw_food(food):
    """Draw food."""
    rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, FOOD_COLOR, rect, border_radius=10)


def draw_info_panel(score, level, speed):
    """Draw top information panel."""
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 50))
    draw_text(f"Score: {score}", font_small, TEXT_COLOR, 15, 12)
    draw_text(f"Level: {level}", font_small, TEXT_COLOR, 180, 12)
    draw_text(f"Speed: {speed}", font_small, TEXT_COLOR, 330, 12)


def show_start_screen():
    """Start screen before the game begins."""
    while True:
        screen.fill(BG_COLOR)
        draw_text("SNAKE", font_large, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 80, center=True)
        draw_text("Press SPACE to start", font_medium, TEXT_COLOR, WIDTH // 2, HEIGHT // 2, center=True)
        draw_text("Use arrow keys to move", font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 60, center=True)
        draw_text("Avoid walls and yourself", font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 95, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def show_game_over(score, level):
    """Game over screen."""
    while True:
        screen.fill(BG_COLOR)
        draw_text("GAME OVER", font_large, FOOD_COLOR, WIDTH // 2, HEIGHT // 2 - 90, center=True)
        draw_text(f"Final Score: {score}", font_medium, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 20, center=True)
        draw_text(f"Level Reached: {level}", font_medium, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 25, center=True)
        draw_text("Press R to restart or ESC to quit", font_small, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 90, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def create_walls():
    """
    Create wall obstacles.
    They are placed on the grid, so snake and food work correctly.
    """
    walls = [
        pygame.Rect(240, 180, CELL_SIZE, 140),
        pygame.Rect(540, 260, CELL_SIZE, 140),
        pygame.Rect(360, 420, 140, CELL_SIZE)
    ]
    return walls


def random_food_position(snake, walls):
    """
    Generate random position for food.
    Food must not appear on the snake or inside walls.
    """
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(60, HEIGHT, CELL_SIZE)
        food_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        on_snake = (x, y) in snake
        on_wall = any(food_rect.colliderect(wall) for wall in walls)

        if not on_snake and not on_wall:
            return (x, y)


def check_wall_collision(head, walls):
    """Check collision between snake head and walls."""
    head_rect = pygame.Rect(head[0], head[1], CELL_SIZE, CELL_SIZE)
    return any(head_rect.colliderect(wall) for wall in walls)


def run_game():
    """Main game function."""
    snake = [(140, 100), (120, 100), (100, 100)]
    direction = (CELL_SIZE, 0)

    score = 0
    level = 1
    speed = START_SPEED

    foods_to_next_level = 4

    walls = create_walls()
    food = random_food_position(snake, walls)

    while True:
        clock.tick(speed)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)


        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]
        new_head = (head_x, head_y)

        # Border collision
        if head_x < 0 or head_x >= WIDTH or head_y < 50 or head_y >= HEIGHT:
            return score, level

        # Self collision
        if new_head in snake:
            return score, level

        # Wall collision
        if check_wall_collision(new_head, walls):
            return score, level

        snake.insert(0, new_head)

        # Food collision
        if new_head == food:
            score += 1
            food = random_food_position(snake, walls)

            # Level up every 4 foods
            if score % foods_to_next_level == 0:
                level += 1
                speed += 2
        else:
            snake.pop()


        screen.fill(BG_COLOR)
        draw_grid()
        draw_info_panel(score, level, speed)
        draw_walls(walls)
        draw_food(food)
        draw_snake(snake)

        pygame.display.update()



while True:
    show_start_screen()
    final_score, final_level = run_game()
    show_game_over(final_score, final_level)