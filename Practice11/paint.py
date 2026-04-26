"""
Paint - Practice 11

Adds square, right triangle, equilateral triangle, and rhombus drawing tools.
Keys: B brush, E eraser, S square, T right triangle, Y equilateral triangle,
H rhombus, number keys choose colors.
"""
import math
import sys

import pygame

WIDTH, HEIGHT = 920, 660
TOOLBAR_H = 76
FPS = 60

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (210, 210, 210)
DARK = (45, 45, 52)
COLORS = [
    (20, 20, 20),
    (230, 57, 70),
    (29, 140, 80),
    (42, 111, 219),
    (252, 186, 3),
    (157, 78, 221),
]


def square_rect(start, end):
    side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x = start[0] if end[0] >= start[0] else start[0] - side
    y = start[1] if end[1] >= start[1] else start[1] - side
    return pygame.Rect(x, y, side, side)


def right_triangle_points(start, end):
    return [start, (start[0], end[1]), end]


def equilateral_points(start, end):
    side = end[0] - start[0]
    height = abs(side) * math.sqrt(3) / 2
    apex_y = start[1] - height if end[1] < start[1] else start[1] + height
    return [start, (end[0], start[1]), ((start[0] + end[0]) / 2, apex_y)]


def rhombus_points(start, end):
    cx = (start[0] + end[0]) / 2
    cy = (start[1] + end[1]) / 2
    return [(cx, start[1]), (end[0], cy), (cx, end[1]), (start[0], cy)]


def draw_shape(surface, tool, start, end, color):
    if tool == "square":
        pygame.draw.rect(surface, color, square_rect(start, end), 3)
    elif tool == "right triangle":
        pygame.draw.polygon(surface, color, right_triangle_points(start, end), 3)
    elif tool == "equilateral":
        pygame.draw.polygon(surface, color, equilateral_points(start, end), 3)
    elif tool == "rhombus":
        pygame.draw.polygon(surface, color, rhombus_points(start, end), 3)


def draw_toolbar(screen, font, tool, color):
    pygame.draw.rect(screen, DARK, (0, 0, WIDTH, TOOLBAR_H))
    title = font.render(f"Tool: {tool.upper()}", True, WHITE)
    screen.blit(title, (16, 24))
    for i, swatch in enumerate(COLORS):
        rect = pygame.Rect(185 + i * 42, 22, 28, 28)
        pygame.draw.rect(screen, swatch, rect, border_radius=4)
        pygame.draw.rect(screen, WHITE if swatch == color else GRAY, rect, 3, border_radius=4)
    hint = font.render("B brush  E eraser  S square  T right tri  Y eq tri  H rhombus  1-6 colors", True, GRAY)
    screen.blit(hint, (455, 24))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 11 - Paint")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
    canvas.fill(WHITE)
    tool = "brush"
    color = COLORS[0]
    drawing = False
    start_pos = None
    last_pos = None

    shape_tools = {"square", "right triangle", "equilateral", "rhombus"}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        canvas_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_H)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                key_tools = {
                    pygame.K_b: "brush",
                    pygame.K_e: "eraser",
                    pygame.K_s: "square",
                    pygame.K_t: "right triangle",
                    pygame.K_y: "equilateral",
                    pygame.K_h: "rhombus",
                }
                if event.key in key_tools:
                    tool = key_tools[event.key]
                elif pygame.K_1 <= event.key <= pygame.K_6:
                    color = COLORS[event.key - pygame.K_1]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse_pos[1] >= TOOLBAR_H:
                drawing = True
                start_pos = canvas_pos
                last_pos = canvas_pos
            elif event.type == pygame.MOUSEMOTION and drawing and tool in ("brush", "eraser"):
                draw_color = WHITE if tool == "eraser" else color
                size = 18 if tool == "eraser" else 5
                pygame.draw.line(canvas, draw_color, last_pos, canvas_pos, size)
                last_pos = canvas_pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                drawing = False
                if tool in shape_tools:
                    draw_shape(canvas, tool, start_pos, canvas_pos, color)

        screen.fill(WHITE)
        screen.blit(canvas, (0, TOOLBAR_H))
        if drawing and tool in shape_tools:
            preview = screen.copy()
            shifted_start = (start_pos[0], start_pos[1] + TOOLBAR_H)
            draw_shape(preview, tool, shifted_start, mouse_pos, color)
            screen.blit(preview, (0, 0))
        draw_toolbar(screen, font, tool, color)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()