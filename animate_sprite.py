import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_path, sprite_width, sprite_height, animation_speed=0.2):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.animation_speed = animation_speed

        self.columns = 8  # nombre de sprites par ligne
        self.rows = 4      # nombre de lignes (directions)

        self.frame_width = self.sprite_sheet.get_width() // self.columns
        self.frame_height = self.sprite_sheet.get_height() // self.rows


        # Créer un dictionnaire pour stocker les animations par direction
        # Assumer que les 4 premières frames horizontales sont les 4 directions
        self.animations = {
        'down': self.load_animation_frames(0),
        'left': self.load_animation_frames(1),
        'right': self.load_animation_frames(2),
        'up': self.load_animation_frames(3)
        }


        # État d'animation initial
        self.current_direction = 'down'
        self.current_frame = 0
        self.animation_timer = 0
        self.is_moving = False

        # Image initiale
        self.image = self.animations[self.current_direction][self.current_frame]
        self.rect = self.image.get_rect()

    def load_animation_frames(self, row):
        frames = []
        for col in range(self.columns):
            x = col * self.frame_width
            y = row * self.frame_height

            frame = self.sprite_sheet.subsurface(
                (x, y, self.frame_width, self.frame_height)
            )

            frame = pygame.transform.scale(
                frame, (self.sprite_width, self.sprite_height)
            )

            frames.append(frame)

        return frames

    def update_animation(self, direction=None):
        """Met à jour l'animation en fonction de la direction"""
        if direction:
            self.current_direction = direction
            self.is_moving = True
        elif not self.is_moving:
            # Si pas de mouvement, rester sur la première frame
            self.current_frame = 0
            self.image = self.animations[self.current_direction][self.current_frame]
            return

        # Mettre à jour le timer d'animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_direction])

        self.image = self.animations[self.current_direction][self.current_frame]

    def stop_animation(self):
        """Arrête l'animation et revient à la première frame"""
        self.is_moving = False
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.animations[self.current_direction][self.current_frame]