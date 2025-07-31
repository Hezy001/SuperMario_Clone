import pygame
import math
import random
from settings import *

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 80
        self.height = 200
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Animation properties
        self.flag_wave_offset = 0
        self.flag_wave_speed = 0.15
        self.pole_color = (139, 69, 19)  # Brown
        self.flag_color = RED
        self.base_color = (101, 67, 33)  # Darker brown
        self.gold_color = (255, 215, 0)
        
        # Particle effects
        self.particles = []
        self.sparkle_particles = []
        
        # State
        self.is_reached = False
        self.reach_timer = 0
        self.celebration_mode = False
        
        # Create Mario-style flag
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.create_flag_design()
        
        # Sound effects
        self.sounds = {}
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds["level_complete"] = pygame.mixer.Sound(SOUND_EFFECTS["level_complete"])
        except:
            self.sounds = {}
        
    def create_flag_design(self):
        """Create the flag design"""
        # Clear the surface
        self.image.fill((0, 0, 0, 0))
        
        # Draw flag pole (vertical line)
        pole_width = 8
        pole_x = self.width - 20
        pygame.draw.line(self.image, self.pole_color, 
                        (pole_x, 0), (pole_x, self.height - 30), pole_width)
        
        # Draw flag (red rectangle with white border)
        flag_width = 60
        flag_height = 40
        flag_x = pole_x - flag_width - 5
        flag_y = 30
        
        # Flag background
        pygame.draw.rect(self.image, self.flag_color, 
                        (flag_x, flag_y, flag_width, flag_height))
        
        # Flag border
        pygame.draw.rect(self.image, WHITE, 
                        (flag_x, flag_y, flag_width, flag_height), 3)
        
        # Flag pole top decoration
        pygame.draw.circle(self.image, self.gold_color, (pole_x, 15), 12)  # Gold circle
        pygame.draw.circle(self.image, BLACK, (pole_x, 15), 12, 3)  # Border
        
        # Flag base/platform
        base_width = 60
        base_height = 30
        base_x = pole_x - base_width // 2
        base_y = self.height - base_height
        
        pygame.draw.rect(self.image, self.base_color, 
                        (base_x, base_y, base_width, base_height))
        pygame.draw.rect(self.image, BLACK, 
                        (base_x, base_y, base_width, base_height), 3)
        
        # Add some decorative elements
        self.add_decorative_elements()
        
    def add_decorative_elements(self):
        """Add decorative elements to the flag"""
        pole_x = self.width - 20
        
        # Add small circles along the pole
        for i in range(3):
            y_pos = 50 + i * 40
            pygame.draw.circle(self.image, self.gold_color, (pole_x, y_pos), 4)
        
        # Add a small star on the flag
        flag_x = pole_x - 65
        flag_y = 35
        self.draw_star(self.image, (flag_x + 30, flag_y + 20), 8, WHITE)
        
        # Add some sparkles around the flag
        self.create_sparkle_particles()
        
    def create_sparkle_particles(self):
        """Create sparkle particles around the flag"""
        pole_x = self.width - 20
        flag_x = pole_x - 65
        flag_y = 35
        
        for _ in range(6):
            particle = {
                'x': int(flag_x) + random.randint(0, 60),
                'y': int(flag_y) + random.randint(0, 40),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'life': random.randint(60, 120),
                'max_life': random.randint(60, 120),
                'color': self.gold_color,
                'size': random.randint(2, 4)
            }
            self.sparkle_particles.append(particle)
    
    def create_celebration_particles(self):
        """Create celebration particles when flag is reached"""
        for _ in range(20):
            particle = {
                'x': int(self.rect.centerx) + random.randint(-30, 30),
                'y': int(self.rect.centery) + random.randint(-50, 50),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(-5, -1),
                'life': random.randint(40, 80),
                'color': random.choice([RED, self.gold_color, WHITE, GREEN]),
                'size': random.randint(3, 6)
            }
            self.particles.append(particle)
    
    def update_particles(self):
        """Update particle effects"""
        # Update sparkle particles
        for particle in self.sparkle_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                # Reset particle
                particle['life'] = particle['max_life']
                particle['x'] = int(self.rect.x) + random.randint(0, self.width)
                particle['y'] = int(self.rect.y) + random.randint(0, self.height)
        
        # Update celebration particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen, camera):
        """Draw particle effects"""
        # Draw sparkle particles
        for particle in self.sparkle_particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), particle['size'])
        
        # Draw celebration particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 80))
            # Convert to RGB color (pygame.draw.circle doesn't support alpha)
            color = particle['color'][:3]  # Take only RGB components
            pos = camera.apply_pos(particle['x'], particle['y'])
            pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), particle['size'])
        
    def draw_star(self, surface, center, size, color):
        """Draw a simple star shape"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            radius = size if i % 2 == 0 else size // 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)
        
    def update(self):
        """Update flag animation"""
        # Animate flag waving
        self.flag_wave_offset += self.flag_wave_speed
        if self.flag_wave_offset > 2 * math.pi:
            self.flag_wave_offset = 0
        
        # Update celebration mode
        if self.celebration_mode:
            self.reach_timer += 1
            if self.reach_timer % 10 == 0:  # Create particles every 10 frames
                self.create_celebration_particles()
        
        # Update particles
        self.update_particles()
        
    def draw(self, screen, camera):
        """Draw the flag with wave animation and particles"""
        # Draw particles first
        self.draw_particles(screen, camera)
        
        # Create a copy of the image for animation
        animated_image = self.image.copy()
        
        # Add wave effect to the flag
        pole_x = self.width - 20
        flag_x = pole_x - 65
        flag_y = 30
        
        # Redraw flag with enhanced wave effect
        wave_offset = int(4 * math.sin(self.flag_wave_offset))
        wave_offset2 = int(2 * math.sin(self.flag_wave_offset * 2))
        
        # Clear the flag area
        pygame.draw.rect(animated_image, (0, 0, 0, 0), 
                        (flag_x, flag_y, 60, 40))
        
        # Draw wavy flag with multiple wave points
        flag_points = [
            (flag_x, flag_y),
            (flag_x + 20, flag_y + wave_offset),
            (flag_x + 40, flag_y + wave_offset2),
            (flag_x + 60, flag_y + wave_offset),
            (flag_x + 60, flag_y + 40 + wave_offset),
            (flag_x + 40, flag_y + 40 + wave_offset2),
            (flag_x + 20, flag_y + 40 + wave_offset),
            (flag_x, flag_y + 40)
        ]
        
        pygame.draw.polygon(animated_image, self.flag_color, flag_points)
        pygame.draw.polygon(animated_image, WHITE, flag_points, 2)
        
        # Add celebration glow effect
        if self.celebration_mode:
            glow_surface = pygame.Surface(animated_image.get_size(), pygame.SRCALPHA)
            glow_intensity = int(50 + 30 * math.sin(self.reach_timer * 0.1))
            glow_surface.fill((255, 255, 255, glow_intensity))
            animated_image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Apply camera transformation and draw
        flag_rect = camera.apply(self)
        screen.blit(animated_image, flag_rect)
        
    def check_collision(self, player):
        """Check if player collides with the flag"""
        return self.rect.colliderect(player.rect)
    
    def reach_flag(self):
        """Handle flag being reached"""
        if not self.is_reached:
            self.is_reached = True
            self.celebration_mode = True
            self.reach_timer = 0
            self.create_celebration_particles()
            
            # Play celebration sound
            if "level_complete" in self.sounds:
                self.sounds["level_complete"].play()
    
    def reset(self):
        """Reset flag state"""
        self.is_reached = False
        self.celebration_mode = False
        self.reach_timer = 0
        self.particles.clear() 