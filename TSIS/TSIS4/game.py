# game.py — игровая логика, отрисовка всех экранов

import random
import sys
from datetime import datetime

import pygame

from config import (
    CELL, COLS, ROWS, HUD_H, FIELD_Y, WIDTH, HEIGHT,
    FOOD_LIFETIME_MS, POWERUP_LIFETIME_MS, POWERUP_EFFECT_MS,
    BLACK, WHITE, RED, ORANGE, GRAY, DARK_RED, YELLOW,
    WALL_COLOR, BG_PANEL, ACCENT, DIM,
    FOODS, POWERUP_TYPES,
    load_settings, save_settings,
)
from db import (
    DB_AVAILABLE,
    db_get_or_create_player, db_save_session,
    db_get_leaderboard, db_get_personal_best,
)


# ════════════════════════════════════════════════════════════════════════════
# UI-хелперы
# ════════════════════════════════════════════════════════════════════════════

def draw_panel(surface, rect, color=BG_PANEL, radius=14, border_color=GRAY, border=2):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def draw_button(surface, font, text, rect, hovered=False):
    color  = (60, 180, 100) if hovered else (40, 120, 70)
    border = (120, 255, 160) if hovered else (52, 168, 83)
    draw_panel(surface, rect, color, radius=10, border_color=border, border=2)
    label = font.render(text, True, WHITE)
    surface.blit(label, (rect.centerx - label.get_width() // 2,
                         rect.centery - label.get_height() // 2))


def text_input_box(surface, font, prompt, rect, value, active):
    border_col = ACCENT if active else GRAY
    draw_panel(surface, rect, BG_PANEL, radius=8, border_color=border_col, border=2)
    if prompt:
        prompt_surf = font.render(prompt, True, DIM)
        surface.blit(prompt_surf, (rect.x, rect.y - 28))
    val_surf = font.render(value + ("|" if active else ""), True, WHITE)
    surface.blit(val_surf, (rect.x + 10, rect.centery - val_surf.get_height() // 2))


# ════════════════════════════════════════════════════════════════════════════
# Вспомогательные функции поля
# ════════════════════════════════════════════════════════════════════════════

def random_free_cell(snake, obstacles, food_pos=None, powerup_pos=None, poison_pos=None):
    occupied = set(snake) | set(map(tuple, obstacles))
    if food_pos:    occupied.add(food_pos)
    if powerup_pos: occupied.add(powerup_pos)
    if poison_pos:  occupied.add(poison_pos)
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in occupied]
    return random.choice(free) if free else None


def generate_obstacles(snake, count):
    """Расставить `count` блоков стен, не касаясь змейки."""
    head = snake[0]
    forbidden = set(map(tuple, snake))
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            forbidden.add((head[0] + dx, head[1] + dy))
    candidates = [(x, y) for x in range(COLS) for y in range(ROWS)
                  if (x, y) not in forbidden]
    random.shuffle(candidates)
    return candidates[:count]


# ════════════════════════════════════════════════════════════════════════════
# Главный класс игры
# ════════════════════════════════════════════════════════════════════════════

class SnakeGame:
    SCREEN_MENU        = "menu"
    SCREEN_USERNAME    = "username"
    SCREEN_GAME        = "game"
    SCREEN_GAMEOVER    = "gameover"
    SCREEN_LEADERBOARD = "leaderboard"
    SCREEN_SETTINGS    = "settings"

    def __init__(self, conn):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake – Extended")
        self.clock = pygame.time.Clock()
        self.conn  = conn

        # Шрифты
        self.font_big   = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_med   = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 18)
        self.font_tiny  = pygame.font.SysFont("Arial", 14)

        # Состояние
        self.settings      = load_settings()
        self.username      = ""
        self.player_id     = None
        self.personal_best = 0

        self.current_screen   = self.SCREEN_MENU
        self.leaderboard_data = []

        self._typing_target  = None
        self._tmp_settings   = {}
        self._tmp_color_input = ""

        self._init_game_state()

    # ── Инициализация игрового состояния ─────────────────────────────────────
    def _init_game_state(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake     = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_dir  = (1, 0)
        self.score     = 0
        self.level     = 1
        self.game_over = False
        self.obstacles = []

        self.food_pos    = None
        self.food_weight = 1
        self.food_color  = RED
        self.food_spawn  = 0

        self.poison_pos   = None
        self.poison_spawn = 0

        self.powerup_pos   = None
        self.powerup_type  = None
        self.powerup_spawn = 0

        self.active_effect     = None
        self.active_effect_end = 0
        self.shield_ready      = False

        self.spawn_food()
        self.maybe_spawn_poison()

    def _new_level(self):
        if self.level >= 3:
            count = 5 + (self.level - 3) * 3
            self.obstacles = generate_obstacles(self.snake, count)

    # ── Спаун объектов ───────────────────────────────────────────────────────
    def spawn_food(self):
        pos = random_free_cell(self.snake, self.obstacles,
                               powerup_pos=self.powerup_pos, poison_pos=self.poison_pos)
        if pos:
            self.food_pos    = pos
            self.food_weight, self.food_color = random.choice(FOODS)
            self.food_spawn  = pygame.time.get_ticks()

    def maybe_spawn_poison(self):
        if random.random() < 0.4:
            pos = random_free_cell(self.snake, self.obstacles,
                                   food_pos=self.food_pos, powerup_pos=self.powerup_pos)
            if pos:
                self.poison_pos   = pos
                self.poison_spawn = pygame.time.get_ticks()
        else:
            self.poison_pos = None

    def maybe_spawn_powerup(self):
        if self.powerup_pos is None and random.random() < 0.3:
            pos = random_free_cell(self.snake, self.obstacles,
                                   food_pos=self.food_pos, poison_pos=self.poison_pos)
            if pos:
                self.powerup_pos   = pos
                self.powerup_type  = random.choice(list(POWERUP_TYPES.keys()))
                self.powerup_spawn = pygame.time.get_ticks()

    # ── Скорость ─────────────────────────────────────────────────────────────
    @property
    def base_speed(self):
        speed = 8 + self.level * 2
        now = pygame.time.get_ticks()
        if self.active_effect == "speed" and now < self.active_effect_end:
            speed = int(speed * 1.7)
        elif self.active_effect == "slow" and now < self.active_effect_end:
            speed = max(4, int(speed * 0.5))
        return speed

    # ── Обработка ввода ──────────────────────────────────────────────────────
    def _handle_key(self, key, uni):
        if key == pygame.K_q:
            self._quit()

        if self.current_screen == self.SCREEN_USERNAME:
            if key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif key == pygame.K_RETURN:
                if self.username.strip():
                    self._login()
            elif len(self.username) < 20 and uni.isprintable() and uni != "":
                self.username += uni
            return

        if self.current_screen == self.SCREEN_SETTINGS:
            if self._typing_target == "color":
                if key == pygame.K_BACKSPACE:
                    self._tmp_color_input = self._tmp_color_input[:-1]
                elif key == pygame.K_RETURN:
                    self._apply_color_input()
                elif uni.isprintable():
                    self._tmp_color_input += uni
            return

        if self.current_screen == self.SCREEN_GAME:
            dirs = {
                pygame.K_UP: (0, -1),   pygame.K_w: (0, -1),
                pygame.K_DOWN: (0, 1),  pygame.K_s: (0, 1),
                pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
                pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
            }
            if key in dirs:
                nd = dirs[key]
                if nd != (-self.direction[0], -self.direction[1]):
                    self.next_dir = nd
            if key == pygame.K_ESCAPE:
                self.current_screen = self.SCREEN_MENU

    def _handle_click(self, pos):
        mx, my = pos
        s = self.current_screen

        if s == self.SCREEN_MENU:
            for _, rect, action in self._menu_buttons():
                if rect.collidepoint(mx, my):
                    action()

        elif s == self.SCREEN_GAMEOVER:
            for _, rect, action in self._gameover_buttons():
                if rect.collidepoint(mx, my):
                    action()

        elif s == self.SCREEN_LEADERBOARD:
            if self._back_button().collidepoint(mx, my):
                self.current_screen = self.SCREEN_MENU

        elif s == self.SCREEN_SETTINGS:
            for item in self._settings_items():
                if item["rect"].collidepoint(mx, my):
                    item["action"]()

    # ── Логин ────────────────────────────────────────────────────────────────
    def _login(self):
        name = self.username.strip()
        if not name:
            return
        self.player_id     = db_get_or_create_player(self.conn, name)
        self.personal_best = db_get_personal_best(self.conn, self.player_id)
        self._init_game_state()
        self.current_screen = self.SCREEN_GAME

    def _quit(self):
        pygame.quit()
        sys.exit()

    # ── Обновление игры ───────────────────────────────────────────────────────
    def update(self):
        if self.current_screen != self.SCREEN_GAME or self.game_over:
            return

        now = pygame.time.get_ticks()

        if self.active_effect and now >= self.active_effect_end:
            self.active_effect = None

        if now - self.food_spawn > FOOD_LIFETIME_MS:
            self.spawn_food()

        if self.poison_pos and now - self.poison_spawn > FOOD_LIFETIME_MS:
            self.poison_pos = None
            self.maybe_spawn_poison()

        if self.powerup_pos and now - self.powerup_spawn > POWERUP_LIFETIME_MS:
            self.powerup_pos = None

        if random.random() < 0.005:
            self.maybe_spawn_powerup()

        # Движение
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)

        hit_wall = not (0 <= new_head[0] <= COLS - 1 and 0 <= new_head[1] <= ROWS - 1)
        hit_self = new_head in self.snake[:-1]
        hit_obs  = new_head in set(self.obstacles)

        if hit_wall or hit_self or hit_obs:
            if self.shield_ready:
                self.shield_ready  = False
                self.active_effect = None
                return
            else:
                self._end_game()
                return

        self.snake.insert(0, new_head)
        grew = False

        if new_head == self.food_pos:
            self.score += self.food_weight
            grew = True
            old_level = self.level
            self.level = self.score // 5 + 1
            if self.level != old_level:
                self._new_level()
            self.spawn_food()
            self.maybe_spawn_poison()
            self.maybe_spawn_powerup()

        elif new_head == self.poison_pos:
            self.poison_pos = None
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            if len(self.snake) <= 1:
                self._end_game()
                return
            self.maybe_spawn_poison()

        elif new_head == self.powerup_pos:
            self._apply_powerup(self.powerup_type)
            self.powerup_pos = None

        if not grew:
            self.snake.pop()

    def _apply_powerup(self, ptype):
        now = pygame.time.get_ticks()
        self.active_effect     = ptype
        self.active_effect_end = now + POWERUP_EFFECT_MS
        if ptype == "shield":
            self.shield_ready = True

    def _end_game(self):
        self.game_over = True
        if self.score > self.personal_best:
            self.personal_best = self.score
        db_save_session(self.conn, self.player_id, self.score, self.level)
        self.current_screen = self.SCREEN_GAMEOVER

    # ════════════════════════════════════════════════════════════════════════
    # Отрисовка
    # ════════════════════════════════════════════════════════════════════════

    def draw(self):
        self.screen.fill(BLACK)
        {
            self.SCREEN_MENU:        self._draw_menu,
            self.SCREEN_USERNAME:    self._draw_username,
            self.SCREEN_GAME:        self._draw_game,
            self.SCREEN_GAMEOVER:    self._draw_gameover,
            self.SCREEN_LEADERBOARD: self._draw_leaderboard,
            self.SCREEN_SETTINGS:    self._draw_settings,
        }[self.current_screen]()
        pygame.display.flip()

    # ── Главное меню ─────────────────────────────────────────────────────────
    def _menu_buttons(self):
        bw, bh = 220, 48
        start_y = HEIGHT // 2 - 20
        entries = [
            ("Play",        self._go_username),
            ("Leaderboard", self._go_leaderboard),
            ("Settings",    self._go_settings),
            ("Quit",        self._quit),
        ]
        return [
            (lbl, pygame.Rect(WIDTH // 2 - bw // 2, start_y + i * 60, bw, bh), act)
            for i, (lbl, act) in enumerate(entries)
        ]

    def _draw_menu(self):
        title = self.font_big.render("SNAKE", True, ACCENT)
        sub   = self.font_small.render("Extended Edition", True, DIM)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        self.screen.blit(sub,   (WIDTH // 2 - sub.get_width() // 2, 128))

        mx, my = pygame.mouse.get_pos()
        for lbl, rect, _ in self._menu_buttons():
            draw_button(self.screen, self.font_med, lbl, rect, rect.collidepoint(mx, my))

        if not DB_AVAILABLE:
            note = self.font_tiny.render("psycopg2 not installed - leaderboard disabled", True, ORANGE)
            self.screen.blit(note, (WIDTH // 2 - note.get_width() // 2, HEIGHT - 30))

    def _go_username(self):
        if self.username.strip():
            self._login()
        else:
            self.current_screen = self.SCREEN_USERNAME

    def _go_leaderboard(self):
        self.leaderboard_data = db_get_leaderboard(self.conn)
        self.current_screen   = self.SCREEN_LEADERBOARD

    def _go_settings(self):
        self._tmp_settings    = dict(self.settings)
        self._tmp_color_input = ",".join(str(v) for v in self.settings["snake_color"])
        self._typing_target   = None
        self.current_screen   = self.SCREEN_SETTINGS

    # ── Ввод имени ───────────────────────────────────────────────────────────
    def _draw_username(self):
        title = self.font_big.render("Enter Username", True, ACCENT)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

        box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 24, 300, 48)
        text_input_box(self.screen, self.font_med, "Username:", box, self.username, True)

        hint = self.font_small.render("Press ENTER to continue", True, DIM)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 50))

    # ── Игровой экран ────────────────────────────────────────────────────────
    def _draw_game(self):
        # HUD-полоса
        pygame.draw.rect(self.screen, (10, 10, 16), (0, 0, WIDTH, HUD_H))
        # Фон поля
        pygame.draw.rect(self.screen, BLACK, (0, FIELD_Y, WIDTH, ROWS * CELL))

        # Сетка
        if self.settings["grid_overlay"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(self.screen, GRAY, (x, FIELD_Y), (x, HEIGHT))
            for y in range(FIELD_Y, HEIGHT, CELL):
                pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

        # Рамка поля
        pygame.draw.rect(self.screen, ACCENT, (0, FIELD_Y, WIDTH, ROWS * CELL), 2)

        # Препятствия
        for ox, oy in self.obstacles:
            r = pygame.Rect(ox * CELL, FIELD_Y + oy * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, WALL_COLOR, r.inflate(-2, -2), border_radius=3)

        # Еда
        if self.food_pos:
            fr = pygame.Rect(self.food_pos[0] * CELL, FIELD_Y + self.food_pos[1] * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, self.food_color, fr.inflate(-4, -4), border_radius=6)
            lbl = self.font_tiny.render(str(self.food_weight), True, WHITE)
            self.screen.blit(lbl, (fr.centerx - lbl.get_width() // 2,
                                   fr.centery - lbl.get_height() // 2))

        # Яд
        if self.poison_pos:
            pr = pygame.Rect(self.poison_pos[0] * CELL, FIELD_Y + self.poison_pos[1] * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, DARK_RED, pr.inflate(-4, -4), border_radius=6)
            lbl = self.font_tiny.render("X", True, WHITE)
            self.screen.blit(lbl, (pr.centerx - lbl.get_width() // 2,
                                   pr.centery - lbl.get_height() // 2))

        # Пауэрап
        if self.powerup_pos and self.powerup_type:
            info = POWERUP_TYPES[self.powerup_type]
            pur = pygame.Rect(self.powerup_pos[0] * CELL, FIELD_Y + self.powerup_pos[1] * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, info["color"], pur.inflate(-4, -4), border_radius=6)
            lbl = self.font_tiny.render(info["symbol"], True, BLACK)
            self.screen.blit(lbl, (pur.centerx - lbl.get_width() // 2,
                                   pur.centery - lbl.get_height() // 2))

        # Змейка
        sc       = tuple(self.settings["snake_color"])
        body_col = tuple(max(0, c - 30) for c in sc)
        for idx, part in enumerate(self.snake):
            r = pygame.Rect(part[0] * CELL, FIELD_Y + part[1] * CELL, CELL, CELL)
            pygame.draw.rect(self.screen, sc if idx == 0 else body_col,
                             r.inflate(-2, -2), border_radius=5)

        # HUD-текст
        now = pygame.time.get_ticks()
        food_left = max(0, FOOD_LIFETIME_MS - (now - self.food_spawn)) // 1000 + 1
        hud = self.font_med.render(
            f"Score: {self.score}   Level: {self.level}   "
            f"Food: {food_left}s   Best: {self.personal_best}",
            True, WHITE
        )
        self.screen.blit(hud, (10, HUD_H // 2 - hud.get_height() // 2))

        # Бейдж активного эффекта
        if self.active_effect:
            remain = max(0, self.active_effect_end - now) // 1000 + 1
            info   = POWERUP_TYPES.get(self.active_effect, {})
            badge  = self.font_small.render(
                f"{info.get('symbol','?')} {self.active_effect.upper()} {remain}s",
                True, info.get("color", WHITE)
            )
            self.screen.blit(badge, (WIDTH - badge.get_width() - 10,
                                     HUD_H // 2 - badge.get_height() // 2))

    # ── Game Over ────────────────────────────────────────────────────────────
    def _gameover_buttons(self):
        bw, bh = 180, 44
        cy = HEIGHT // 2 + 70
        return [
            ("Retry",     pygame.Rect(WIDTH // 2 - 200, cy, bw, bh), self._retry),
            ("Main Menu", pygame.Rect(WIDTH // 2 + 20,  cy, bw, bh), self._to_menu),
        ]

    def _retry(self):
        self._init_game_state()
        self.personal_best  = db_get_personal_best(self.conn, self.player_id)
        self.current_screen = self.SCREEN_GAME

    def _to_menu(self):
        self.current_screen = self.SCREEN_MENU

    def _draw_gameover(self):
        panel = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 120, 500, 260)
        draw_panel(self.screen, panel, BG_PANEL, radius=16)

        title = self.font_big.render("GAME OVER", True, RED)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 105))

        for i, line in enumerate([
            f"Score: {self.score}",
            f"Level reached: {self.level}",
            f"Personal best: {self.personal_best}",
        ]):
            surf = self.font_med.render(line, True, WHITE)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2,
                                    HEIGHT // 2 - 55 + i * 34))

        mx, my = pygame.mouse.get_pos()
        for lbl, rect, _ in self._gameover_buttons():
            draw_button(self.screen, self.font_med, lbl, rect, rect.collidepoint(mx, my))

    # ── Лидерборд ────────────────────────────────────────────────────────────
    def _back_button(self):
        return pygame.Rect(WIDTH // 2 - 80, HEIGHT - 56, 160, 40)

    def _draw_leaderboard(self):
        title = self.font_big.render("Leaderboard", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 24))

        cols_x  = [40, 90, 280, 380, 480]
        headers = ["#", "Player", "Score", "Level", "Date"]
        for cx, h in zip(cols_x, headers):
            self.screen.blit(self.font_med.render(h, True, ACCENT), (cx, 80))
        pygame.draw.line(self.screen, ACCENT, (30, 108), (WIDTH - 30, 108), 1)

        if not DB_AVAILABLE or not self.leaderboard_data:
            msg = "No data available" if not DB_AVAILABLE else "No scores yet!"
            surf = self.font_med.render(msg, True, DIM)
            self.screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT // 2))
        else:
            for rank, (uname, score, lvl, played_at) in enumerate(self.leaderboard_data, 1):
                row_color = YELLOW if rank == 1 else (WHITE if rank <= 3 else DIM)
                date_str  = (played_at.strftime("%Y-%m-%d")
                             if isinstance(played_at, datetime) else str(played_at)[:10])
                for cx, val in zip(cols_x, [str(rank), uname[:18], str(score), str(lvl), date_str]):
                    self.screen.blit(
                        self.font_small.render(val, True, row_color),
                        (cx, 118 + rank * 30)
                    )

        mx, my = pygame.mouse.get_pos()
        back = self._back_button()
        draw_button(self.screen, self.font_med, "<- Back", back, back.collidepoint(mx, my))

    # ── Настройки ────────────────────────────────────────────────────────────
    def _settings_items(self):
        bw, bh = 220, 44
        cx = WIDTH // 2
        return [
            {
                "type": "toggle", "label": f"Grid: {'ON' if self._tmp_settings.get('grid_overlay') else 'OFF'}",
                "rect": pygame.Rect(cx - bw // 2, 160, bw, bh),
                "action": lambda: self._tmp_settings.update(
                    {"grid_overlay": not self._tmp_settings["grid_overlay"]}),
            },
            {
                "type": "toggle", "label": f"Sound: {'ON' if self._tmp_settings.get('sound') else 'OFF'}",
                "rect": pygame.Rect(cx - bw // 2, 220, bw, bh),
                "action": lambda: self._tmp_settings.update(
                    {"sound": not self._tmp_settings["sound"]}),
            },
            {
                "type": "button", "label": "Save & Back",
                "rect": pygame.Rect(cx - bw // 2, HEIGHT - 80, bw, bh),
                "action": self._save_settings,
            },
        ]

    def _apply_color_input(self):
        try:
            parts = [int(p.strip()) for p in self._tmp_color_input.split(",")]
            if len(parts) == 3 and all(0 <= v <= 255 for v in parts):
                self._tmp_settings["snake_color"] = parts
        except ValueError:
            pass
        self._typing_target = None

    def _save_settings(self):
        self._apply_color_input()
        self.settings = dict(self._tmp_settings)
        save_settings(self.settings)
        self.current_screen = self.SCREEN_MENU

    def _draw_settings(self):
        title = self.font_big.render("Settings", True, ACCENT)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

        mx, my = pygame.mouse.get_pos()
        for item in self._settings_items():
            draw_button(self.screen, self.font_med, item["label"], item["rect"],
                        item["rect"].collidepoint(mx, my))

        color_label = self.font_med.render("Snake Color (R,G,B):", True, WHITE)
        self.screen.blit(color_label, (WIDTH // 2 - 130, 290))

        color_box = pygame.Rect(WIDTH // 2 - 130, 330, 260, 44)
        active = (self._typing_target == "color")
        text_input_box(self.screen, self.font_med, "", color_box, self._tmp_color_input, active)

        if pygame.mouse.get_pressed()[0] and color_box.collidepoint(mx, my):
            self._typing_target = "color"

        try:
            swatch_col = tuple(int(p.strip()) for p in self._tmp_color_input.split(","))
            if len(swatch_col) == 3:
                pygame.draw.rect(self.screen, swatch_col,
                                 pygame.Rect(WIDTH // 2 + 140, 330, 44, 44), border_radius=6)
        except Exception:
            pass

        hint = self.font_tiny.render("Click the box, type R,G,B and press ENTER", True, DIM)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 390))

    # ── Главный цикл ─────────────────────────────────────────────────────────
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN:
                    self._handle_key(event.key, event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)

            self.update()
            self.draw()
            fps = self.base_speed if self.current_screen == self.SCREEN_GAME else 60
            self.clock.tick(fps)