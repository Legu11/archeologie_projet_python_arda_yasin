import pygame
from constants import *

class AztecCoin(pygame.sprite.Sprite):
    """Représente une pièce aztèque qui tombe après avoir vaincu un monstre"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/aztec_coin.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 3

    def fall(self):
        """La pièce tombe avec la gravité"""
        if self.rect.y < GAME_FLOOR - 40:
            self.rect.y += self.gravity
        else:
            self.rect.y = GAME_FLOOR - 40
