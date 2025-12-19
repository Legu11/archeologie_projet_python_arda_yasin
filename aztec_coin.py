import pygame
from constants import *

# Charger et préparer l'image de la pièce une seule fois
_coin_image_cache = None

def _get_coin_image():
    """Cache la charge de l'image de la pièce"""
    global _coin_image_cache
    if _coin_image_cache is None:
        _coin_image_cache = pygame.image.load('assets/images/aztec_coin.png')
        _coin_image_cache = pygame.transform.scale(_coin_image_cache, (70, 70))
        _coin_image_cache = _coin_image_cache.convert_alpha()
    return _coin_image_cache

class AztecCoin(pygame.sprite.Sprite):
    """Représente une pièce aztèque qui tombe après avoir vaincu un monstre"""
    
    def __init__(self, x, y, gravity=3):
        super().__init__()
        # Utiliser l'image en cache
        self.image = _get_coin_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = gravity

    def fall(self):
        """La pièce tombe avec la gravité"""
        if self.rect.y < GAME_FLOOR - 40:
            self.rect.y += self.gravity
        else:
            self.rect.y = GAME_FLOOR - 40
