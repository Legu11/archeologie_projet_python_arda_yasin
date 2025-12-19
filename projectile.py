import pygame
from constants import *

class Projectile(pygame.sprite.Sprite):
    """Représente une balle tirée par le joueur"""
    
    def __init__(self, x, y, direction='right'):
        super().__init__()
        self.image = pygame.image.load('assets/images/bullet_attack.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x + 50
        self.rect.y = y + 25
        self.speed = 7
        self.direction = direction
        
        # Définir la vélocité selon la direction
        self.vx = 0
        self.vy = 0
        
        if direction == 'right':
            self.vx = self.speed
        elif direction == 'left':
            self.vx = -self.speed
        elif direction == 'up':
            self.vy = -self.speed
        elif direction == 'down':
            self.vy = self.speed

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Supprimer le projectile s'il sort de l'écran
        if (self.rect.x > SCREEN_WIDTH or 
            self.rect.x < -30 or 
            self.rect.y < -30 or 
            self.rect.y > SCREEN_HEIGHT + 30):
            self.kill()
