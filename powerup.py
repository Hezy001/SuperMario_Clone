import pygame
import math
import random
from settings import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        self.x = x
        self.y = y
        
        # Get power-up properties
        self.properties = POWERUP_TYPES.get(powerup_type, {})
        self.color = self.properties.get("color", WHITE)
        self.effect = self.properties.get("effect", "none")
        self.points = self.properties.get("points", 100)
        
        # Animation properties
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.bob_offset = 0
        self.original_y = y
        self.rotation_angle = 0
        
        # Particle effects
        self.particles = []
        self.collect_particles = []
        
        # State
        self.is_collected = False
        self.collect_timer = 0
        
        # Create sprite
        self.create_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Sound effects
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds["powerup"] = pygame.mixer.Sound(SOUND_EFFECTS["powerup"])
        except:
            self.sounds = {}
    
    def create_sprite(self):
        """Create the power-up sprite"""
        size = POWERUP_SIZE
        
        if self.powerup_type == "mushroom":
            self.create_mushroom_sprite(size)
        elif self.powerup_type == "star":
            self.create_star_sprite(size)
        else:
            self.create_generic_sprite(size)
    
    def create_mushroom_sprite(self, size):
        """Create mushroom sprite"""
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Mushroom cap (red)
        cap_radius = size // 3
        cap_center = (size // 2, size // 3)
        pygame.draw.circle(self.image, RED, cap_center, cap_radius)
        
        # Mushroom stem (brown)
        stem_rect = pygame.Rect(size // 2 - 4, size // 3, 8, size // 2)
        pygame.draw.rect(self.image, BROWN, stem_rect)
        
        # White spots on cap
        spot_positions = [
            (cap_center[0] - 5, cap_center[1] - 3),
            (cap_center[0] + 5, cap_center[1] - 3),
            (cap_center[0], cap_center[1] + 2)
        ]
        for pos in spot_positions:
            pygame.draw.circle(self.image, WHITE, pos, 3)
        
        # Add border
        pygame.draw.circle(self.image, BLACK, cap_center, cap_radius, 2)
    
    def create_star_sprite(self, size):
        """Create star sprite"""
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        center = (size // 2, size // 2)
        star_radius = size // 3
        
        # Draw star
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            radius = star_radius if i % 2 == 0 else star_radius // 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(self.image, self.color, points)
            pygame.draw.polygon(self.image, BLACK, points, 2)
    
    def create_generic_sprite(self, size):
        """Create generic power-up sprite"""
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw a simple circle
        center = (size // 2, size // 2)
        radius = size // 3
        pygame.draw.circle(self.image, self.color, center, radius)
        pygame.draw.circle(self.image, BLACK, center, radius, 2)
        
        # Add a question mark
        font = pygame.font.Font(None, size // 2)
        text = font.render("?", True, BLACK)
        text_rect = text.get_rect(center=center)
        self.image.blit(text, text_rect)
    
    def create_sparkle_particles(self):
        """Create sparkle particles around the power-up"""
        for _ in range(4):
            particle = {
                'x': int(self.rect.centerx) + random.randint(-15, 15),
                'y': int(self.rect.centery) + random.randint(-15, 15),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'life': random.randint(40, 80),
                'max_life': random.randint(40, 80),
                'color': self.color,
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
    
    def create_collect_particles(self):
        """Create particles when power-up is collected"""
        for _ in range(15):
            particle = {
                'x': int(self.rect.centerx),
                'y': int(self.rect.centery),
                'vx': random.uniform(-4, 4),
                'vy': random.uniform(-6, -2),
                'life': random.randint(30, 60),
                'color': self.color,
                'size': random.randint(3, 6)
            }
            self.collect_particles.append(particle)
    
    def update_particles(self):
        """Update particle effects"""
        # Update sparkle particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                # Reset particle
                particle['life'] = particle['max_life']
                particle['x'] = int(self.rect.centerx) + random.randint(-15, 15)
                particle['y'] = int(self.rect.centery) + random.randint(-15, 15)
        
        # Update collect particles
        for particle in self.collect_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.collect_particles.remove(particle)
    
    def draw_particles(self, screen, camera):
        """Draw particle effects"""
        # Draw sparkle particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), particle['size'])
        
        # Draw collect particles
        for particle in self.collect_particles:
            alpha = int(255 * (particle['life'] / 60))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), particle['size'])
    
    def update(self):
        """Update power-up animation and state"""
        if not self.is_collected:
            # Bobbing animation
            self.animation_timer += self.animation_speed
            self.bob_offset = int(3 * abs(math.sin(self.animation_timer)))
            self.rect.y = self.original_y - self.bob_offset
            
            # Rotation animation for star
            if self.powerup_type == "star":
                self.rotation_angle += 2
                if self.rotation_angle >= 360:
                    self.rotation_angle = 0
            
            # Create sparkle particles occasionally
            if random.random() < 0.02:  # 2% chance per frame
                self.create_sparkle_particles()
        else:
            # Collection animation
            self.collect_timer += 1
            if self.collect_timer > 30:  # Remove after 30 frames
                self.kill()
        
        # Update particles
        self.update_particles()
    
    def collect(self):
        """Handle power-up collection"""
        if not self.is_collected:
            self.is_collected = True
            self.create_collect_particles()
            
            # Play sound effect
            if "powerup" in self.sounds:
                self.sounds["powerup"].play()
    
    def draw(self, screen, camera):
        """Draw the power-up with particles"""
        # Draw particles first
        self.draw_particles(screen, camera)
        
        if not self.is_collected:
            # Apply rotation for star
            if self.powerup_type == "star":
                rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
                powerup_rect = rotated_image.get_rect(center=self.rect.center)
                powerup_rect = camera.apply_rect(powerup_rect)
                screen.blit(rotated_image, powerup_rect)
            else:
                # Draw normally
                powerup_rect = camera.apply(self)
                screen.blit(self.image, powerup_rect) 