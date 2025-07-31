import pygame
import sys
import os
from game import MarioGame

def main():
    # Change to the directory containing this script so asset paths work correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create game instance
    game = MarioGame()
    
    # Game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Update game
        game.update()
        
        # Draw everything
        game.draw()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 