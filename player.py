import pygame

from constants import *
from animate_sprite import AnimateSprite

class Player(AnimateSprite):

    def __init__(self):
        # Initialiser avec le sprite sheet d'animation
        super().__init__('assets/images/perso_move.png', PLAYER_WIDTH, PLAYER_HEIGHT, animation_speed=0.15)
        self.rect.x = 100
        self.rect.y = GAME_FLOOR
        self.speed = 3

    def move_right(self):
        # verifier si on sort pas de l'écran a droite
        if self.rect.x + self.speed + PLAYER_WIDTH < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.update_animation('right')

    def move_left(self):
        if self.rect.x - self.speed >=0:
            self.rect.x -= self.speed
            self.update_animation('left')

    def move_up(self):
        if self.rect.y - self.speed >=0:
            self.rect.y -= self.speed
            self.update_animation('up')

    def move_down(self):
        if self.rect.y + self.speed < GAME_FLOOR:
            self.rect.y += self.speed
            self.update_animation('down')

    def stop_moving(self):
        """Arrête l'animation quand le joueur ne bouge plus"""
        self.stop_animation()