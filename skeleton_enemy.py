import pygame
import random
from constants import *

# Charger et préparer l'image du squelette une seule fois (pas à chaque création)
_skeleton_image_cache = None

def _get_skeleton_image():
    """Cache la charge de l'image du squelette"""
    global _skeleton_image_cache
    if _skeleton_image_cache is None:
        try:
            _skeleton_image_cache = pygame.image.load('assets/images/skeleton_ennemy.png')
            _skeleton_image_cache = pygame.transform.scale(_skeleton_image_cache, (250, 250))
            _skeleton_image_cache = _skeleton_image_cache.convert_alpha()
        except Exception as e:
            print(f"ERREUR: Impossible de charger skeleton_ennemy.png: {e}")
            print("Utilisation d'une image par défaut (red square)")
            # Créer une image de remplacement (un carré rouge)
            _skeleton_image_cache = pygame.Surface((250, 250))
            _skeleton_image_cache.fill((255, 0, 0))
    return _skeleton_image_cache

class SkeletonEnemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # Utiliser l'image en cache au lieu de la charger/redimensionner à chaque fois
        self.image = _get_skeleton_image()
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 50 + random.randint(10, 1000)
        self.rect.y = GAME_FLOOR - random.randint(10, 300)
        self.speed = 2.0  # Squelettes un peu plus rapides
        
        self.max_health = 2  # Squelettes moins solides
        self.health = self.max_health

    def move(self):
        """Déplacement aléatoire du squelette"""
        self.rect.x -= self.speed
        if self.rect.x < -300:
            self.rect.x = SCREEN_WIDTH + 100
            self.rect.y = GAME_FLOOR - random.randint(10, 300)

    def follow_player(self, player):
        """Le squelette suit le joueur"""
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

    def take_damage(self, damage):
        """Le squelette reçoit des dégâts et retourne True s'il est mort"""
        self.health -= damage
        return self.health <= 0
