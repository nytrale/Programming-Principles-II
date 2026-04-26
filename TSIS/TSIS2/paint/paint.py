# paint.py — Paint Application TSIS 2
# Practice 10 + 11 + новые инструменты

import pygame
import datetime
from collections import deque

pygame.init()

# ─────────────────────────────────────────────
# НАСТРОЙКИ
# ─────────────────────────────────────────────
WIDTH, HEIGHT = 1300, 650
TOOLBAR_H = 60
CANVAS_H = HEIGHT - TOOLBAR_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint — TSIS 2")
clock = pygame.time.Clock()

# Канвас — отдельная поверхность для рисования
canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill((255, 255, 255))

# ─────────────────────────────────────────────
# СОСТОЯНИЕ
# ─────────────────────────────────────────────
color       = (0, 0, 0)
mode        = "pencil"
brush_size  = 3          # small=2, medium=5, large=10
brush_sizes = [2, 5, 10]
brush_idx   = 0

drawing     = False
start_pos   = None
prev_pos    = None

# Для прямой линии — превью
line_preview = False

# Для текстового инструмента
text_mode    = False
text_pos     = None
text_input   = ""
font         = pygame.font.SysFont("Arial", 24)

# ─────────────────────────────────────────────
# ЦВЕТА ПАЛИТРЫ
# ─────────────────────────────────────────────
PALETTE = [
    (0,   0,   0),    # чёрный
    (255, 255, 255),  # белый
    (255, 0,   0),    # красный
    (0,   255, 0),    # зелёный
    (0,   0,   255),  # синий
    (255, 255, 0),    # жёлтый
    (255, 165, 0),    # оранжевый
    (128, 0,   128),  # фиолетовый
    (0,   255, 255),  # голубой
    (255, 105, 180),  # розовый
    (139, 69,  19),   # коричневый
    (128, 128, 128),  # серый
]

# ─────────────────────────────────────────────
# FLOOD FILL
# ─────────────────────────────────────────────
def flood_fill(surface, pos, fill_color):
    """Заливка области цветом (BFS алгоритм)."""
    x, y = pos
    w, h = surface.get_size()

    # Цвет в точке клика
    target_color = surface.get_at((x, y))[:3]
    fill_c = fill_color[:3]

    # Если цвет уже такой — ничего не делаем
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

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))


# ─────────────────────────────────────────────
# ОТРИСОВКА ТУЛБАРА
# ─────────────────────────────────────────────
def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, (180, 180, 180), (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 2)

    tb_font = pygame.font.SysFont("Arial", 13)

    # Инструменты
    tools = [
        ("pencil",         "Pencil(P)"),
        ("line",           "Line(L)"),
        ("rect",           "Rect(R)"),
        ("circle",         "Circle(C)"),
        ("square",         "Square(4)"),
        ("right_triangle", "RTriangle(5)"),
        ("equilateral",    "ETriangle(6)"),
        ("rhombus",        "Rhombus(7)"),
        ("fill",           "Fill(F)"),
        ("text",           "Text(T)"),
        ("eraser",         "Eraser(E)"),
    ]

    x = 5
    for tool_mode, label in tools:
        active = (mode == tool_mode)
        bg = (100, 149, 237) if active else (200, 200, 200)
        pygame.draw.rect(screen, bg, (x, 8, 72, 28), border_radius=5)
        txt = tb_font.render(label, True, (255,255,255) if active else (0,0,0))
        screen.blit(txt, (x + 4, 16))
        x += 76

    # Размер кисти
    size_x = x + 5
    for i, s in enumerate(brush_sizes):
        active = (brush_idx == i)
        bg = (100, 149, 237) if active else (200, 200, 200)
        label = f"S{i+1}"
        pygame.draw.rect(screen, bg, (size_x, 8, 32, 28), border_radius=5)
        txt = tb_font.render(label, True, (255,255,255) if active else (0,0,0))
        screen.blit(txt, (size_x + 6, 16))
        size_x += 36

    # Палитра цветов
    pal_x = size_x + 10
    for i, c in enumerate(PALETTE):
        rect = pygame.Rect(pal_x + i * 26, 10, 24, 24)
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, (0,0,0), rect, 1)
        if c == color:
            pygame.draw.rect(screen, (255, 215, 0), rect, 3)

    # Текущий цвет
    pygame.draw.rect(screen, color, (WIDTH - 50, 10, 36, 36))
    pygame.draw.rect(screen, (0,0,0), (WIDTH - 50, 10, 36, 36), 2)


