import pygame

class TempleGate(pygame.sprite.Sprite):
    """Représente la porte du temple qui permet d'entrer à l'intérieur"""
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 150, 0))  # transparent
