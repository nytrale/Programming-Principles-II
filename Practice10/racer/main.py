import pygame, sys
import random, time
from pygame.locals import *

pygame.init()

# Настройки
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

def load_image(name, fallback_color, size):
    try:
        img = pygame.image.load(name)
        return pygame.transform.scale(img, size)
    except Exception as e:
        print(f"Предупреждение: Не удалось загрузить {name}. Ошибка: {e}")
    
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

player_img = load_image("Player.png.png", (0, 0, 255), (40, 80))
player_img = pygame.transform.rotate(player_img, 180)
enemy_img = load_image("Enemy.png.png", (255, 0, 0), (40, 80))

coin_img = load_image("Coin.png.png", (255, 255, 0), (30, 30))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

font_small = pygame.font.SysFont(None, 25)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill((255, 255, 255))
    
    score_txt = font_small.render(f"Enemies: {SCORE}", True, (0,0,0))
    coin_txt = font_small.render(f"Coins: {COIN_SCORE}", True, (0,0,0))
    DISPLAYSURF.blit(score_txt, (10, 10))
    DISPLAYSURF.blit(coin_txt, (SCREEN_WIDTH - 100, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += 1
        C1.spawn()

    if pygame.sprite.spritecollideany(P1, enemies):
        print("GAME OVER")
        time.sleep(1)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)