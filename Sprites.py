import pygame
import random
from Settings import *
from os import path

class Player(pygame.sprite.Sprite):
    def __init__(self,bird_fly):
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_fly
        self.index = 0
        self.image = self.images[self.index]
        self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 3
        self.rect.y = HEIGHT / 2
        self.gravity = 1
        self.y = 0
        self.heart = 3

    def jump(self):
        self.y = -15


    def update(self):
        self.index += 1
        if self.index > 3:
              self.index = 0

        self.image = self.images[self.index]
        self.image.set_colorkey(YELLOW)

        self.y = self.y + self.gravity
        self.rect.y += self.y
        if self.rect.bottom >= HEIGHT:
            self.jump()
        if self.rect.top <= 0:
            self.rect.top = 0

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, wall_img, game):
        self.groups = game.all_sprites, game.walls
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = wall_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(150,400)
        self.rect.x = x + WALLDISTANCE
        self.dx = OBJECTSPEED

    def update(self):
        self.rect.x += self.dx

        if self.rect.right < 0:
            self.kill()

class Wallup(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_img, game):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = wall_img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x + WALLDISTANCE
        self.rect.top = random.randrange(y + 200, y + 300)
        self.dx = OBJECTSPEED


    def update(self):
        self.rect.x += self.dx

        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self,clouds):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(clouds)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(-50,HEIGHT-500)

    def update(self):
        self.rect.x += BACKGROUNDSPEED
        if self.rect.right < 0:
            self.kill()

class Gcoin(pygame.sprite.Sprite):
    reward = 100
    def __init__(self, gold, y, game):
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = gold
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + WALLDISTANCE
        self.rect.top = random.randrange(y + 50, y + 150)
        self.dx = OBJECTSPEED

    def update(self):
        self.rect.x += self.dx
        if self.rect.right < 0:
            self.kill()

class Scoin(pygame.sprite.Sprite):
    reward = 25
    def __init__(self, silver, y, game):
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = silver
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + WALLDISTANCE
        self.rect.top = random.randrange(y + 50, y + 150)
        self.dx = OBJECTSPEED

    def update(self):
        self.rect.x += self.dx
        if self.rect.right < 0:
            self.kill()

class Heartup(pygame.sprite.Sprite):
    def __init__(self, y, heart, game):
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = heart
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + WALLDISTANCE
        self.rect.top = y + 150
        self.dx = OBJECTSPEED

    def update(self):
        self.rect.x += self.dx
        if self.rect.right < 0:
            self.kill()
