import pygame
import math
import random
from settings import *

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Camera position
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        
        # Camera modes
        self.CAMERA_FOLLOW = "follow"
        self.CAMERA_LERP = "lerp"
        self.CAMERA_LOCKED = "locked"
        self.current_mode = self.CAMERA_LERP
        
        # Smoothing
        self.smoothness = CAMERA_SMOOTHNESS
        
        # Level boundaries
        self.level_width = 0
        self.level_height = 0
        
        # Zoom system
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.zoom_speed = CAMERA_ZOOM_SPEED
        
        # Shake system
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_decay = CAMERA_SHAKE_DECAY
        
        # Debug mode
        self.debug_mode = False
        
    def set_level_dimensions(self, width, height=None):
        """Set the level dimensions for camera boundaries"""
        self.level_width = width
        self.level_height = height or self.screen_height
    
    def set_camera_mode(self, mode):
        """Set the camera mode"""
        if mode in [self.CAMERA_FOLLOW, self.CAMERA_LERP, self.CAMERA_LOCKED]:
            self.current_mode = mode
    
    def set_zoom(self, zoom, instant=False):
        """Set camera zoom level"""
        self.target_zoom = max(0.5, min(2.0, zoom))  # Clamp between 0.5 and 2.0
        if instant:
            self.zoom_level = self.target_zoom
    
    def shake_camera(self, intensity, duration):
        """Trigger camera shake effect"""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)
    
    def update(self, target):
        """Update camera position based on target"""
        if not target:
            return
        
        # Calculate target position
        target_x = target.rect.centerx - self.screen_width // 2
        target_y = target.rect.centery - self.screen_height // 2
        
        # Apply level boundaries
        target_x = max(0, min(target_x, self.level_width - self.screen_width))
        target_y = max(0, min(target_y, self.level_height - self.screen_height))
        
        # Update based on camera mode
        if self.current_mode == self.CAMERA_FOLLOW:
            self.x = target_x
            self.y = target_y
        elif self.current_mode == self.CAMERA_LERP:
            self.x += (target_x - self.x) * self.smoothness
            self.y += (target_y - self.y) * self.smoothness
        # CAMERA_LOCKED doesn't update position
        
        # Update zoom
        if abs(self.zoom_level - self.target_zoom) > 0.01:
            self.zoom_level += (self.target_zoom - self.zoom_level) * self.zoom_speed
        
        # Update shake effect
        self.update_shake()
    
    def update_shake(self):
        """Update camera shake effect"""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calculate shake offset
            if self.shake_intensity > 0:
                self.shake_offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
                self.shake_offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
                
                # Decay shake intensity
                self.shake_intensity *= self.shake_decay
                
                if self.shake_intensity < 0.1:
                    self.shake_intensity = 0
        else:
            # Reset shake when duration is over
            self.shake_offset_x = 0
            self.shake_offset_y = 0
            self.shake_intensity = 0
    
    def apply(self, sprite):
        """Apply camera transformation to a sprite"""
        # Calculate position with shake and zoom
        x = (sprite.rect.x - self.x + self.shake_offset_x) * self.zoom_level
        y = (sprite.rect.y - self.y + self.shake_offset_y) * self.zoom_level
        
        # Create transformed rect
        transformed_rect = sprite.rect.copy()
        transformed_rect.x = x
        transformed_rect.y = y
        transformed_rect.width *= self.zoom_level
        transformed_rect.height *= self.zoom_level
        
        return transformed_rect
    
    def apply_rect(self, rect):
        """Apply camera transformation to a rect"""
        # Calculate position with shake and zoom
        x = (rect.x - self.x + self.shake_offset_x) * self.zoom_level
        y = (rect.y - self.y + self.shake_offset_y) * self.zoom_level
        
        # Create transformed rect
        transformed_rect = rect.copy()
        transformed_rect.x = x
        transformed_rect.y = y
        transformed_rect.width *= self.zoom_level
        transformed_rect.height *= self.zoom_level
        
        return transformed_rect
    
    def apply_pos(self, x, y):
        """Apply camera transformation to coordinates"""
        # Calculate position with shake and zoom
        transformed_x = (x - self.x + self.shake_offset_x) * self.zoom_level
        transformed_y = (y - self.y + self.shake_offset_y) * self.zoom_level
        
        return (transformed_x, transformed_y)
    
    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates"""
        return self.apply_pos(world_x, world_y)
    
    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x / self.zoom_level) + self.x - self.shake_offset_x
        world_y = (screen_y / self.zoom_level) + self.y - self.shake_offset_y
        return (world_x, world_y)
    
    def is_visible(self, sprite):
        """Check if a sprite is visible on screen"""
        transformed_rect = self.apply(sprite)
        
        # Check if sprite is within screen bounds
        return (transformed_rect.right > 0 and 
                transformed_rect.left < self.screen_width and
                transformed_rect.bottom > 0 and 
                transformed_rect.top < self.screen_height)
    
    def get_visible_area(self):
        """Get the visible world area"""
        top_left = self.screen_to_world(0, 0)
        bottom_right = self.screen_to_world(self.screen_width, self.screen_height)
        
        return {
            'left': top_left[0],
            'top': top_left[1],
            'right': bottom_right[0],
            'bottom': bottom_right[1],
            'width': bottom_right[0] - top_left[0],
            'height': bottom_right[1] - top_left[1]
        }
    
    def reset(self):
        """Reset camera to initial state"""
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.zoom_level = 1.0
        self.target_zoom = 1.0
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
    
    def draw_debug_info(self, screen):
        """Draw debug information about the camera"""
        if not self.debug_mode:
            return
        
        font = pygame.font.Font(None, 24)
        
        # Camera position
        pos_text = font.render(f"Camera: ({self.x:.1f}, {self.y:.1f})", True, (255, 255, 0))
        screen.blit(pos_text, (10, 10))
        
        # Zoom level
        zoom_text = font.render(f"Zoom: {self.zoom_level:.2f}", True, (255, 255, 0))
        screen.blit(zoom_text, (10, 35))
        
        # Camera mode
        mode_text = font.render(f"Mode: {self.current_mode}", True, (255, 255, 0))
        screen.blit(mode_text, (10, 60))
        
        # Shake info
        if self.shake_intensity > 0:
            shake_text = font.render(f"Shake: {self.shake_intensity:.1f}", True, (255, 0, 0))
            screen.blit(shake_text, (10, 85))
        
        # Visible area
        visible_area = self.get_visible_area()
        area_text = font.render(f"Area: {visible_area['left']:.0f},{visible_area['top']:.0f} to {visible_area['right']:.0f},{visible_area['bottom']:.0f}", True, (255, 255, 0))
        screen.blit(area_text, (10, 110)) 