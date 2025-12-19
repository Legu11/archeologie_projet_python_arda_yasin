import pygame

from constants import *
from projectile import Projectile
from animate_sprite import AnimateSprite

class Player(AnimateSprite):

    def __init__(self):
        # Initialiser avec le sprite sheet d'animation
        super().__init__('assets/images/perso_move.png', PLAYER_WIDTH, PLAYER_HEIGHT, animation_speed=0.15)
        self.rect.x = 100
        self.rect.y = GAME_FLOOR
        self.speed = 3
        self.direction = 'right'  # Direction actuelle du joueur

        # Groupe pour les projectiles
        self.all_projectiles = pygame.sprite.Group()
        
        # Système de cooldown pour les tirs
        self.last_shot_time = 0  
        self.shot_cooldown = 70  

    def launch_projectile(self):
        """Tire une balle dans la direction du joueur avec cooldown"""
        current_time = pygame.time.get_ticks()
        
        # Vérifier si le cooldown est écoulé
        if current_time - self.last_shot_time >= self.shot_cooldown:
            new_projectile = Projectile(self.rect.x, self.rect.y, self.direction)
            self.all_projectiles.add(new_projectile)
            self.last_shot_time = current_time

    def move_right(self):
        # verifier si on sort pas de l'écran a droite
        if self.rect.x + self.speed + PLAYER_WIDTH < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.update_animation('right')
        self.direction = 'right'

    def move_left(self):
        if self.rect.x - self.speed >=0:
            self.rect.x -= self.speed
            self.update_animation('left')
        self.direction = 'left'

    def move_up(self):
        if self.rect.y - self.speed >=0:
            self.rect.y -= self.speed
            self.update_animation('up')
        self.direction = 'up'

    def move_down(self):
        if self.rect.y + self.speed < GAME_FLOOR:
            self.rect.y += self.speed
            self.update_animation('down')
        self.direction = 'down'

    def stop_moving(self):
        """Arrête l'animation quand le joueur ne bouge plus"""
        self.stop_animation()