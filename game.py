import pygame

from constants import *
from enemy import Enemy
from player import Player
from temple_gate import TempleGate

class Game: 

    def __init__(self):
        # créer la fenêtre du jeu 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mon Premier Jeu")

        # importer l'image d'arrière plan
        self.background_image = pygame.image.load('assets/images/temple.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # importer l'image intérieure du temple
        self.interior_image = pygame.image.load('assets/images/archeology_site.jpg')
        self.interior_image = pygame.transform.scale(self.interior_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # gestion des scènes
        self.current_scene = "temple"  # "temple" ou "interior"
        
        # créer le joueur
        self.player = Player()

        # créer la porte du temple (position où se trouve le perso)
        self.temple_gate = TempleGate(750, 400, 30, 30)
        self.gate_group = pygame.sprite.Group()
        self.gate_group.add(self.temple_gate)
        
        # Position du marqueur de la porte du temple
        self.gate_marker_x = 800
        self.gate_marker_y = 450
        
        # Position du marqueur intérieur (où le joueur arrive en entrant)
        self.interior_marker_x = 100
        self.interior_marker_y = GAME_FLOOR

        # creer le groupe avec les ennemies
        self.all_ennemies = pygame.sprite.Group()
        #self.all_ennemies.add(Enemy())
        #self.all_ennemies.add(Enemy())
        #self.all_ennemies.add(Enemy())
        

        # créer un score
        self.score = 0
        self.font = pygame.font.Font(None, 30)


        # maintenir allumé la fenêtre du jeu
        self.running = True

    def colision(self):         
        # verifier si un ennemie touche le joueur
        if pygame.sprite.spritecollide(self.player, self.all_ennemies, True):
            self.running = False
            print("game over")

        # vérifier si le joueur touche la porte du temple
        if self.current_scene == "temple":
            if pygame.sprite.spritecollide(self.player, self.gate_group, False):
                self.enter_temple()
    
    def enter_temple(self):
        """Entrer à l'intérieur du temple"""
        self.current_scene = "interior"
        # Repositionner le joueur à l'entrée de l'intérieur
        self.player.rect.x = 100
        self.player.rect.y = GAME_FLOOR
    
    def exit_temple(self):
        """Quitter l'intérieur du temple"""
        self.current_scene = "temple"
        # Repositionner le joueur devant la porte
        self.player.rect.x = 700
        self.player.rect.y = GAME_FLOOR

    def draw_marker(self, x, y, color=(100, 255, 100), radius=20):
        """Dessine un marqueur visible à une position donnée"""
        # Cercle principal
        pygame.draw.circle(self.screen, color, (x, y), radius)
        # Bordure du cercle
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius, 3)
        # Croix au centre
        pygame.draw.line(self.screen, (255, 255, 255), (x - 10, y), (x + 10, y), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (x, y - 10), (x, y + 10), 2)

    def keyboard(self):
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
        
        # Appuyer sur E pour quitter l'intérieur du temple
        if keys[pygame.K_e] and self.current_scene == "interior":
            self.exit_temple()


    def run(self):
        clock = pygame.time.Clock() # initialiser une horloge
        while self.running:

            self.colision()

            # deplacer tout les ennemies (uniquement à l'extérieur du temple)
            if self.current_scene == "temple":
                for enemy in self.all_ennemies:
                    enemy.move()

            clock.tick(120) # 120 fps 
            self.keyboard()
            
            # afficher le fond d'écran approprié selon la scène
            if self.current_scene == "temple":
                self.screen.blit(self.background_image, (0, 0))
            else:  # interior
                self.screen.blit(self.interior_image, (0, 0))

            # dessiner le score
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            
            # afficher les éléments selon la scène
            if self.current_scene == "temple":
                self.all_ennemies.draw(self.screen)
                # Afficher le marqueur de la porte du temple
                self.draw_marker(self.gate_marker_x, self.gate_marker_y, color=(100, 200, 255))
            else:  # interior
                # afficher un message pour quitter
                exit_text = self.font.render("Appuyez sur E pour quitter", True, (255, 255, 255))
                self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - 150, 50))
            
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip() # actualiser l'écran

            # on parcourt tous les evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                       
                    print("fermeture du jeu")
                    self.running = False
                    pygame.quit()