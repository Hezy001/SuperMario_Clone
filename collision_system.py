import pygame
from settings import *

class CollisionSystem:
    """Improved collision system with better physics and collision detection"""
    
    def __init__(self):
        self.debug_mode = False  # Set to True to see collision boxes
        
    def update_player_collisions(self, player, platforms, jumping_blocks=None, pipes=None, enemies=None):
        """Main collision update method for player"""
        
        # Store original position for collision resolution
        original_x = player.rect.x
        original_y = player.rect.y
        
        # Apply horizontal movement and collision
        player.rect.x += player.velocity_x
        self.resolve_horizontal_collisions(player, platforms, jumping_blocks, pipes)
        
        # Apply vertical movement and collision
        player.rect.y += player.velocity_y
        self.resolve_vertical_collisions(player, platforms, jumping_blocks, pipes)
        
        # Check enemy collisions (separate from movement collisions)
        if enemies:
            self.check_enemy_collisions(player, enemies)
    
    def resolve_horizontal_collisions(self, player, platforms, jumping_blocks=None, pipes=None):
        """Resolve horizontal collisions with proper collision response"""
        
        # Check platforms
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if player.velocity_x > 0:  # Moving right
                    player.rect.right = platform.rect.left
                    player.velocity_x = 0
                elif player.velocity_x < 0:  # Moving left
                    player.rect.left = platform.rect.right
                    player.velocity_x = 0
        
        # Check jumping blocks
        if jumping_blocks:
            for block in jumping_blocks:
                if player.rect.colliderect(block.rect):
                    if player.velocity_x > 0:  # Moving right
                        player.rect.right = block.rect.left
                        player.velocity_x = 0
                    elif player.velocity_x < 0:  # Moving left
                        player.rect.left = block.rect.right
                        player.velocity_x = 0
        
        # Check pipes
        if pipes:
            for pipe in pipes:
                if player.rect.colliderect(pipe.rect):
                    if player.velocity_x > 0:  # Moving right
                        player.rect.right = pipe.rect.left
                        player.velocity_x = 0
                    elif player.velocity_x < 0:  # Moving left
                        player.rect.left = pipe.rect.right
                        player.velocity_x = 0
    
    def resolve_vertical_collisions(self, player, platforms, jumping_blocks=None, pipes=None):
        """Resolve vertical collisions with proper collision response"""
        
        player.on_ground = False
        
        # Check platforms
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if player.velocity_y > 0:  # Falling down
                    player.rect.bottom = platform.rect.top
                    player.velocity_y = 0
                    player.on_ground = True
                    player.is_jumping = False
                elif player.velocity_y < 0:  # Jumping up
                    player.rect.top = platform.rect.bottom
                    player.velocity_y = 0
        
        # Check jumping blocks
        if jumping_blocks:
            for block in jumping_blocks:
                if player.rect.colliderect(block.rect):
                    if player.velocity_y > 0:  # Landing on top
                        player.rect.bottom = block.rect.top
                        player.velocity_y = 0
                        player.on_ground = True
                        player.is_jumping = False
                    elif player.velocity_y < 0:  # Hitting from below
                        player.rect.top = block.rect.bottom
                        player.velocity_y = 0
                        # Trigger block hit effect
                        block.hit()
        
        # Check pipes
        if pipes:
            for pipe in pipes:
                if player.rect.colliderect(pipe.rect):
                    if player.velocity_y > 0:  # Landing on top
                        player.rect.bottom = pipe.rect.top
                        player.velocity_y = 0
                        player.on_ground = True
                        player.is_jumping = False
                    elif player.velocity_y < 0:  # Hitting from below
                        player.rect.top = pipe.rect.bottom
                        player.velocity_y = 0
    
    def check_enemy_collisions(self, player, enemies):
        """Check and handle enemy collisions with proper response"""
        
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                # Determine collision direction
                collision_side = self.get_collision_side(player, enemy)
                
                if collision_side == "top":  # Player landing on enemy
                    # Kill enemy and bounce player
                    enemy.kill()
                    player.velocity_y = PLAYER_JUMP_SPEED * 0.7  # Bounce
                    player.on_ground = False
                    player.is_jumping = True
                    return "enemy_killed"
                    
                elif collision_side in ["left", "right", "bottom"]:  # Player hit by enemy
                    return "player_hit"
        
        return None
    
    def get_collision_side(self, player, enemy):
        """Determine which side of the enemy the player collided with"""
        
        # Calculate overlap on each axis
        overlap_x = min(player.rect.right, enemy.rect.right) - max(player.rect.left, enemy.rect.left)
        overlap_y = min(player.rect.bottom, enemy.rect.bottom) - max(player.rect.top, enemy.rect.top)
        
        # Determine collision side based on overlap and velocity
        if overlap_x < overlap_y:
            if player.rect.centerx < enemy.rect.centerx:
                return "left"
            else:
                return "right"
        else:
            if player.rect.centery < enemy.rect.centery:
                return "top"
            else:
                return "bottom"
    
    def check_coin_collisions(self, player, coins):
        """Check coin collection collisions"""
        collected_coins = []
        for coin in coins:
            if player.rect.colliderect(coin.rect):
                collected_coins.append(coin)
        return collected_coins
    
    def check_flag_collisions(self, player, flags):
        """Check flag/level completion collisions"""
        for flag in flags:
            if player.rect.colliderect(flag.rect):
                return True
        return False
    
    def update_enemy_collisions(self, enemy, platforms):
        """Update enemy collisions with platforms"""
        
        # Apply gravity
        enemy.velocity_y += GRAVITY
        
        # Move horizontally
        enemy.rect.x += enemy.velocity_x
        
        # Check horizontal collisions
        for platform in platforms:
            if enemy.rect.colliderect(platform.rect):
                if enemy.velocity_x > 0:  # Moving right
                    enemy.rect.right = platform.rect.left
                    enemy.change_direction()  # Use enemy's change_direction method
                elif enemy.velocity_x < 0:  # Moving left
                    enemy.rect.left = platform.rect.right
                    enemy.change_direction()  # Use enemy's change_direction method
        
        # Move vertically
        enemy.rect.y += enemy.velocity_y
        
        # Check vertical collisions
        enemy.on_ground = False
        for platform in platforms:
            if enemy.rect.colliderect(platform.rect):
                if enemy.velocity_y > 0:  # Falling
                    enemy.rect.bottom = platform.rect.top
                    enemy.velocity_y = 0
                    enemy.on_ground = True
                elif enemy.velocity_y < 0:  # Jumping up
                    enemy.rect.top = platform.rect.bottom
                    enemy.velocity_y = 0
    
    def draw_debug_collisions(self, screen, player, platforms, enemies=None, coins=None):
        """Draw collision boxes for debugging"""
        if not self.debug_mode:
            return
        
        # Draw player collision box
        pygame.draw.rect(screen, (255, 0, 0), player.rect, 2)
        
        # Draw platform collision boxes
        for platform in platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform.rect, 2)
        
        # Draw enemy collision boxes
        if enemies:
            for enemy in enemies:
                pygame.draw.rect(screen, (255, 255, 0), enemy.rect, 2)
        
        # Draw coin collision boxes
        if coins:
            for coin in coins:
                pygame.draw.rect(screen, (255, 255, 255), coin.rect, 2)
    
    def toggle_debug_mode(self):
        """Toggle debug collision visualization"""
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}") 