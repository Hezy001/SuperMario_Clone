import pygame
import math
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="left", enemy_type="goomba"):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        self.enemy_type = enemy_type
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        
        # Physics
        self.velocity_x = ENEMY_SPEED if direction == "right" else -ENEMY_SPEED
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = GRAVITY
        
        # Animation
        self.animation_timer = 0
        self.animation_speed = 0.15
        self.animation_index = 0
        self.frame_count = 0
        
        # AI behavior - varied initialization
        self.behavior_timer = random.randint(0, 60)  # Random start time
        self.behavior_interval = random.randint(60, 180)  # 1-3 seconds
        self.patrol_distance = random.randint(50, 150)
        self.start_x = x
        self.is_jumping = False
        self.jump_cooldown = random.randint(0, 30)  # Random initial cooldown
        
        # Enemy-specific variations
        if self.enemy_type == "koopa":
            # Koopas are more aggressive and jump more
            self.behavior_interval = random.randint(40, 120)  # Faster behavior changes
            self.patrol_distance = random.randint(80, 200)  # Larger patrol area
        else:  # Goomba
            # Goombas are slower and more predictable
            self.behavior_interval = random.randint(80, 240)  # Slower behavior changes
            self.patrol_distance = random.randint(30, 100)  # Smaller patrol area
        
        # State
        self.is_alive = True
        self.is_stunned = False
        self.stun_timer = 0
        self.health = 1
        
        # Particle effects
        self.particles = []
        self.death_particles = []
        
        # Load sprites and create rect
        self.load_sprites()
        self.image = self.walk_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Sound effects
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds["enemy_hit"] = pygame.mixer.Sound(SOUND_EFFECTS["enemy_hit"])
        except:
            self.sounds = {}
    
    def load_sprites(self):
        """Load enemy sprites based on type"""
        try:
            if self.enemy_type == "koopa":
                self.load_koopa_sprites()
            else:  # goomba
                self.load_goomba_sprites()
        except Exception as e:
            print(f"Error loading enemy sprites: {e}")
            self.create_fallback_sprites()
    
    def load_koopa_sprites(self):
        """Load Koopa sprites"""
        try:
            # Load Koopa sprite from assets
            koopa_sprite = pygame.image.load("assets/images/koopas/koopa.png").convert_alpha()
            koopa_sprite = pygame.transform.scale(koopa_sprite, (ENEMY_WIDTH, ENEMY_HEIGHT))
            
            # Create walk animation frames
            self.walk_sprites = [koopa_sprite]
            
            # Create a second frame by slightly modifying the first
            frame2 = koopa_sprite.copy()
            # Add some visual variation
            overlay = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 30))
            frame2.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.walk_sprites.append(frame2)
            
        except Exception as e:
            print(f"Error loading Koopa sprites: {e}")
            self.create_fallback_sprites()
    
    def load_goomba_sprites(self):
        """Load Goomba sprites"""
        try:
            # Create Goomba sprites (brown mushroom-like enemy)
            self.walk_sprites = []
            
            # Frame 1: Normal Goomba
            frame1 = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
            # Body (brown circle)
            pygame.draw.circle(frame1, BROWN, (ENEMY_WIDTH//2, ENEMY_HEIGHT//2), ENEMY_WIDTH//3)
            # Eyes (white circles with black pupils)
            pygame.draw.circle(frame1, WHITE, (ENEMY_WIDTH//2 - 8, ENEMY_HEIGHT//2 - 5), 4)
            pygame.draw.circle(frame1, WHITE, (ENEMY_WIDTH//2 + 8, ENEMY_HEIGHT//2 - 5), 4)
            pygame.draw.circle(frame1, BLACK, (ENEMY_WIDTH//2 - 8, ENEMY_HEIGHT//2 - 5), 2)
            pygame.draw.circle(frame1, BLACK, (ENEMY_WIDTH//2 + 8, ENEMY_HEIGHT//2 - 5), 2)
            # Angry eyebrows
            pygame.draw.line(frame1, BLACK, (ENEMY_WIDTH//2 - 12, ENEMY_HEIGHT//2 - 8), 
                           (ENEMY_WIDTH//2 - 4, ENEMY_HEIGHT//2 - 10), 2)
            pygame.draw.line(frame1, BLACK, (ENEMY_WIDTH//2 + 4, ENEMY_HEIGHT//2 - 10), 
                           (ENEMY_WIDTH//2 + 12, ENEMY_HEIGHT//2 - 8), 2)
            self.walk_sprites.append(frame1)
            
            # Frame 2: Slightly different
            frame2 = frame1.copy()
            # Move eyebrows down slightly
            pygame.draw.rect(frame2, (0, 0, 0, 0), (ENEMY_WIDTH//2 - 12, ENEMY_HEIGHT//2 - 10, 24, 4))
            pygame.draw.line(frame2, BLACK, (ENEMY_WIDTH//2 - 12, ENEMY_HEIGHT//2 - 6), 
                           (ENEMY_WIDTH//2 - 4, ENEMY_HEIGHT//2 - 8), 2)
            pygame.draw.line(frame2, BLACK, (ENEMY_WIDTH//2 + 4, ENEMY_HEIGHT//2 - 8), 
                           (ENEMY_WIDTH//2 + 12, ENEMY_HEIGHT//2 - 6), 2)
            self.walk_sprites.append(frame2)
            
        except Exception as e:
            print(f"Error loading Goomba sprites: {e}")
            self.create_fallback_sprites()
    
    def create_fallback_sprites(self):
        """Create fallback sprites if asset loading fails"""
        # Create simple colored rectangles
        frame1 = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        frame1.fill(RED if self.enemy_type == "koopa" else BROWN)
        pygame.draw.rect(frame1, BLACK, (0, 0, ENEMY_WIDTH, ENEMY_HEIGHT), 2)
        
        frame2 = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        frame2.fill(RED if self.enemy_type == "koopa" else BROWN)
        pygame.draw.rect(frame2, BLACK, (0, 0, ENEMY_WIDTH, ENEMY_HEIGHT), 2)
        # Add some variation
        pygame.draw.circle(frame2, WHITE, (ENEMY_WIDTH//2, ENEMY_HEIGHT//2), 5)
        
        self.walk_sprites = [frame1, frame2]
    
    def create_death_particles(self):
        """Create death particle effects"""
        for _ in range(12):
            particle = {
                'x': int(self.rect.centerx) + random.randint(-10, 10),
                'y': int(self.rect.centery) + random.randint(-10, 10),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -2),
                'life': random.randint(30, 60),
                'color': RED if self.enemy_type == "koopa" else BROWN,
                'size': random.randint(2, 4)
            }
            self.death_particles.append(particle)
    
    def update_particles(self):
        """Update particle effects"""
        # Update death particles
        for particle in self.death_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.death_particles.remove(particle)
    
    def draw_particles(self, screen, camera):
        """Draw particle effects"""
        # Draw death particles
        for particle in self.death_particles:
            alpha = int(255 * (particle['life'] / 60))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), particle['size'])
    
    def update(self, platforms):
        """Update enemy physics and AI"""
        if not self.is_alive:
            self.update_particles()
            return
        
        # Update behavior timer
        self.behavior_timer += 1
        
        # AI behavior
        self.update_ai()
        
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Limit fall speed
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.rect.x += self.velocity_x
        self.handle_horizontal_collision(platforms)
        
        self.rect.y += self.velocity_y
        self.handle_vertical_collision(platforms)
        
        # Update animation
        self.update_animation()
        
        # Update frame count
        self.frame_count += 1
        
        # Update stun timer
        if self.is_stunned:
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.is_stunned = False
        
        # Update jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
    
    def update_ai(self):
        """Update enemy AI behavior with varied movements"""
        # Patrol behavior
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.direction = "left" if self.rect.x > self.start_x else "right"
            self.velocity_x = ENEMY_SPEED if self.direction == "right" else -ENEMY_SPEED
        
        # Random behavior changes
        if self.behavior_timer >= self.behavior_interval:
            self.behavior_timer = 0
            # Varied behavior intervals based on enemy type
            if self.enemy_type == "koopa":
                self.behavior_interval = random.randint(40, 120)  # Faster for Koopas
            else:
                self.behavior_interval = random.randint(80, 240)  # Slower for Goombas
            
            # Random direction change (varies by enemy type)
            if self.enemy_type == "koopa":
                if random.random() < 0.4:  # 40% chance for Koopas
                    self.direction = "right" if self.direction == "left" else "left"
                    self.velocity_x = ENEMY_SPEED if self.direction == "right" else -ENEMY_SPEED
            else:  # Goomba
                if random.random() < 0.2:  # 20% chance for Goombas
                    self.direction = "right" if self.direction == "left" else "left"
                    self.velocity_x = ENEMY_SPEED if self.direction == "right" else -ENEMY_SPEED
            
            # Random jump (for Koopas) - more aggressive
            if self.enemy_type == "koopa" and self.on_ground and self.jump_cooldown <= 0:
                if random.random() < 0.6:  # 60% chance for Koopas
                    self.velocity_y = ENEMY_JUMP_SPEED
                    self.on_ground = False
                    self.is_jumping = True
                    self.jump_cooldown = random.randint(30, 90)  # Variable cooldown
            
            # Random speed changes
            if random.random() < 0.3:  # 30% chance
                speed_multiplier = random.uniform(0.5, 1.5)
                self.velocity_x = ENEMY_SPEED * speed_multiplier if self.direction == "right" else -ENEMY_SPEED * speed_multiplier
            
            # Random pause (especially for Goombas)
            if self.enemy_type == "goomba" and random.random() < 0.2:  # 20% chance
                self.velocity_x = 0
                self.behavior_interval = random.randint(30, 90)  # Shorter pause
    
    def handle_horizontal_collision(self, platforms):
        """Handle horizontal collisions with platforms"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                    self.direction = "left"
                    self.velocity_x = -ENEMY_SPEED
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                    self.direction = "right"
                    self.velocity_x = ENEMY_SPEED
                    
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
    
    def update_animation(self):
        """Update enemy animation"""
        self.animation_timer += self.animation_speed
        
        if self.animation_timer >= 1:
            self.animation_index = (self.animation_index + 1) % len(self.walk_sprites)
            self.animation_timer = 0
        
        self.image = self.walk_sprites[self.animation_index]
        
        # Flip sprite based on direction
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        
        # Apply stun effect
        if self.is_stunned and self.frame_count % 4 < 2:
            # Create a transparent overlay
            overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))
            self.image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
    def take_damage(self):
        """Handle enemy taking damage"""
        if self.is_stunned:
            return False
        
        self.health -= 1
        if self.health <= 0:
            self.die()
            return True
        else:
            self.is_stunned = True
            self.stun_timer = 30  # 0.5 seconds
            return False
    
    def die(self):
        """Handle enemy death"""
        self.is_alive = False
        self.create_death_particles()
        
        # Play death sound
        if "enemy_hit" in self.sounds:
            self.sounds["enemy_hit"].play()
    
    def draw(self, screen, camera):
        """Draw the enemy with particles"""
        # Draw particles first
        self.draw_particles(screen, camera)
        
        if self.is_alive:
            # Draw the enemy
            enemy_rect = camera.apply(self)
            screen.blit(self.image, enemy_rect) 