# main.py — точка входа в игру TSIS 3

import pygame
from persistence import load_settings, add_score
from ui import main_menu, username_screen, settings_screen, leaderboard_screen, game_over_screen
from racer import RacerGame, WIDTH, HEIGHT


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer — TSIS 3")

# Загружаем картинки
coin_img  = pygame.image.load("coin.png")
coin_img  = pygame.transform.scale(coin_img, (30, 30))

racer_img = pygame.image.load("space_racer.png")
racer_img = pygame.transform.scale(racer_img, (50, 70))

street_img = pygame.image.load("AnimatedStreet.png")



# Загружаем настройки
settings = load_settings()
username = "Player"

# ─────────────────────────────────────────────
# ГЛАВНЫЙ ЦИКЛ ПРИЛОЖЕНИЯ
# ─────────────────────────────────────────────

while True:
    action = main_menu(screen, WIDTH, HEIGHT)

    if action == "quit":
        break

    elif action == "leaderboard":
        leaderboard_screen(screen, WIDTH, HEIGHT)

    elif action == "settings":
        settings = settings_screen(screen, WIDTH, HEIGHT, settings)

    elif action == "play":
        # Ввод имени
        username = username_screen(screen, WIDTH, HEIGHT)

        # Игровой цикл с возможностью Retry
        while True:
            game = RacerGame(screen, username, settings, racer_img, coin_img, street_img)
            score, distance, coins = game.run()

            # Сохраняем результат
            add_score(username, score, distance)

            # Game Over экран
            result = game_over_screen(screen, WIDTH, HEIGHT, score, distance, coins)

            if result == "retry":
                continue
            else:
                break

pygame.quit()