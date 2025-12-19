import pygame
from constants import *

class Projectile(pygame.sprite.Sprite):
    """Représente une balle tirée par le joueur"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/bullet_attack.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x + 50
        self.rect.y = y + 25
        self.speed = 7

    def move(self):
        self.rect.x += self.speed
        # Supprimer le projectile s'il sort de l'écran
        if self.rect.x > SCREEN_WIDTH:
            self.kill()
