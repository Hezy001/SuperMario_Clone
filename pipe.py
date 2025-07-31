import pygame
from settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, height=100, pipe_type="normal"):
        super().__init__()
        self.pipe_type = pipe_type
        self.height = height
        
        # Create pipe sprite based on type
        self.create_pipe_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - height  # Position from bottom (y is ground level)
        # Ensure pipe touches the ground by setting bottom to ground level
        self.rect.bottom = y
        
    def create_pipe_sprite(self):
        """Create pipe sprite based on type"""
        self.image = pygame.Surface((60, self.height), pygame.SRCALPHA)
        
        if self.pipe_type == "normal":
            # Standard green pipe with Mario-style design
            # Top cap (darker green)
            pygame.draw.rect(self.image, (0, 120, 0), (0, 0, 60, 25))
            pygame.draw.rect(self.image, (0, 100, 0), (5, 5, 50, 15))
            # Pipe body (main green)
            pygame.draw.rect(self.image, (0, 150, 0), (5, 25, 50, self.height-25))
            # Inner pipe (darker green)
            pygame.draw.rect(self.image, (0, 100, 0), (10, 30, 40, self.height-35))
            # Highlight lines
            pygame.draw.line(self.image, (0, 200, 0), (10, 30), (10, self.height-5), 2)
            pygame.draw.line(self.image, (0, 200, 0), (50, 30), (50, self.height-5), 2)
            
        elif self.pipe_type == "warp":
            # Warp pipe (purple) with special design
            # Top cap (darker purple)
            pygame.draw.rect(self.image, (80, 0, 120), (0, 0, 60, 25))
            pygame.draw.rect(self.image, (60, 0, 100), (5, 5, 50, 15))
            # Pipe body (main purple)
            pygame.draw.rect(self.image, (100, 0, 150), (5, 25, 50, self.height-25))
            # Inner pipe (darker purple)
            pygame.draw.rect(self.image, (60, 0, 100), (10, 30, 40, self.height-35))
            # Warp effect lines
            pygame.draw.line(self.image, (150, 0, 200), (10, 30), (10, self.height-5), 2)
            pygame.draw.line(self.image, (150, 0, 200), (50, 30), (50, self.height-5), 2)
            # Add some sparkle effect
            for i in range(0, self.height, 30):
                pygame.draw.circle(self.image, (200, 100, 255), (30, i + 40), 2)
                
        elif self.pipe_type == "fire":
            # Fire pipe (red/orange) with fire effect
            # Top cap (dark red)
            pygame.draw.rect(self.image, (120, 30, 0), (0, 0, 60, 25))
            pygame.draw.rect(self.image, (100, 20, 0), (5, 5, 50, 15))
            # Pipe body (main red)
            pygame.draw.rect(self.image, (150, 50, 0), (5, 25, 50, self.height-25))
            # Inner pipe (darker red)
            pygame.draw.rect(self.image, (100, 30, 0), (10, 30, 40, self.height-35))
            # Fire effect lines
            pygame.draw.line(self.image, (255, 100, 0), (10, 30), (10, self.height-5), 2)
            pygame.draw.line(self.image, (255, 100, 0), (50, 30), (50, self.height-5), 2)
            # Add fire effect dots
            for i in range(0, self.height, 25):
                pygame.draw.circle(self.image, (255, 150, 0), (30, i + 45), 3)
                
        else:
            # Default to normal pipe
            pygame.draw.rect(self.image, (0, 120, 0), (0, 0, 60, 25))
            pygame.draw.rect(self.image, (0, 100, 0), (5, 5, 50, 15))
            pygame.draw.rect(self.image, (0, 150, 0), (5, 25, 50, self.height-25))
            pygame.draw.rect(self.image, (0, 100, 0), (10, 30, 40, self.height-35))
            pygame.draw.line(self.image, (0, 200, 0), (10, 30), (10, self.height-5), 2)
            pygame.draw.line(self.image, (0, 200, 0), (50, 30), (50, self.height-5), 2) 