import pygame
import random
from constants import *

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/images/aztec_monster.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 50 + random.randint(10, 1000)
        self.rect.y = GAME_FLOOR - random.randint(10,300)
        self.speed = 1.5

    def respawn(self):
        self.rect.x = SCREEN_WIDTH - 50 + random.randint(10, 1000)
        self.rect.y = GAME_FLOOR - random.randint(10,300)

    def move(self):
        self.rect.x -= 1
        if self.rect.x <= 0:
            self.respawn()
    
    def follow_player(self, player):
        """Le monstre suit le joueur en se déplaçant horizontalement et verticalement"""
        # Calculer la direction vers le joueur
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        # Calculer la distance
        distance = (dx**2 + dy**2)**0.5
        
        # Normaliser et appliquer la vitesse pour mouvement lisse
        if distance > 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            
            self.rect.x += dx
            self.rect.y += dy
