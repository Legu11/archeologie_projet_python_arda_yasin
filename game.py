import pygame
import json
import os

from constants import *
from enemy import Enemy
from player import Player
from temple_gate import TempleGate
from projectile import Projectile
from aztec_coin import AztecCoin

class Game: 

    SCORES_FILE = 'best_score.json'

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mon Premier Jeu")

        # Charger et convertir les images de fond (pour meilleure performance)
        self.background_image = self._load_image('assets/images/temple.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.interior_image = self._load_image('assets/images/archeology_site.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.current_scene = "temple"
        self.player = Player()

        self.temple_gate = TempleGate(750, 400, 30, 30)
        self.gate_group = pygame.sprite.Group()
        self.gate_group.add(self.temple_gate)
        
        self.gate_marker_x = 800
        self.gate_marker_y = 450
        
        self.arrow_offset = 0
        self.arrow_direction = 1
        self.arrow_speed = 0.5
        
        self.interior_marker_x = 100
        self.interior_marker_y = GAME_FLOOR

        self.interior_enemies = pygame.sprite.Group()
        self.all_ennemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.score = 0
        self.best_score = self.load_best_score()
        self.font = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 60)
        
        # Cache pour les textes rendus (éviter de rerender chaque frame)
        self.score_text = None
        self.exit_text = None
        self.update_score_text()
        self.update_exit_text()
        
        self.health = 4
        self.max_health = 4
        self.last_hit_time = 0
        self.hit_cooldown = 1000
        self.heart_image = self._load_image('assets/images/red_heart.png', 40, 40)

        self.running = True
        self.game_over = False
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)

    def _load_image(self, path, width, height):
        """Charge et redimensionne une image"""
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (width, height))
        return image.convert_alpha()
    
    def _create_enemy_at_location(self, location):
        """Crée un ennemi à une position spécifique (left, right, top)"""
        enemy = Enemy()
        if location == 'left':
            enemy.rect.x = -200
            enemy.rect.y = GAME_FLOOR - 150
        elif location == 'right':
            enemy.rect.x = SCREEN_WIDTH + 100
            enemy.rect.y = GAME_FLOOR - 150
        else:  # top
            enemy.rect.x = SCREEN_WIDTH // 2 - 75
            enemy.rect.y = -200
        return enemy
    
    def _render_centered_text(self, text, font, color, center_pos):
        """Rend et affiche un texte centré"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.screen.blit(text_surface, text_rect)

    def load_best_score(self):
        """Charge le meilleur score depuis le fichier JSON"""
        if os.path.exists(self.SCORES_FILE):
            try:
                with open(self.SCORES_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('best_score', 0)
            except:
                return 0
        return 0
    
    def save_best_score(self):
        """Sauvegarde le meilleur score dans un fichier JSON"""
        if self.score > self.best_score:
            self.best_score = self.score
            try:
                with open(self.SCORES_FILE, 'w') as f:
                    json.dump({'best_score': self.best_score}, f)
            except:
                pass
    
    def update_score_text(self):
        """Met en cache le texte du score pour ne pas le re-renderer chaque frame"""
        self.score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
    
    def update_exit_text(self):
        """Met en cache le texte de sortie pour ne pas le re-renderer chaque frame"""
        self.exit_text = self.font.render("Appuyez sur E pour quitter, SPACE pour tirer", True, (255, 255, 255))

    def colision(self):
        # Ne vérifier les collisions que si le jeu n'est pas terminé
        if self.game_over:
            return
        
        # verifier si un ennemie touche le joueur
        if pygame.sprite.spritecollide(self.player, self.all_ennemies, True):
            self.game_over = True
            self.save_best_score()
            print("game over")

        # vérifier si le joueur touche la porte du temple
        if self.current_scene == "temple":
            if pygame.sprite.spritecollide(self.player, self.gate_group, False):
                self.enter_temple()
        
        # Collisions intérieures du temple
        if self.current_scene == "interior":
            # Vérifier si les projectiles touchent les monstres
            for projectile in self.player.all_projectiles:
                hit_enemies = pygame.sprite.spritecollide(projectile, self.interior_enemies, False)
                if hit_enemies:
                    projectile.kill()
                    for enemy in hit_enemies:
                        is_dead = enemy.take_damage(1)
                        
                        # Si l'ennemi est mort
                        if is_dead:
                            enemy.kill()
                            # Laisser tomber une pièce
                            coin = AztecCoin(enemy.rect.x, enemy.rect.y)
                            self.coins.add(coin)
                            self.score += 100
                            self.update_score_text()  # Mettre à jour le cache du texte
                            
                            # Respawner un monstre au même endroit
                            self.respawn_interior_enemy()
            
            # Vérifier si le joueur ramasse les pièces
            collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in collected_coins:
                self.score += 50
                self.update_score_text()
                print(f"Coin collected! Score: {self.score}")
            
            # Vérifier si un monstre touche le joueur
            if pygame.sprite.spritecollide(self.player, self.interior_enemies, False):
                current_time = pygame.time.get_ticks()
                # Vérifier le cooldown pour éviter que le joueur perde plusieurs coeurs d'un coup
                if current_time - self.last_hit_time > self.hit_cooldown:
                    self.health -= 1
                    self.last_hit_time = current_time
                    print(f"Hit! Health: {self.health}/4")
                    
                    if self.health <= 0:
                        self.game_over = True
                        self.save_best_score()
                        print("game over - no more hearts")
    
    def enter_temple(self):
        """Entrer à l'intérieur du temple"""
        self.current_scene = "interior"
        self.player.rect.x = 455
        self.player.rect.y = GAME_FLOOR
        self.player.last_shot_time = 0
        self.spawn_interior_enemies()
    
    def spawn_interior_enemies(self):
        """Spawn les monstres aztèques à l'intérieur du temple en dehors de l'écran"""
        self.interior_enemies.empty()
        for location in ['left', 'right', 'top']:
            enemy = self._create_enemy_at_location(location)
            self.interior_enemies.add(enemy)
    
    def respawn_interior_enemy(self):
        """Respawner un nouveau monstre aléatoirement depuis un côté"""
        import random
        spawn_location = random.choice(['left', 'right', 'top'])
        enemy = self._create_enemy_at_location(spawn_location)
        self.interior_enemies.add(enemy)
    
    def exit_temple(self):
        """Quitter l'intérieur du temple"""
        self.current_scene = "temple"
        # Repositionner le joueur devant la porte
        self.player.rect.x = 700
        self.player.rect.y = GAME_FLOOR
        
        # Nettoyer les ennemis intérieurs, les pièces et les projectiles
        self.interior_enemies.empty()
        self.coins.empty()
        self.player.all_projectiles.empty()

    def draw_animated_arrow(self, x, y):
        """Dessine une flèche animée qui monte et descend pour indiquer l'emplacement de la téléportation"""
        # animation oscillante avec inversion de direction
        self.arrow_offset += self.arrow_speed * self.arrow_direction
        
        # Inverser la direction quand la flèche atteint les limites
        if self.arrow_offset >= 20 or self.arrow_offset <= -20:
            self.arrow_direction *= -1
        
        arrow_y = y + self.arrow_offset
        
        # Dessiner la flèche (triangle pointant vers le haut)
        arrow_size = 25
        tip = (x, arrow_y - arrow_size)
        
        # Base de la flèche
        left_base = (x - arrow_size, arrow_y)
        right_base = (x + arrow_size, arrow_y)
        
        points = [tip, left_base, right_base]
        pygame.draw.polygon(self.screen, (255, 215, 0), points)
        pygame.draw.polygon(self.screen, (255, 255, 255), points, 3)
        pygame.draw.line(self.screen, (255, 215, 0), left_base, right_base, 4)
        pygame.draw.line(self.screen, (255, 255, 255), left_base, right_base, 2)
    
    def draw_marker(self, x, y, color=(100, 255, 100), radius=20):
        """Dessine un marqueur visible à une position donnée"""
        pygame.draw.circle(self.screen, color, (x, y), radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius, 3)
        pygame.draw.line(self.screen, (255, 255, 255), (x - 10, y), (x + 10, y), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (x, y - 10), (x, y + 10), 2)
    
    def draw_enemy_health_bars(self):
        """Dessine les barres de vie de tous les ennemis"""
        for enemy in self.interior_enemies:
            bar_width = 40
            bar_height = 5
            bar_x = enemy.rect.centerx - bar_width // 2
            bar_y = enemy.rect.top - 15
            
            pygame.draw.rect(self.screen, (200, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            
            # calcul du ratio de santé pour la barre en pixels
            health_percentage = enemy.health / enemy.max_health
            health_width = bar_width * health_percentage
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
            
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
    
    def draw_hearts(self):
        """Dessine les coeurs visuels dans le coin supérieur droit"""
        heart_x = SCREEN_WIDTH - 40
        heart_y = 10
        for i in range(self.health):
            self.screen.blit(self.heart_image, (heart_x - (i * 35), heart_y))
    
    def draw_game_over_screen(self):
        """Affiche l'écran game over avec le score et le meilleur score"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        panel_width = 500
        panel_height = 350
        panel_x = SCREEN_WIDTH // 2 - panel_width // 2
        panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
        
        pygame.draw.rect(self.screen, (20, 20, 40), (panel_x, panel_y, panel_width, panel_height), border_radius=15)
        pygame.draw.rect(self.screen, (255, 215, 0), (panel_x, panel_y, panel_width, panel_height), 4, border_radius=15)
        
        self._render_centered_text("GAME OVER", self.font_large, (255, 0, 0), (SCREEN_WIDTH // 2, panel_y + 40))
        
        pygame.draw.line(self.screen, (255, 215, 0), (panel_x + 30, panel_y + 90), (panel_x + panel_width - 30, panel_y + 90), 2)
        
        self._render_centered_text(f"Score Final: {self.score}", self.font, (200, 200, 255), (SCREEN_WIDTH // 2, panel_y + 140))
        self._render_centered_text(f"Meilleur Score: {self.best_score}", self.font, (255, 215, 0), (SCREEN_WIDTH // 2, panel_y + 190))
        
        button_hover = self.restart_button.collidepoint(pygame.mouse.get_pos())
        if button_hover:
            pygame.draw.rect(self.screen, (0, 200, 0), self.restart_button, border_radius=8)
        else:
            pygame.draw.rect(self.screen, (0, 150, 0), self.restart_button, border_radius=8)
        
        pygame.draw.rect(self.screen, (255, 255, 255), self.restart_button, 3, border_radius=8)
        self._render_centered_text("RESTART", self.font, (255, 255, 255), self.restart_button.center)
    
    def handle_game_over_click(self, pos):
        """Gère le clic sur le bouton restart"""
        if self.restart_button.collidepoint(pos):
            self.reset_game()
    
    def reset_game(self):
        """Réinitialise le jeu pour une nouvelle partie"""
        self.score = 0
        self.health = self.max_health
        self.current_scene = "temple"
        self.game_over = False
        self.last_hit_time = 0
        
        self.player.rect.x = 100
        self.player.rect.y = GAME_FLOOR
        
        self.interior_enemies.empty()
        self.all_ennemies.empty()
        self.coins.empty()
        self.player.all_projectiles.empty()

    def keyboard(self):
        # Ne pas traiter l'input du joueur si le jeu est terminé
        if self.game_over:
            return
        
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_RIGHT]:
            self.player.move_right()
            moved = True
        elif keys[pygame.K_LEFT]:
            self.player.move_left()
            moved = True
        elif keys[pygame.K_UP]:
            self.player.move_up()
            moved = True
        elif keys[pygame.K_DOWN]:
            self.player.move_down()
            moved = True

        if not moved:
            self.player.stop_moving()
        
        if keys[pygame.K_e] and self.current_scene == "interior":
            self.exit_temple()
        
        if keys[pygame.K_SPACE] and self.current_scene == "interior":
            self.player.launch_projectile()


    def run(self):
        clock = pygame.time.Clock() # initialiser une horloge
        while self.running:

            # Mettre à jour les collisions et la logique de jeu seulement si le jeu n'est pas terminé
            if not self.game_over:
                self.colision()

                for projectile in self.player.all_projectiles:
                    projectile.move()

                for coin in self.coins:
                    coin.fall()

                if self.current_scene == "temple":
                    for enemy in self.all_ennemies:
                        enemy.move()
                else:  # interior - les monstres suivent le joueur
                    for enemy in self.interior_enemies:
                        enemy.follow_player(self.player)

            clock.tick(100) 
            self.keyboard()
            
            # afficher le fond d'écran approprié selon la scène
            if self.current_scene == "temple":
                self.screen.blit(self.background_image, (0, 0))
            else:  
                self.screen.blit(self.interior_image, (0, 0))
            
            # Afficher le score (utiliser le texte en cache)
            if self.score_text:
                self.screen.blit(self.score_text, (10, 10))
            
            self.draw_hearts()
            
            # afficher les éléments selon la scène
            if self.current_scene == "temple":
                self.all_ennemies.draw(self.screen)
                # Afficher la flèche animée indiquant l'emplacement de la téléportation
                self.draw_animated_arrow(self.gate_marker_x, self.gate_marker_y)
            else:  # interior
                # Afficher le message pour quitter (utiliser le texte en cache)
                if self.exit_text:
                    self.screen.blit(self.exit_text, (SCREEN_WIDTH // 2 - 220, 50))
                
                # Afficher les monstres intérieurs
                self.interior_enemies.draw(self.screen)
                
                # Afficher les barres de vie des monstres
                self.draw_enemy_health_bars()
                
                # Afficher les pièces
                self.coins.draw(self.screen)
            
            # Afficher les projectiles
            self.player.all_projectiles.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            
            if self.game_over:
                self.draw_game_over_screen()
            
            pygame.display.flip() # actualiser l'écran

            # on parcourt tous les evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                       
                    print("fermeture du jeu")
                    self.running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        self.handle_game_over_click(event.pos)