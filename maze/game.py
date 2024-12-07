from typing import Any
import pygame

pygame.init()

window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Лабіринт")

background = pygame.transform.scale(pygame.image.load("background.jpg"), (700, 500))

game_over = False

clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

kick = pygame.mixer.Sound("kick.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_X=0, player_y=0, player_speed=5):
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_X
        self.rect.y = player_y
        self.speed = player_speed
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <=470:
            self.direction = "left"
        if self.rect.x >= 670:
            self.direction = "right"

        if self.direction == "left":
            self.rect.x -= self.speed
        if self.direction == "right":
            self.rect.x += self.speed

class Wall(pygame.sprite.Sprite):
    def __init__(self, r, g, b, x, y, width, height):
        self.r = r
        self.g = g
        self.b = b
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player("hero.png", 0, 0, 10)
enemy = Enemy("cyborg.png", 100, 100, 15)
treasure = GameSprite("treasure.png", 200, 200, 5)

#128, 75, 120
w1 = Wall(128, 75, 120, 100, 20, 400, 20)

while not game_over:
    window.blit(background, (0, 0))

    w1.draw()
    player.draw()
    enemy.draw()
    treasure.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    player.update()
    enemy.update()
    treasure.update()

    if pygame.sprite.collide_rect(enemy) or player.rect.collide_rect(w1):
        kick.play()
        game_over = True


    pygame.display.update()
    clock.tick(60)
pygame.quit()