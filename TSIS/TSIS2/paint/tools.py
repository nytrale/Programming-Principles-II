
import pygame
import datetime
from collections import deque

def flood_fill(surface, pos, fill_color):
    x, y = pos
    w, h = surface.get_size()

    target_color = surface.get_at((x, y))[:3]
    fill_c = fill_color[:3]

    if target_color == fill_c:
        return

    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != target_color:
            continue
        surface.set_at((cx, cy), fill_c)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))




def draw_rect(surface, color, start, end, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    pygame.draw.rect(surface, color, (x, y, w, h), size)


def draw_circle(surface, color, start, end, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    r  = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 // 2)
    pygame.draw.circle(surface, color, (cx, cy), max(r, 1), size)


def draw_square(surface, color, start, end, size):
    s = min(abs(end[0]-start[0]), abs(end[1]-start[1]))
    pygame.draw.rect(surface, color, (start[0], start[1], s, s), size)


def draw_right_triangle(surface, color, start, end, size):
    pygame.draw.polygon(surface, color, [
        start,
        (end[0], start[1]),
        end
    ], size)


def draw_equilateral(surface, color, start, end, size):
    x, y = start
    s = abs(end[0] - start[0]) or 60
    pygame.draw.polygon(surface, color, [
        (x, y),
        (x + s, y),
        (x + s // 2, y - s)
    ], size)


def draw_rhombus(surface, color, start, end, size):
    x, y = start
    s = max(abs(end[0]-start[0]), abs(end[1]-start[1])) // 2 or 40
    pygame.draw.polygon(surface, color, [
        (x, y - s),
        (x + s, y),
        (x, y + s),
        (x - s, y)
    ], size)


def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)


def draw_pencil(surface, color, prev, curr, size):
    if prev:
        pygame.draw.line(surface, color, prev, curr, size)


def draw_eraser(surface, pos, size):
    pygame.draw.circle(surface, (255, 255, 255), pos, size * 5)




def render_text(surface, text, pos, color, font):
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)


def preview_text(surface, text, pos, color, font, toolbar_h):
    rendered = font.render(text + "|", True, color)
    surface.blit(rendered, (pos[0], pos[1] + toolbar_h))



def save_canvas(surface):
    """Сохраняет канвас в PNG с временной меткой."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"canvas_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Сохранено: {filename}")
    return filename