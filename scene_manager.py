import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_FLOOR
from enemy import Enemy
from skeleton_enemy import SkeletonEnemy


class SceneManager:
    """Gère les transitions entre scènes et la logique des scènes intérieures"""
    
    def __init__(self, game):
        """
        Initialise le gestionnaire de scènes
        :param game: Référence à l'objet Game
        """
        self.game = game
    
    def update_transition(self):
        if self.game.transition_active:
            self.game.transition_alpha -= 1  # Fade out progressif (très lent)
            if self.game.transition_alpha <= 0:
                self.game.transition_alpha = 0
                self.game.transition_active = False
    
    def enter_temple(self):
        self.game.current_scene = "interior"
        self.game.player.rect.x = 455
        self.game.player.rect.y = GAME_FLOOR
        self.game.player.last_shot_time = 0
        self.spawn_interior_enemies()

        self.game.transition_alpha = 200  # Fade rapide
        self.game.transition_active = True
    
    def exit_temple(self):
        """Quitter l'intérieur du temple"""
        self.game.current_scene = "temple"
        # Repositionner le joueur un peu en arrière de l'entrée du temple (pour éviter la téléportation automatique)
        self.game.player.rect.x = self.game.gate_marker_x - 150
        self.game.player.rect.y = self.game.gate_marker_y
        
        # Nettoyer les ennemis intérieurs, les pièces et les projectiles
        self.game.interior_enemies.empty()
        self.game.coins.empty()
        self.game.player.all_projectiles.empty()
    
    def enter_cave(self):
        """Entrer à l'intérieur de la grotte avec transition"""
        self.game.current_scene = "dark_cave"
        self.game.player.rect.x = 455
        self.game.player.rect.y = GAME_FLOOR
        self.game.player.last_shot_time = 0
        self.spawn_cave_enemies()
        # Déclencher la transition
        self.game.transition_alpha = 200
        self.game.transition_active = True
    
    def exit_cave(self):
        """Quitter l'intérieur de la grotte"""
        self.game.current_scene = "temple"
        # Repositionner le joueur un peu en arrière de l'entrée de la grotte (pour éviter la téléportation automatique)
        self.game.player.rect.x = self.game.cave_marker_x - 150
        self.game.player.rect.y = self.game.cave_marker_y
        
        # Nettoyer les ennemis intérieurs, les pièces et les projectiles
        self.game.interior_enemies.empty()
        self.game.coins.empty()
        self.game.player.all_projectiles.empty()
    
    def spawn_interior_enemies(self):
        """Spawn les monstres aztèques à l'intérieur du temple en dehors de l'écran"""
        self.game.interior_enemies.empty()
        for location in ['left', 'right', 'top']:
            enemy = self._create_enemy_at_location(location)
            self.game.interior_enemies.add(enemy)
    
    def spawn_cave_enemies(self):
        """Spawn les squelettes à l'intérieur de la grotte (uniquement de gauche et droite)"""
        self.game.interior_enemies.empty()
        for location in ['left', 'right']:
            skeleton = self._create_skeleton_at_location(location)
            self.game.interior_enemies.add(skeleton)
    
    def respawn_interior_enemy(self):
        """Respawner un nouveau monstre aléatoirement depuis un côté"""
        if self.game.current_scene == "dark_cave":
            spawn_location = random.choice(['left', 'right'])
            enemy = self._create_skeleton_at_location(spawn_location)
        else:
            spawn_location = random.choice(['left', 'right', 'top'])
            enemy = self._create_enemy_at_location(spawn_location)
        self.game.interior_enemies.add(enemy)
    
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
    
    def _create_skeleton_at_location(self, location):
        """Crée un squelette à une position spécifique (left, right, top)"""
        skeleton = SkeletonEnemy()
        if location == 'left':
            skeleton.rect.x = -200
            skeleton.rect.y = GAME_FLOOR - 150
        elif location == 'right':
            skeleton.rect.x = SCREEN_WIDTH + 100
            skeleton.rect.y = GAME_FLOOR - 150
        else:  # top
            skeleton.rect.x = SCREEN_WIDTH // 2 - 75
            skeleton.rect.y = -200
        return skeleton
