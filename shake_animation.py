import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class ShakeAnimation:
    """Gère les effets de shake et d'overlay rouge lors des dégâts"""
    
    def __init__(self, duration=300, intensity=5):
        """
        Initialise l'effet de shake
        :param duration: Durée de l'effet en millisecondes
        :param intensity: Intensité du tremblement en pixels
        """
        self.duration = duration
        self.intensity = intensity
        self.start_time = 0
        self.active = False
    
    def trigger(self):
        """Déclenche l'effet de shake"""
        self.start_time = pygame.time.get_ticks()
        self.active = True
    
    def is_active(self):
        """Retourne True si l'effet est toujours actif"""
        if self.active:
            elapsed = pygame.time.get_ticks() - self.start_time
            if elapsed >= self.duration:
                self.active = False
        return self.active
    
    def get_shake_offset(self):
        """Retourne un offset aléatoire pour le shake de l'écran"""
        if self.is_active():
            shake_x = random.randint(-self.intensity, self.intensity)
            shake_y = random.randint(-self.intensity, self.intensity)
            return shake_x, shake_y
        return 0, 0
    
    def draw_red_flash(self, screen):
        """Affiche l'overlay rouge qui fade progressivement"""
        if self.is_active():
            elapsed = pygame.time.get_ticks() - self.start_time
            # Calculer l'alpha en fonction du temps écoulé (fade out progressif)
            alpha = int(150 * (1 - elapsed / self.duration))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(alpha)
            overlay.fill((255, 0, 0))  # Rouge
            screen.blit(overlay, (0, 0))
