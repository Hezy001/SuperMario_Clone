import pygame
import math
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        
        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = False
        self.facing_right = True
        self.max_fall_speed = MAX_FALL_SPEED
        
        # Animation
        self.animation_timer = 0
        self.animation_speed = ANIMATION_SPEED
        self.animation_index = 0
        self.frame_count = 0
        
        # Power-up system
        self.powerup_state = "normal"  # normal, big, invincible
        self.powerup_timer = 0
        self.invincible_timer = 0
        self.invincible_duration = 2000  # 2 seconds
        
        # Particle effects
        self.particles = []
        self.jump_particles = []
        
        # Sound effects
        self.sounds = {}
        self.load_sounds()
        
        # Load sprites
        self.load_sprites()
        self.base_image = self.idle_sprites[0]
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Collision system reference
        self.collision_system = None
        
        # Camera shake
        self.camera_shake = 0
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds["jump"] = pygame.mixer.Sound(SOUND_EFFECTS["jump"])
            self.sounds["jump"].set_volume(0.7)  # Set jump sound volume
            self.sounds["powerup"] = pygame.mixer.Sound(SOUND_EFFECTS["powerup"])
            self.sounds["powerup"].set_volume(0.6)  # Set powerup sound volume
            self.sounds["enemy_hit"] = pygame.mixer.Sound(SOUND_EFFECTS["enemy_hit"])
            self.sounds["enemy_hit"].set_volume(0.5)  # Set enemy hit sound volume
        except:
            self.sounds = {}
    
    def load_sprites(self):
        """Load Mario sprites from assets"""
        try:
            # Load base sprites
            idle_sprite = pygame.image.load("assets/images/mario/idle.png").convert_alpha()
            idle_sprite = pygame.transform.scale(idle_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            
            jump_sprite = pygame.image.load("assets/images/mario/jump.png").convert_alpha()
            jump_sprite = pygame.transform.scale(jump_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            
            run1_sprite = pygame.image.load("assets/images/mario/run1.png").convert_alpha()
            run1_sprite = pygame.transform.scale(run1_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            
            run2_sprite = pygame.image.load("assets/images/mario/run2.png").convert_alpha()
            run2_sprite = pygame.transform.scale(run2_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            
            run3_sprite = pygame.image.load("assets/images/mario/run3.png").convert_alpha()
            run3_sprite = pygame.transform.scale(run3_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
            
            # Create sprite lists
            self.idle_sprites = [idle_sprite]
            self.jump_sprite = jump_sprite
            self.run_sprites = [run1_sprite, run2_sprite, run3_sprite]
            
        except Exception as e:
            print(f"Error loading sprites: {e}")
            self.create_fallback_sprites()
    
    def create_fallback_sprites(self):
        """Create simple colored rectangles as fallback sprites"""
        # Idle sprite (red rectangle)
        idle_sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        idle_sprite.fill(RED)
        self.idle_sprites = [idle_sprite]
        
        # Jump sprite (blue rectangle)
        self.jump_sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.jump_sprite.fill((0, 0, 255))
        
        # Run sprites (different shades of red)
        run1 = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        run1.fill((200, 0, 0))
        run2 = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        run2.fill((150, 0, 0))
        run3 = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        run3.fill((100, 0, 0))
        self.run_sprites = [run1, run2, run3]
    
    def handle_input(self):
        """Handle keyboard input for player movement"""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
        else:
            self.velocity_x = 0
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = PLAYER_JUMP_SPEED
            self.on_ground = False
            self.is_jumping = True
            self.create_jump_particles()
            if "jump" in self.sounds:
                self.sounds["jump"].play()
    
    def create_jump_particles(self):
        """Create particle effects when jumping"""
        for _ in range(8):
            particle = {
                'x': int(self.rect.centerx) + random.randint(-10, 10),
                'y': int(self.rect.bottom),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': random.randint(20, 40),
                'color': (255, 255, 255)
            }
            self.jump_particles.append(particle)
    
    def create_powerup_particles(self, color):
        """Create particle effects for power-ups"""
        for _ in range(PARTICLE_COUNT):
            particle = {
                'x': int(self.rect.centerx),
                'y': int(self.rect.centery),
                'vx': random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED),
                'vy': random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED),
                'life': PARTICLE_LIFETIME,
                'color': color
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Update particle effects"""
        # Update jump particles
        for particle in self.jump_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.jump_particles.remove(particle)
        
        # Update power-up particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen, camera):
        """Draw particle effects"""
        # Draw jump particles
        for particle in self.jump_particles:
            alpha = int(255 * (particle['life'] / 40))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 2)
        
        # Draw power-up particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / PARTICLE_LIFETIME))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 3)
    
    def update(self, platforms, jumping_blocks=None, pipes=None, enemies=None):
        """Update player physics and collision"""
        # Handle input
        self.handle_input()
        
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Limit fall speed
        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed
        
        # Update power-up timers
        if self.powerup_timer > 0:
            self.powerup_timer -= 16  # Assuming 60 FPS
            if self.powerup_timer <= 0:
                self.powerup_state = "normal"
                # Reset invincibility when star power-up expires
                if self.invincible_timer > 0:
                    self.invincible_timer = 0
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 16
            if self.invincible_timer <= 0:
                self.invincible_timer = 0
                # Ensure the image is restored to normal when invincibility expires
                if hasattr(self, 'base_image'):
                    self.image = self.base_image.copy()
        
        # Update position using collision system if available
        if self.collision_system:
            self.collision_system.update_player_collisions(
                self, platforms, jumping_blocks, pipes, enemies
            )
        else:
            # Fallback collision handling
            self.rect.x += self.velocity_x
            self.handle_horizontal_collision(platforms)
            
            self.rect.y += self.velocity_y
            self.handle_vertical_collision(platforms)
            
            # Handle jumping block collisions
            if jumping_blocks:
                self.handle_jumping_block_collision(jumping_blocks)
                
            # Handle pipe collisions
            if pipes:
                self.handle_pipe_collision(pipes)
        
        # Update animation
        self.update_animation()
        
        # Update particles
        self.update_particles()
        
        # Update frame count
        self.frame_count += 1
    
    def handle_horizontal_collision(self, platforms):
        """Handle horizontal collisions with platforms"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                    
    def handle_vertical_collision(self, platforms):
        """Handle vertical collisions with platforms"""
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    
    def handle_jumping_block_collision(self, jumping_blocks):
        """Handle collisions with jumping blocks"""
        for block in jumping_blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity_y > 0:  # Landing on top
                    self.rect.bottom = block.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.velocity_y < 0:  # Hitting from below
                    self.rect.top = block.rect.bottom
                    self.velocity_y = 0
                    
    def handle_pipe_collision(self, pipes):
        """Handle collisions with pipes"""
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                if self.velocity_y > 0:  # Landing on top
                    self.rect.bottom = pipe.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.velocity_x > 0:  # Moving right
                    self.rect.right = pipe.rect.left
                elif self.velocity_x < 0:  # Moving left
                    self.rect.left = pipe.rect.right
                    
    def update_animation(self):
        """Update player animation based on state"""
        self.animation_timer += self.animation_speed
        
        # Store the base image without any effects
        if self.is_jumping:
            self.base_image = self.jump_sprite
        elif abs(self.velocity_x) > 0:
            if self.animation_timer >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.run_sprites)
                self.animation_timer = 0
            self.animation_index = min(self.animation_index, len(self.run_sprites) - 1)
            self.base_image = self.run_sprites[self.animation_index]
        else:
            if self.animation_timer >= 1:
                self.animation_index = (self.animation_index + 1) % len(self.idle_sprites)
                self.animation_timer = 0
            self.animation_index = min(self.animation_index, len(self.idle_sprites) - 1)
            self.base_image = self.idle_sprites[self.animation_index]
            
        # Flip sprite based on direction
        if not self.facing_right:
            self.base_image = pygame.transform.flip(self.base_image, True, False)
        
        # Create display image (copy of base image)
        if hasattr(self, 'base_image') and self.base_image is not None:
            self.image = self.base_image.copy()
        else:
            # Fallback if base_image is not available
            self.image = self.idle_sprites[0].copy()
        
        # Apply invincibility effect - very subtle blinking
        if self.invincible_timer > 0 and self.frame_count % 12 < 6:
            # Create a very subtle transparent overlay for blinking effect
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 32))  # Very subtle (32 instead of 64)
            self.image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
    def apply_powerup(self, powerup_type):
        """Apply a power-up effect"""
        if powerup_type == "mushroom":
            self.powerup_state = "big"
            self.powerup_timer = POWERUP_TYPES["mushroom"]["duration"]
            self.create_powerup_particles(POWERUP_TYPES["mushroom"]["color"])
            if "powerup" in self.sounds:
                self.sounds["powerup"].play()
        elif powerup_type == "star":
            self.powerup_state = "invincible"
            self.powerup_timer = POWERUP_TYPES["star"]["duration"]
            # Set invincibility timer to 4 seconds (4000ms) as requested
            self.invincible_timer = 4000
            self.create_powerup_particles(POWERUP_TYPES["star"]["color"])
            if "powerup" in self.sounds:
                self.sounds["powerup"].play()
    
    def take_damage(self):
        """Handle player taking damage"""
        if self.invincible_timer > 0:
            return False  # Player is invincible
        
        if self.powerup_state == "big":
            self.powerup_state = "normal"
            self.powerup_timer = 0
        else:
            if "enemy_hit" in self.sounds:
                self.sounds["enemy_hit"].play()
            return True  # Player should lose a life
        
        # Set brief invincibility
        self.invincible_timer = 2000  # 2 seconds - reasonable time to recover
        return False
    
    def reset(self, x, y):
        """Reset player to starting position"""
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.is_jumping = False
        self.powerup_state = "normal"
        self.powerup_timer = 0
        self.invincible_timer = 0
        self.particles.clear()
        self.jump_particles.clear()
        
        # Ensure the image is restored to normal
        if hasattr(self, 'base_image') and self.base_image is not None:
            self.image = self.base_image.copy()
        else:
            self.image = self.idle_sprites[0].copy()
    
    def draw(self, screen, camera):
        """Draw the player with particles"""
        # Draw particles first
        self.draw_particles(screen, camera)
        
        # Draw the player
        player_rect = camera.apply(self)
        screen.blit(self.image, player_rect)
        
        # Debug: Show power-up state
        if hasattr(camera, 'debug_mode') and camera.debug_mode:
            font = pygame.font.Font(None, 24)
            powerup_text = font.render(f"Power: {self.powerup_state}", True, (255, 255, 0))
            text_rect = powerup_text.get_rect(center=(player_rect.centerx, player_rect.top - 20))
            screen.blit(powerup_text, text_rect) 