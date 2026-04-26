import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COINS = 0

LEVEL_UP_COINS = 10
last_level = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)



class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.values = [1, 2, 5]
        self.set_random_coin()
        self.rect = self.image.get_rect()
        self.spawn()

    def set_random_coin(self):
        self.value = random.choice(self.values)

        if self.value == 1:
            img = pygame.image.load("coin.png")
        elif self.value == 2:
            img = pygame.image.load("coin.png")
        else:
            img = pygame.image.load("coin.png")

        self.image = pygame.transform.scale(img.convert_alpha(), (40, 40))

    def spawn(self):
        self.set_random_coin()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# ---------------- OBJECTS ----------------
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)


# ---------------- GAME LOOP ----------------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # background
    DISPLAYSURF.blit(background, (0, 0))

    # UI
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coin_text, (250, 10))

    # update entities
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    collected = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected:
        COINS += coin.value
        coin.spawn()


    current_level = COINS // LEVEL_UP_COINS
    if current_level > last_level:
        SPEED += 1
        last_level = current_level

    pygame.display.update()
    FramePerSec.tick(FPS)