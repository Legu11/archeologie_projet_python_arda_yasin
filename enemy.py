import pygame
import random
from constants import *

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/images/monster_omori.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 50 + random.randint(10, 1000)
        self.rect.y = GAME_FLOOR - random.randint(10,300)

    def respawn(self):
        self.rect.x = SCREEN_WIDTH - 50 + random.randint(10, 1000)
        self.rect.y = GAME_FLOOR - random.randint(10,300)

    def move(self):
        self.rect.x -= 1
        if self.rect.x <= 0:
            self.respawn()
