import pygame
import json
import os

from constants import *
from enemy import Enemy
from player import Player
from temple_gate import TempleGate
from projectile import Projectile
from aztec_coin import AztecCoin
from shake_animation import ShakeAnimation
from scene_manager import SceneManager
from ui_renderer import UIRenderer

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
        self.font_score = pygame.font.Font(None, 36)
        
        # Cache pour les textes rendus (éviter de rerender chaque frame)
        self.exit_text = None
        self.update_exit_text()
        
        # Charger l'image du coin aztèque pour l'affichage du score
        self.coin_icon = self._load_image('assets/images/aztec_coin.png', 32, 32)
        
        self.health = 4
        self.max_health = 4
        self.last_hit_time = 0
        self.hit_cooldown = 1000
        self.heart_image = self._load_image('assets/images/red_heart.png', 40, 40)

        self.running = True
        self.game_over = False
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
        
        # Variables pour la transition simple
        self.transition_alpha = 0
        self.transition_active = False
        
        # Effet de shake et overlay rouge
        self.shake_animation = ShakeAnimation(duration=300, intensity=5)
        
        # Gestionnaire de scènes
        self.scene_manager = SceneManager(self)
        
        # Gestionnaire UI
        self.ui_renderer = UIRenderer(self)

    def _load_image(self, path, width, height):
        """Charge et redimensionne une image"""
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (width, height))
        return image.convert_alpha()
    



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
                self.scene_manager.enter_temple()
        
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
                            
                            # Respawner un monstre au même endroit
                            self.scene_manager.respawn_interior_enemy()
            
            # Vérifier si le joueur ramasse les pièces
            collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in collected_coins:
                self.score += 50
                print(f"Coin collected! Score: {self.score}")
            
            # Vérifier si un monstre touche le joueur
            if pygame.sprite.spritecollide(self.player, self.interior_enemies, False):
                current_time = pygame.time.get_ticks()
                # Vérifier le cooldown pour éviter que le joueur perde plusieurs coeurs d'un coup
                if current_time - self.last_hit_time > self.hit_cooldown:
                    self.health -= 1
                    self.last_hit_time = current_time
                    self.shake_animation.trigger()  # Déclencher l'effet de hit
                    print(f"Hit! Health: {self.health}/4")
                    
                    if self.health <= 0:
                        self.game_over = True
                        self.save_best_score()
                        print("game over - no more hearts")
    

    

    

    






    
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
            self.scene_manager.exit_temple()
        
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
            
            # Mettre à jour la transition
            self.scene_manager.update_transition()

            clock.tick(100) 
            self.keyboard()
            
            # Récupérer l'offset de shake
            shake_x, shake_y = self.shake_animation.get_shake_offset()
            
            # afficher le fond d'écran approprié selon la scène
            if self.current_scene == "temple":
                self.screen.blit(self.background_image, (shake_x, shake_y))
            else:  
                self.screen.blit(self.interior_image, (shake_x, shake_y))
            
            # Afficher le score avec le coin aztèque
            self.ui_renderer.draw_score()
            
            self.ui_renderer.draw_hearts()
            
            # afficher les éléments selon la scène
            if self.current_scene == "temple":
                self.all_ennemies.draw(self.screen)
                # Afficher la flèche animée indiquant l'emplacement de la téléportation
                self.ui_renderer.draw_animated_arrow(self.gate_marker_x, self.gate_marker_y)
            else:  # interior
                # Afficher le message pour quitter (utiliser le texte en cache)
                if self.exit_text:
                    self.screen.blit(self.exit_text, (SCREEN_WIDTH // 2 - 220, 50))
                
                # Afficher les monstres intérieurs
                self.interior_enemies.draw(self.screen)
                
                # Afficher les barres de vie des monstres
                self.ui_renderer.draw_enemy_health_bars()
                
                # Afficher les pièces
                self.coins.draw(self.screen)
            
            # Afficher les projectiles
            self.player.all_projectiles.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            
            if self.game_over:
                self.ui_renderer.draw_game_over_screen()
            
            # Afficher la transition
            self.ui_renderer.draw_transition()
            
            # Afficher l'effet de hit (overlay rouge)
            self.shake_animation.draw_red_flash(self.screen)
            
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