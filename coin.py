import pygame
import math
from settings import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create a transparent surface for the coin
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw a proper circular coin
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)  # Gold circle
        pygame.draw.circle(self.image, (255, 165, 0), (10, 10), 8)   # Darker gold inner circle
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 6)   # Bright gold center
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.bob_offset = 0
        self.original_y = y
        
    def update(self):
        # Simple bobbing animation
        self.animation_timer += self.animation_speed
        self.bob_offset = int(3 * abs(math.sin(self.animation_timer)))
        self.rect.y = self.original_y - self.bob_offset 