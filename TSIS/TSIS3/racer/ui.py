# ui.py — экраны игры (меню, настройки, лидерборд, game over)

import pygame
from persistence import load_leaderboard, save_settings

# ─────────────────────────────────────────────
# ЦВЕТА
# ─────────────────────────────────────────────
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (100, 100, 100)
DARK   = (30,  30,  30)
BLUE   = (50,  120, 220)
GREEN  = (50,  200, 50)
RED    = (220, 50,  50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)


# ─────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────

def draw_button(screen, text, rect, font, active=False):
    """Рисует кнопку и возвращает True если нажата."""
    color = BLUE if active else GRAY
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect.collidepoint(pygame.mouse.get_pos())


def draw_text_center(screen, text, font, color, y, width):
    """Рисует текст по центру экрана."""
    txt = font.render(text, True, color)
    screen.blit(txt, (width // 2 - txt.get_width() // 2, y))


# ─────────────────────────────────────────────
# ГЛАВНОЕ МЕНЮ
# ─────────────────────────────────────────────

def main_menu(screen, width, height):
    """
    Возвращает: 'play', 'leaderboard', 'settings', 'quit'
    """
    font_big   = pygame.font.SysFont("Arial", 52, bold=True)
    font_med   = pygame.font.SysFont("Arial", 30)

    btn_play   = pygame.Rect(width//2 - 110, 200, 220, 55)
    btn_leader = pygame.Rect(width//2 - 110, 270, 220, 55)
    btn_sett   = pygame.Rect(width//2 - 110, 340, 220, 55)
    btn_quit   = pygame.Rect(width//2 - 110, 410, 220, 55)

    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK)
        draw_text_center(screen, "RACER", font_big, YELLOW, 100, width)

        mx, my = pygame.mouse.get_pos()
        click  = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        draw_button(screen, "Play",        btn_play,   font_med, btn_play.collidepoint(mx, my))
        draw_button(screen, "Leaderboard", btn_leader, font_med, btn_leader.collidepoint(mx, my))
        draw_button(screen, "Settings",    btn_sett,   font_med, btn_sett.collidepoint(mx, my))
        draw_button(screen, "Quit",        btn_quit,   font_med, btn_quit.collidepoint(mx, my))

        if click:
            if btn_play.collidepoint(mx, my):   return "play"
            if btn_leader.collidepoint(mx, my): return "leaderboard"
            if btn_sett.collidepoint(mx, my):   return "settings"
            if btn_quit.collidepoint(mx, my):   return "quit"

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
# ВВОД ИМЕНИ
# ─────────────────────────────────────────────

def username_screen(screen, width, height):
    """Экран ввода имени игрока. Возвращает строку с именем."""
    font_big = pygame.font.SysFont("Arial", 40, bold=True)
    font_med = pygame.font.SysFont("Arial", 28)
    font_sml = pygame.font.SysFont("Arial", 22)

    username = ""
    clock    = pygame.time.Clock()

    while True:
        screen.fill(DARK)
        draw_text_center(screen, "Enter Your Name", font_big, YELLOW, 150, width)
        draw_text_center(screen, username + "|", font_med, WHITE, 240, width)
        draw_text_center(screen, "Press Enter to Start", font_sml, GRAY, 310, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 16:
                    username += event.unicode

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
# ЭКРАН НАСТРОЕК
# ─────────────────────────────────────────────

def settings_screen(screen, width, height, settings):
    """Экран настроек. Возвращает обновлённые настройки."""
    font_big = pygame.font.SysFont("Arial", 40, bold=True)
    font_med = pygame.font.SysFont("Arial", 26)

    btn_sound  = pygame.Rect(width//2 - 110, 180, 220, 50)
    btn_easy   = pygame.Rect(width//2 - 170, 260, 100, 50)
    btn_normal = pygame.Rect(width//2 - 50,  260, 100, 50)
    btn_hard   = pygame.Rect(width//2 + 70,  260, 100, 50)

    btn_def    = pygame.Rect(width//2 - 200, 350, 80, 50)
    btn_red    = pygame.Rect(width//2 - 100, 350, 80, 50)
    btn_blue   = pygame.Rect(width//2,       350, 80, 50)
    btn_green  = pygame.Rect(width//2 + 100, 350, 80, 50)

    btn_back   = pygame.Rect(width//2 - 80, 450, 160, 50)

    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK)
        draw_text_center(screen, "Settings", font_big, YELLOW, 80, width)

        mx, my = pygame.mouse.get_pos()
        click  = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Звук
        sound_label = "Sound: ON" if settings["sound"] else "Sound: OFF"
        draw_button(screen, sound_label, btn_sound, font_med, btn_sound.collidepoint(mx, my))

        # Сложность
        draw_text_center(screen, "Difficulty:", font_med, WHITE, 230, width)
        draw_button(screen, "Easy",   btn_easy,   font_med, settings["difficulty"] == "easy")
        draw_button(screen, "Normal", btn_normal, font_med, settings["difficulty"] == "normal")
        draw_button(screen, "Hard",   btn_hard,   font_med, settings["difficulty"] == "hard")

        # Цвет машины
        draw_text_center(screen, "Car Color:", font_med, WHITE, 320, width)
        pygame.draw.rect(screen, WHITE,              btn_def,   border_radius=8)
        pygame.draw.rect(screen, RED,                btn_red,   border_radius=8)
        pygame.draw.rect(screen, BLUE,               btn_blue,  border_radius=8)
        pygame.draw.rect(screen, GREEN,              btn_green, border_radius=8)

        # Подсветка выбранного цвета
        color_map = {"default": btn_def, "red": btn_red, "blue": btn_blue, "green": btn_green}
        sel_rect  = color_map.get(settings["car_color"], btn_def)
        pygame.draw.rect(screen, YELLOW, sel_rect, 4, border_radius=8)

        draw_button(screen, "◀  Back", btn_back, font_med, btn_back.collidepoint(mx, my))

        if click:
            if btn_sound.collidepoint(mx, my):
                settings["sound"] = not settings["sound"]
            if btn_easy.collidepoint(mx, my):   settings["difficulty"] = "easy"
            if btn_normal.collidepoint(mx, my): settings["difficulty"] = "normal"
            if btn_hard.collidepoint(mx, my):   settings["difficulty"] = "hard"
            if btn_def.collidepoint(mx, my):    settings["car_color"]  = "default"
            if btn_red.collidepoint(mx, my):    settings["car_color"]  = "red"
            if btn_blue.collidepoint(mx, my):   settings["car_color"]  = "blue"
            if btn_green.collidepoint(mx, my):  settings["car_color"]  = "green"
            if btn_back.collidepoint(mx, my):
                save_settings(settings)
                return settings

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
# ЛИДЕРБОРД
# ─────────────────────────────────────────────

def leaderboard_screen(screen, width, height):
    """Экран лидерборда."""
    font_big = pygame.font.SysFont("Arial", 40, bold=True)
    font_med = pygame.font.SysFont("Arial", 24)
    font_sml = pygame.font.SysFont("Arial", 20)

    btn_back = pygame.Rect(width//2 - 80, height - 70, 160, 50)
    clock    = pygame.time.Clock()

    leaderboard = load_leaderboard()   # читаем файл один раз, не в цикле

    while True:
        screen.fill(DARK)
        draw_text_center(screen, "Leaderboard", font_big, YELLOW, 40, width)

        for i, entry in enumerate(leaderboard):
            color = YELLOW if i == 0 else WHITE
            line  = f"{i+1}. {entry['name']}  —  Score: {entry['score']}  |  Distance: {entry['distance']}m"
            txt   = font_sml.render(line, True, color)
            screen.blit(txt, (40, 110 + i * 35))

        if not leaderboard:
            draw_text_center(screen, "No scores yet!", font_med, GRAY, 200, width)

        mx, my = pygame.mouse.get_pos()
        click  = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        draw_button(screen, "◀  Back", btn_back, font_med, btn_back.collidepoint(mx, my))

        if click and btn_back.collidepoint(mx, my):
            return

        pygame.display.flip()
        clock.tick(60)


# ─────────────────────────────────────────────
# GAME OVER
# ─────────────────────────────────────────────

def game_over_screen(screen, width, height, score, distance, coins):
    """
    Экран Game Over.
    Возвращает: 'retry' или 'menu'
    """
    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font_med = pygame.font.SysFont("Arial", 28)
    font_sml = pygame.font.SysFont("Arial", 22)

    btn_retry = pygame.Rect(width//2 - 120, 380, 220, 55)
    btn_menu  = pygame.Rect(width//2 - 120, 450, 220, 55)

    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK)
        draw_text_center(screen, "GAME OVER", font_big, RED, 100, width)
        draw_text_center(screen, f"Score:    {score}",    font_med, WHITE,  200, width)
        draw_text_center(screen, f"Distance: {distance}m", font_med, WHITE, 245, width)
        draw_text_center(screen, f"Coins:    {coins}",    font_med, YELLOW, 290, width)

        mx, my = pygame.mouse.get_pos()
        click  = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        draw_button(screen, "Retry",     btn_retry, font_med, btn_retry.collidepoint(mx, my))
        draw_button(screen, "Main Menu", btn_menu,  font_med, btn_menu.collidepoint(mx, my))

        if click:
            if btn_retry.collidepoint(mx, my): return "retry"
            if btn_menu.collidepoint(mx, my):  return "menu"

        pygame.display.flip()
        clock.tick(60)