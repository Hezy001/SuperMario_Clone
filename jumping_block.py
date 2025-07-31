import pygame
import math
import random
from settings import *

class JumpingBlock(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type="single", content_type="coin"):
        super().__init__()
        self.block_type = block_type
        self.content_type = content_type
        self.x = x
        self.y = y
        
        # Load sprite and set up rect
        self.load_sprite()
        self.image = self.question_block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation properties
        self.animation_timer = 0
        self.animation_speed = ANIMATION_SPEED
        self.bob_offset = 0
        self.original_y = y
        
        # State
        self.is_hit = False
        self.hit_timer = 0
        self.hit_duration = 30  # frames
        self.has_given_points = False  # Track if points were already given
        self.has_given_content = False  # Track if content was given
        
        # Enhanced Mario-style jiggle effect
        self.jiggle_offset = 0
        self.jiggle_intensity = 0
        self.jiggle_speed = JIGGLE_SPEED
        self.jiggle_decay = JIGGLE_DECAY
        self.jiggle_phase = 0
        
        # Particle effects
        self.particles = []
        self.hit_particles = []
        
        # Collision detection
        self.last_collision_frame = -1
        self.current_frame = 0
        
        # Sound effects
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds["block_hit"] = pygame.mixer.Sound(SOUND_EFFECTS["block_hit"])
            self.sounds["coin"] = pygame.mixer.Sound(SOUND_EFFECTS["coin"])
            self.sounds["powerup"] = pygame.mixer.Sound(SOUND_EFFECTS["powerup"])
        except:
            self.sounds = {}
    
    def load_sprite(self):
        """Load question mark block sprite"""
        try:
            # Load question mark block sprite from assets
            base_block = pygame.image.load("assets/images/mario/question mario.png").convert_alpha()
            base_block = pygame.transform.scale(base_block, (50, 50))
            
            # Create different block variations
            if self.block_type == "single":
                self.question_block = base_block
            elif self.block_type == "double":
                # Create a double-width block
                self.question_block = pygame.Surface((100, 50), pygame.SRCALPHA)
                self.question_block.blit(base_block, (0, 0))
                self.question_block.blit(base_block, (50, 0))
            elif self.block_type == "triple":
                # Create a triple-width block
                self.question_block = pygame.Surface((150, 50), pygame.SRCALPHA)
                self.question_block.blit(base_block, (0, 0))
                self.question_block.blit(base_block, (50, 0))
                self.question_block.blit(base_block, (100, 0))
        except Exception as e:
            print(f"Error loading jumping block sprite: {e}")
            self.create_fallback_sprite()
    
    def create_fallback_sprite(self):
        """Create fallback sprite if asset loading fails"""
        if self.block_type == "single":
            width, height = 50, 50
        elif self.block_type == "double":
            width, height = 100, 50
        elif self.block_type == "triple":
            width, height = 150, 50
        else:
            width, height = 50, 50
            
        # Create a yellow question mark block
        self.question_block = pygame.Surface((width, height))
        self.question_block.fill(YELLOW)
        pygame.draw.rect(self.question_block, BLACK, (0, 0, width, height), 3)
        
        # Draw a simple question mark
        font = pygame.font.Font(None, 36)
        text = font.render("?", True, BLACK)
        text_rect = text.get_rect(center=(width//2, height//2))
        self.question_block.blit(text, text_rect)
    
    def create_hit_particles(self):
        """Create particle effects when block is hit"""
        for _ in range(12):
            particle = {
                'x': int(self.rect.centerx) + random.randint(-20, 20),
                'y': int(self.rect.centery) + random.randint(-10, 10),
                'vx': random.uniform(-4, 4),
                'vy': random.uniform(-6, -2),
                'life': random.randint(30, 60),
                'color': (255, 255, 0)  # Yellow particles
            }
            self.hit_particles.append(particle)
    
    def create_content_particles(self, content_type):
        """Create particles for block content"""
        color = (255, 215, 0) if content_type == "coin" else POWERUP_TYPES.get(content_type, {}).get("color", (255, 255, 255))
        
        for _ in range(8):
            particle = {
                'x': int(self.rect.centerx),
                'y': int(self.rect.top),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-4, -1),
                'life': random.randint(40, 80),
                'color': color
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Update particle effects"""
        # Update hit particles
        for particle in self.hit_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.hit_particles.remove(particle)
        
        # Update content particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen, camera):
        """Draw particle effects"""
        # Draw hit particles
        for particle in self.hit_particles:
            alpha = int(255 * (particle['life'] / 60))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 3)
        
        # Draw content particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 80))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 4)
            
    def update(self):
        """Update block animation and state"""
        self.current_frame += 1
        
        if not self.is_hit:
            # Bobbing animation for question blocks
            self.animation_timer += self.animation_speed
            self.bob_offset = int(2 * abs(math.sin(self.animation_timer)))
            self.rect.y = self.original_y - self.bob_offset
        else:
            # Hit animation
            self.hit_timer += 1
            if self.hit_timer >= self.hit_duration:
                self.is_hit = False
                self.hit_timer = 0
                
        # Update enhanced jiggle effect
        if self.jiggle_intensity > 0.1:
            self.jiggle_phase += self.jiggle_speed
            # Multi-frequency jiggle for more realistic effect
            jiggle1 = math.sin(self.jiggle_phase) * self.jiggle_intensity
            jiggle2 = math.sin(self.jiggle_phase * 2) * self.jiggle_intensity * 0.5
            jiggle3 = math.sin(self.jiggle_phase * 3) * self.jiggle_intensity * 0.25
            self.jiggle_offset = int(jiggle1 + jiggle2 + jiggle3)
            self.jiggle_intensity *= self.jiggle_decay
        else:
            self.jiggle_offset = 0
            self.jiggle_intensity = 0
            self.jiggle_phase = 0
        
        # Update particles
        self.update_particles()
            
    def check_collision_from_below(self, player):
        """Check if player is hitting this block from below"""
        if self.current_frame == self.last_collision_frame:
            return False  # Already processed this frame
            
        if not self.rect.colliderect(player.rect):
            return False
            
        # Check if player is moving upward and hitting from below
        if player.velocity_y < 0:  # Moving upward
            # Check if player's top is hitting the block's bottom
            player_top = player.rect.top
            block_bottom = self.rect.bottom
            
            # Allow some tolerance for collision detection
            if abs(player_top - block_bottom) < 15:
                self.last_collision_frame = self.current_frame
                return True
                
        return False
            
    def hit(self):
        """Handle block being hit from below"""
        if not self.is_hit:
            self.is_hit = True
            self.hit_timer = 0
            self.jiggle_intensity = JIGGLE_INTENSITY
            
            # Create hit particles
            self.create_hit_particles()
            
            # Create content particles if content exists
            if not self.has_given_content and self.content_type != "empty":
                self.create_content_particles(self.content_type)
            
            # Play sound effect
            if "block_hit" in self.sounds:
                self.sounds["block_hit"].play()
            
            # Change appearance when hit
            self.change_hit_appearance()
                
    def change_hit_appearance(self):
        """Change block appearance when hit"""
        try:
            if self.block_type == "single":
                self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
                # Create a darker version
                dark_block = pygame.image.load("assets/images/mario/question mario.png").convert_alpha()
                dark_block = pygame.transform.scale(dark_block, (50, 50))
                dark_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                dark_surface.fill((139, 69, 19, 128))  # Brown with transparency
                dark_block.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = dark_block
            elif self.block_type == "double":
                self.image = pygame.Surface((100, 50), pygame.SRCALPHA)
                dark_block = pygame.image.load("assets/images/mario/question mario.png").convert_alpha()
                dark_block = pygame.transform.scale(dark_block, (50, 50))
                dark_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                dark_surface.fill((139, 69, 19, 128))
                dark_block.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image.blit(dark_block, (0, 0))
                self.image.blit(dark_block, (50, 0))
            elif self.block_type == "triple":
                self.image = pygame.Surface((150, 50), pygame.SRCALPHA)
                dark_block = pygame.image.load("assets/images/mario/question mario.png").convert_alpha()
                dark_block = pygame.transform.scale(dark_block, (50, 50))
                dark_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                dark_surface.fill((139, 69, 19, 128))
                dark_block.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image.blit(dark_block, (0, 0))
                self.image.blit(dark_block, (50, 0))
                self.image.blit(dark_block, (100, 0))
        except Exception as e:
            # Fallback: create a brown block
            if self.block_type == "single":
                width, height = 50, 50
            elif self.block_type == "double":
                width, height = 100, 50
            elif self.block_type == "triple":
                width, height = 150, 50
            else:
                width, height = 50, 50
                
            self.image = pygame.Surface((width, height))
            self.image.fill((139, 69, 19))  # Brown color
            pygame.draw.rect(self.image, BLACK, (0, 0, width, height), 3)
                
    def get_points(self):
        """Get points for hitting this block (only once)"""
        if not self.has_given_points:
            self.has_given_points = True
            return 200
        return 0
    
    def get_content(self):
        """Get content from this block (only once)"""
        if not self.has_given_content:
            self.has_given_content = True
            return self.content_type
        return None
    
    def reset_points(self):
        """Reset the points flag (for new levels)"""
        self.has_given_points = False
        self.has_given_content = False
        self.last_collision_frame = -1
    
    def draw(self, screen, camera):
        """Draw the block with jiggle effect and particles"""
        # Draw particles first
        self.draw_particles(screen, camera)
        
        # Apply jiggle effect to the image
        if self.jiggle_offset != 0:
            # Create a copy of the image with jiggle offset
            jiggled_image = self.image.copy()
            # Apply horizontal jiggle
            jiggled_rect = jiggled_image.get_rect()
            jiggled_rect.x = self.jiggle_offset
            
            # Create a new surface with the jiggled image
            final_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            final_image.blit(jiggled_image, jiggled_rect)
        else:
            final_image = self.image
        
        # Draw the block
        block_rect = camera.apply(self)
        screen.blit(final_image, block_rect) 