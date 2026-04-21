import pygame
import sys
import math

pygame.init()

# Window
WIDTH, HEIGHT = 1000, 700
TOOLBAR_H = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Canvas
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
GREEN = (60, 180, 90)
BLUE = (70, 120, 220)
YELLOW = (240, 220, 70)
GRAY = (220, 220, 220)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)
tool = "brush"
color = BLACK
drawing = False
start_pos = None
last_pos = None
brush_size = 5

colors = [BLACK, RED, GREEN, BLUE, YELLOW]
color_rects = [pygame.Rect(20 + i * 50, 20, 35, 35) for i in range(len(colors))]

def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))

    for i, rect in enumerate(color_rects):
        pygame.draw.rect(screen, colors[i], rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    text = font.render(f"Tool: {tool}   Keys: B-brush R-rect C-circle E-eraser", True, BLACK)
    screen.blit(text, (320, 25))

def get_rect(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True
preview_pos = None

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Color selection
            if y < TOOLBAR_H:
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(event.pos):
                        color = colors[i]
            else:
                drawing = True
                start_pos = (x, y - TOOLBAR_H)
                last_pos = start_pos
                preview_pos = start_pos

                if tool == "brush":
                    pygame.draw.circle(canvas, color, start_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, start_pos, 15)

        if event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            if y > TOOLBAR_H:
                current_pos = (x, y - TOOLBAR_H)
                preview_pos = current_pos

                if tool == "brush":
                    pygame.draw.line(canvas, color, last_pos, current_pos, brush_size * 2)
                    last_pos = current_pos
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, 30)
                    last_pos = current_pos

        if event.type == pygame.MOUSEBUTTONUP and drawing:
            x, y = event.pos
            if y > TOOLBAR_H:
                end_pos = (x, y - TOOLBAR_H)

                if tool == "rect":
                    pygame.draw.rect(canvas, color, get_rect(start_pos, end_pos), 3)
                elif tool == "circle":
                    radius = int(math.dist(start_pos, end_pos))
                    pygame.draw.circle(canvas, color, start_pos, radius, 3)

            drawing = False
            start_pos = None
            last_pos = None
            preview_pos = None

    screen.fill(WHITE)
    draw_toolbar()
    screen.blit(canvas, (0, TOOLBAR_H))

    # Shape preview
    if drawing and tool in ["rect", "circle"] and start_pos and preview_pos:
        temp = canvas.copy()
        if tool == "rect":
            pygame.draw.rect(temp, color, get_rect(start_pos, preview_pos), 2)
        elif tool == "circle":
            radius = int(math.dist(start_pos, preview_pos))
            pygame.draw.circle(temp, color, start_pos, radius, 2)
        screen.blit(temp, (0, TOOLBAR_H))

    pygame.display.update()

pygame.quit()
sys.exit()