import pygame
from constants import *

# Charger et préparer l'image de la balle une seule fois
_projectile_image_cache = None

def _get_projectile_image():
    """Cache la charge de l'image du projectile"""
    global _projectile_image_cache
    if _projectile_image_cache is None:
        _projectile_image_cache = pygame.image.load('assets/images/bullet_attack.png')
        _projectile_image_cache = pygame.transform.scale(_projectile_image_cache, (50, 50))
        _projectile_image_cache = _projectile_image_cache.convert_alpha()
    return _projectile_image_cache

class Projectile(pygame.sprite.Sprite):
    """Représente une balle tirée par le joueur"""
    
    # Dictionnaire de direction vers vélocité (plus efficace qu'un if/elif)
    DIRECTION_VELOCITY = {
        'right': (7, 0),
        'left': (-7, 0),
        'up': (0, -7),
        'down': (0, 7)
    }
    
    def __init__(self, x, y, direction='right'):
        super().__init__()
        # Utiliser l'image en cache
        self.image = _get_projectile_image()
        self.rect = self.image.get_rect()
        self.rect.x = x + 50
        self.rect.y = y + 25
        
        # Récupérer la vélocité selon la direction
        self.vx, self.vy = self.DIRECTION_VELOCITY.get(direction, (7, 0))

    def move(self):
        """Déplace le projectile et le supprime s'il sort de l'écran"""
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Supprimer le projectile s'il sort de l'écran
        if (self.rect.x > SCREEN_WIDTH or 
            self.rect.x < -30 or 
            self.rect.y < -30 or 
            self.rect.y > SCREEN_HEIGHT + 30):
            self.kill()