# ─────────────────────────────────────────────
# ГЛАВНЫЙ ЦИКЛ
# ─────────────────────────────────────────────
running = True
while running:
    # Копия канваса для превью линии
    canvas_preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ── Клавиатура ──
        if event.type == pygame.KEYDOWN:

            # Текстовый режим — ввод символов
            if text_mode:
                if event.key == pygame.K_RETURN:
                    # Подтверждаем текст — рисуем на канвасе
                    if text_input:
                        rendered = font.render(text_input, True, color)
                        canvas.blit(rendered, text_pos)
                    text_mode  = False
                    text_input = ""
                    text_pos   = None
                elif event.key == pygame.K_ESCAPE:
                    text_mode  = False
                    text_input = ""
                    text_pos   = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
                continue  # не обрабатываем другие клавиши в текст режиме

            # Сохранение Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_META):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename  = f"canvas_{timestamp}.png"
                pygame.image.save(canvas, filename)
                print(f"Сохранено: {filename}")

            # Инструменты
            if event.key == pygame.K_p: mode = "pencil"
            if event.key == pygame.K_l: mode = "line"
            if event.key == pygame.K_r: mode = "rect"
            if event.key == pygame.K_c: mode = "circle"
            if event.key == pygame.K_e: mode = "eraser"
            if event.key == pygame.K_f: mode = "fill"
            if event.key == pygame.K_t: mode = "text"
            if event.key == pygame.K_4: mode = "square"
            if event.key == pygame.K_5: mode = "right_triangle"
            if event.key == pygame.K_6: mode = "equilateral"
            if event.key == pygame.K_7: mode = "rhombus"

            # Размер кисти
            if event.key == pygame.K_F1: brush_idx = 0; brush_size = brush_sizes[0]
            if event.key == pygame.K_F2: brush_idx = 1; brush_size = brush_sizes[1]
            if event.key == pygame.K_F3: brush_idx = 2; brush_size = brush_sizes[2]

        # ── Клик мышью ──
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Клик по тулбару
            if my < TOOLBAR_H:
                # Проверяем кнопки инструментов
                tools_list = ["pencil","line","rect","circle","square",
                              "right_triangle","equilateral","rhombus","fill","text","eraser"]
                x = 5
                for t in tools_list:
                    if x <= mx <= x + 72 and 8 <= my <= 36:
                        mode = t
                        break
                    x += 76

                # Кнопки размера
                size_x = x + 5
                for i in range(3):
                    if size_x <= mx <= size_x + 32 and 8 <= my <= 36:
                        brush_idx  = i
                        brush_size = brush_sizes[i]
                        break
                    size_x += 36

                # Палитра
                pal_x = size_x + 10
                for i, c in enumerate(PALETTE):
                    if pal_x + i*26 <= mx <= pal_x + i*26 + 24 and 10 <= my <= 34:
                        color = c
                        break
                continue

            # Клик по канвасу
            canvas_y = my - TOOLBAR_H
            canvas_pos = (mx, canvas_y)

            if mode == "fill":
                flood_fill(canvas, canvas_pos, color)

            elif mode == "text":
                text_mode = True
                text_pos  = canvas_pos
                text_input = ""

            else:
                drawing   = True
                start_pos = canvas_pos
                prev_pos  = canvas_pos

        # ── Отпускание мыши ──
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                mx, my = event.pos
                canvas_y  = my - TOOLBAR_H
                end_pos   = (mx, canvas_y)

                if mode == "line":
                    pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

                elif mode == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(end_pos[0] - start_pos[0])
                    h = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

                elif mode == "circle":
                    cx = (start_pos[0] + end_pos[0]) // 2
                    cy = (start_pos[1] + end_pos[1]) // 2
                    r  = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5 // 2)
                    pygame.draw.circle(canvas, color, (cx, cy), max(r, 1), brush_size)

                elif mode == "square":
                    size = min(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, color, (start_pos[0], start_pos[1], size, size), brush_size)

                elif mode == "right_triangle":
                    pygame.draw.polygon(canvas, color, [
                        start_pos,
                        (end_pos[0], start_pos[1]),
                        end_pos
                    ], brush_size)

                elif mode == "equilateral":
                    x, y = start_pos
                    size = abs(end_pos[0] - start_pos[0]) or 60
                    pygame.draw.polygon(canvas, color, [
                        (x, y),
                        (x + size, y),
                        (x + size // 2, y - size)
                    ], brush_size)

                elif mode == "rhombus":
                    x, y = start_pos
                    size = max(abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1])) // 2 or 40
                    pygame.draw.polygon(canvas, color, [
                        (x, y - size),
                        (x + size, y),
                        (x, y + size),
                        (x - size, y)
                    ], brush_size)

            drawing   = False
            start_pos = None
            prev_pos  = None

        # ── Движение мыши ──
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            if my < TOOLBAR_H:
                continue
            canvas_y    = my - TOOLBAR_H
            canvas_pos  = (mx, canvas_y)

            if drawing:
                if mode == "pencil":
                    if prev_pos:
                        pygame.draw.line(canvas, color, prev_pos, canvas_pos, brush_size)
                    prev_pos = canvas_pos

                elif mode == "eraser":
                    pygame.draw.circle(canvas, (255, 255, 255), canvas_pos, brush_size * 5)
                    prev_pos = canvas_pos

    # ── Отрисовка ──
    screen.fill((230, 230, 230))

    # Превью линии пока тянем
    if drawing and mode == "line" and start_pos:
        mx, my = pygame.mouse.get_pos()
        canvas_y = my - TOOLBAR_H
        pygame.draw.line(canvas_preview, color, start_pos, (mx, canvas_y), brush_size)
        screen.blit(canvas_preview, (0, TOOLBAR_H))
    else:
        screen.blit(canvas, (0, TOOLBAR_H))

    # Превью текста пока печатаем
    if text_mode and text_pos:
        preview_surf = font.render(text_input + "|", True, color)
        screen.blit(preview_surf, (text_pos[0], text_pos[1] + TOOLBAR_H))

    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()