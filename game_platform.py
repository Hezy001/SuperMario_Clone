import pygame
from settings import *

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Make ground wider to cover the entire level and extend left of Mario
        self.image = pygame.Surface((SCREEN_WIDTH * 4, 100))
        self.image.fill(GREEN)
        
        # Add some texture to the ground
        for i in range(0, self.image.get_width(), 50):
            pygame.draw.line(self.image, (0, 100, 0), (i, 0), (i, 100), 2)
        
        self.rect = self.image.get_rect()
        # Position ground to extend left of Mario's starting position (100, 300)
        self.rect.x = -SCREEN_WIDTH  # Start ground to the left of screen
        self.rect.y = SCREEN_HEIGHT - 100

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        
        # Add some texture to platforms
        for i in range(0, width, 20):
            pygame.draw.line(self.image, (0, 100, 0), (i, 0), (i, height), 1)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 