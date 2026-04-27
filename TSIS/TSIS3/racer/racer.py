# racer.py — основная игровая логика TSIS 3

import os
import pygame
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GREEN = (50, 200, 50)
BLUE = (50, 120, 220)
CYAN = (0, 220, 220)

CAR_COLORS = {
    "default": WHITE,
    "red": RED,
    "blue": BLUE,
    "green": GREEN,
}

WIDTH = 500
HEIGHT = 700
LANE_X = [125, 250, 375]
ROAD_LEFT = 50
ROAD_RIGHT = 450

DIFFICULTY_SETTINGS = {
    "easy": {"enemy_base": 3, "obstacle_freq": 60, "traffic_freq": 80},
    "normal": {"enemy_base": 5, "obstacle_freq": 45, "traffic_freq": 60},
    "hard": {"enemy_base": 8, "obstacle_freq": 30, "traffic_freq": 40},
}


class RacerGame:
    def __init__(self, screen, username, settings, racer_img, coin_img, street_img):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Arial", 22)
        self.font_big = pygame.font.SysFont("Arial", 32, bold=True)
        self.clock = pygame.time.Clock()

        self.coin_img = coin_img

        road_w = ROAD_RIGHT - ROAD_LEFT
        self.street_img = pygame.transform.scale(street_img, (road_w, HEIGHT))

        self.music_path = os.path.join(
            os.path.dirname(__file__),
            "sounds",
            "background.mp3"
        )

        diff = settings.get("difficulty", "normal")
        self.diff_cfg = DIFFICULTY_SETTINGS[diff]

        car_color = CAR_COLORS.get(settings.get("car_color", "default"), WHITE)

        if car_color == WHITE:
            self._player_surf = racer_img
        else:
            colored = racer_img.copy()
            colored.fill(car_color, special_flags=pygame.BLEND_MULT)
            self._player_surf = colored

        self.reset()

    def start_music(self):
        if os.path.exists(self.music_path):
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def reset(self):
        self.player = pygame.Rect(225, 580, 50, 70)

        self.score = 0
        self.coins = []
        self.coin_count = 0
        self.distance = 0
        self.frame = 0

        self.enemies = []
        self.enemy_speed = self.diff_cfg["enemy_base"]

        self.obstacles = []

        self.powerups = []
        self.active_powerup = None
        self.powerup_timer = 0

        self.nitro_active = False
        self.nitro_end = 0

        self.base_speed = 5
        self.player_speed = self.base_speed

        self.shield_active = False
        self.street_y = 0

    def spawn_enemy(self):
        lane = random.choice(LANE_X)
        rect = pygame.Rect(lane - 25, -80, 50, 70)

        if abs(rect.x - self.player.x) > 60 or rect.y > self.player.y - 100:
            self.enemies.append(rect)

    def spawn_obstacle(self):
        lane = random.choice(LANE_X)
        kind = random.choice(["oil", "bump", "barrier"])
        rect = pygame.Rect(lane - 20, -40, 40, 20)

        self.obstacles.append({
            "rect": rect,
            "kind": kind
        })

    def spawn_powerup(self):
        if len(self.powerups) >= 1:
            return

        lane = random.choice(LANE_X)
        kind = random.choice(["nitro", "shield", "repair"])
        rect = pygame.Rect(lane - 15, -30, 30, 30)

        self.powerups.append({
            "rect": rect,
            "kind": kind,
            "spawned": time.time()
        })

    def spawn_coin(self):
        x = random.randint(ROAD_LEFT, ROAD_RIGHT - 30)
        value = random.choice([1, 2, 3])
        rect = pygame.Rect(x, -30, 30, 30)

        self.coins.append({
            "rect": rect,
            "value": value
        })

    def update(self):
        self.frame += 1
        self.distance += 1

        if self.nitro_active and time.time() > self.nitro_end:
            self.nitro_active = False
            self.player_speed = self.base_speed

        self.enemy_speed = self.diff_cfg["enemy_base"] + self.distance // 500

        if self.frame % 90 == 0:
            self.spawn_enemy()

        if self.frame % self.diff_cfg["obstacle_freq"] == 0:
            self.spawn_obstacle()

        if self.frame % 150 == 0:
            self.spawn_coin()

        if self.frame % 200 == 0:
            self.spawn_powerup()

        self.street_y = (self.street_y + self.player_speed) % HEIGHT

        for e in self.enemies[:]:
            e.y += self.enemy_speed

            if e.y > HEIGHT:
                self.enemies.remove(e)

        for o in self.obstacles[:]:
            o["rect"].y += self.player_speed

            if o["rect"].y > HEIGHT:
                self.obstacles.remove(o)

        for c in self.coins[:]:
            c["rect"].y += self.player_speed

            if c["rect"].y > HEIGHT:
                self.coins.remove(c)

        for p in self.powerups[:]:
            p["rect"].y += self.player_speed

            if p["rect"].y > HEIGHT or time.time() - p["spawned"] > 8:
                self.powerups.remove(p)

    def check_collisions(self):
        for c in self.coins[:]:
            if self.player.colliderect(c["rect"]):
                self.coins.remove(c)
                self.coin_count += c["value"]
                self.score += c["value"] * 10

        for p in self.powerups[:]:
            if self.player.colliderect(p["rect"]):
                self.powerups.remove(p)
                self.activate_powerup(p["kind"])

        for o in self.obstacles[:]:
            if self.player.colliderect(o["rect"]):
                if self.shield_active:
                    self.shield_active = False
                    self.obstacles.remove(o)

                elif o["kind"] == "oil":
                    self.player_speed = max(2, self.player_speed - 2)
                    self.obstacles.remove(o)

                elif o["kind"] == "bump":
                    self.obstacles.remove(o)
                    self.score = max(0, self.score - 20)

                elif o["kind"] == "barrier":
                    return True

        for e in self.enemies[:]:
            if self.player.colliderect(e):
                if self.shield_active:
                    self.shield_active = False
                    self.enemies.remove(e)
                    return False

                return True

        return False

    def activate_powerup(self, kind):
        self.active_powerup = kind
        self.powerup_timer = time.time()

        if kind == "nitro":
            self.nitro_active = True
            self.nitro_end = time.time() + 4
            self.player_speed = self.base_speed * 2

        elif kind == "shield":
            self.shield_active = True

        elif kind == "repair":
            if self.obstacles:
                self.obstacles.pop(0)

            self.score += 30

    def draw(self):
        self.screen.fill((40, 40, 40))

        self.screen.blit(self.street_img, (ROAD_LEFT, self.street_y - HEIGHT))
        self.screen.blit(self.street_img, (ROAD_LEFT, self.street_y))

        for c in self.coins:
            self.screen.blit(self.coin_img, (c["rect"].x, c["rect"].y))

        for o in self.obstacles:
            if o["kind"] == "oil":
                pygame.draw.ellipse(self.screen, (0, 0, 80), o["rect"])
                pygame.draw.ellipse(self.screen, (0, 0, 150), o["rect"].inflate(-8, -4))

            elif o["kind"] == "bump":
                pygame.draw.rect(self.screen, GRAY, o["rect"], border_radius=4)
                pygame.draw.rect(self.screen, WHITE, o["rect"], 2, border_radius=4)

            elif o["kind"] == "barrier":
                pygame.draw.rect(self.screen, RED, o["rect"], border_radius=3)
                pygame.draw.rect(self.screen, YELLOW, o["rect"], 2, border_radius=3)

        for p in self.powerups:
            r = p["rect"]

            if p["kind"] == "nitro":
                pygame.draw.rect(self.screen, ORANGE, r, border_radius=6)
                txt = self.font.render("N", True, WHITE)

            elif p["kind"] == "shield":
                pygame.draw.rect(self.screen, CYAN, r, border_radius=6)
                txt = self.font.render("S", True, BLACK)

            else:
                pygame.draw.rect(self.screen, GREEN, r, border_radius=6)
                txt = self.font.render("R", True, WHITE)

            self.screen.blit(txt, (r.x + 8, r.y + 6))

        for e in self.enemies:
            pygame.draw.rect(self.screen, RED, e, border_radius=6)
            pygame.draw.rect(self.screen, (180, 0, 0), e, 2, border_radius=6)

        self.screen.blit(self._player_surf, (self.player.x, self.player.y))

        if self.shield_active:
            pygame.draw.circle(self.screen, CYAN, self.player.center, 45, 3)

        self.draw_hud()

    def draw_hud(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, 50))

        score_txt = self.font.render(f"Score: {self.score}", True, YELLOW)
        dist_txt = self.font.render(f"Dist: {self.distance}m", True, WHITE)
        coin_txt = self.font.render(f"Coins: {self.coin_count}", True, YELLOW)

        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(dist_txt, (150, 10))
        self.screen.blit(coin_txt, (280, 10))

        if self.active_powerup:
            elapsed = time.time() - self.powerup_timer

            if self.active_powerup == "nitro" and elapsed < 4:
                remaining = round(4 - elapsed, 1)
                txt = self.font.render(f"NITRO {remaining}s", True, ORANGE)
                self.screen.blit(txt, (10, HEIGHT - 35))

            elif self.active_powerup == "shield" and self.shield_active:
                txt = self.font.render("SHIELD ACTIVE", True, CYAN)
                self.screen.blit(txt, (10, HEIGHT - 35))

            elif self.active_powerup == "repair" and elapsed < 2:
                txt = self.font.render("REPAIR!", True, GREEN)
                self.screen.blit(txt, (10, HEIGHT - 35))

            else:
                self.active_powerup = None

    def run(self):
        self.start_music()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    return self.score, self.distance, self.coin_count

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop_music()
                        return self.score, self.distance, self.coin_count

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.player.left > ROAD_LEFT:
                self.player.x -= self.player_speed

            if keys[pygame.K_RIGHT] and self.player.right < ROAD_RIGHT:
                self.player.x += self.player_speed

            self.update()
            game_over = self.check_collisions()

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

            if game_over:
                self.stop_music()
                return self.score, self.distance, self.coin_count

        self.stop_music()
        return self.score, self.distance, self.coin_count