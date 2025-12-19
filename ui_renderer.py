"""
Gère tout le rendu et l'affichage UI du jeu
"""
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class UIRenderer:
    """Gère le rendu de tous les éléments UI du jeu"""
    
    def __init__(self, game):
        """Initialise le rendu UI
        
        Args:
            game: Référence au jeu principal pour accéder aux états et ressources
        """
        self.game = game
    
    def _render_centered_text(self, text, font, color, center_pos):
        """Rend et affiche un texte centré"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.game.screen.blit(text_surface, text_rect)
    
    def draw_score(self):
        """Affiche le score de manière sobre avec le coin aztèque"""
        # Afficher le coin
        self.game.screen.blit(self.game.coin_icon, (10, 10))
        
        # Afficher le score à côté du coin
        score_text = self.game.font_score.render(str(self.game.score), True, (255, 215, 0))
        self.game.screen.blit(score_text, (50, 12))
    
    def draw_hearts(self):
        """Dessine les coeurs visuels dans le coin supérieur droit"""
        heart_x = SCREEN_WIDTH - 40
        heart_y = 10
        for i in range(self.game.health):
            self.game.screen.blit(self.game.heart_image, (heart_x - (i * 35), heart_y))
    
    def draw_transition(self):
        """Affiche un overlay noir pour la transition"""
        if self.game.transition_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(self.game.transition_alpha)
            overlay.fill((0, 0, 0))
            self.game.screen.blit(overlay, (0, 0))
    
    def draw_animated_arrow(self, x, y):
        """Dessine une flèche animée qui monte et descend pour indiquer l'emplacement de la téléportation"""
        # animation oscillante avec inversion de direction
        self.game.arrow_offset += self.game.arrow_speed * self.game.arrow_direction
        
        # Inverser la direction quand la flèche atteint les limites
        if self.game.arrow_offset >= 20 or self.game.arrow_offset <= -20:
            self.game.arrow_direction *= -1
        
        arrow_y = y + self.game.arrow_offset
        
        # Dessiner la flèche (triangle pointant vers le haut)
        arrow_size = 25
        tip = (x, arrow_y - arrow_size)
        
        # Base de la flèche
        left_base = (x - arrow_size, arrow_y)
        right_base = (x + arrow_size, arrow_y)
        
        points = [tip, left_base, right_base]
        pygame.draw.polygon(self.game.screen, (255, 215, 0), points)
        pygame.draw.polygon(self.game.screen, (255, 255, 255), points, 3)
        pygame.draw.line(self.game.screen, (255, 215, 0), left_base, right_base, 4)
        pygame.draw.line(self.game.screen, (255, 255, 255), left_base, right_base, 2)
    
    def draw_marker(self, x, y, color=(100, 255, 100), radius=20):
        """Dessine un marqueur visible à une position donnée"""
        pygame.draw.circle(self.game.screen, color, (x, y), radius)
        pygame.draw.circle(self.game.screen, (255, 255, 255), (x, y), radius, 3)
        pygame.draw.line(self.game.screen, (255, 255, 255), (x - 10, y), (x + 10, y), 2)
        pygame.draw.line(self.game.screen, (255, 255, 255), (x, y - 10), (x, y + 10), 2)
    
    def draw_enemy_health_bars(self):
        """Dessine les barres de vie de tous les ennemis"""
        for enemy in self.game.interior_enemies:
            bar_width = 40
            bar_height = 5
            bar_x = enemy.rect.centerx - bar_width // 2
            bar_y = enemy.rect.top - 15
            
            pygame.draw.rect(self.game.screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # calcul du ratio de santé pour la barre en pixels
            health_percentage = enemy.health / enemy.max_health
            health_width = bar_width * health_percentage
            pygame.draw.rect(self.game.screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
            
            pygame.draw.rect(self.game.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_game_over_screen(self):
        """Affiche l'écran game over avec le score et le meilleur score"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))
        
        panel_width = 500
        panel_height = 350
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
        
        pygame.draw.rect(self.game.screen, (20, 20, 40), (panel_x, panel_y, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(self.game.screen, (255, 215, 0), (panel_x, panel_y, panel_width, panel_height), 4, border_radius=15)
        
        self._render_centered_text("GAME OVER", self.game.font_large, (255, 0, 0), (SCREEN_WIDTH // 2, panel_y + 40))
        
        pygame.draw.line(self.game.screen, (255, 215, 0), (panel_x + 30, panel_y + 90), (panel_x + panel_width - 30, panel_y + 90), 2)
        
        self._render_centered_text(f"Score Final: {self.game.score}", self.game.font, (200, 200, 255), (SCREEN_WIDTH // 2, panel_y + 140))
        self._render_centered_text(f"Meilleur Score: {self.game.best_score}", self.game.font, (255, 215, 0), (SCREEN_WIDTH // 2, panel_y + 190))
        
        button_hover = self.game.restart_button.collidepoint(pygame.mouse.get_pos())
        if button_hover:
            pygame.draw.rect(self.game.screen, (0, 200, 0), self.game.restart_button, border_radius=8)
        else:
            pygame.draw.rect(self.game.screen, (0, 150, 0), self.game.restart_button, border_radius=8)
        
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.game.restart_button, 3, border_radius=8)
        self._render_centered_text("RESTART", self.game.font, (255, 255, 255), self.game.restart_button.center)

