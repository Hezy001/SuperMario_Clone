import pygame
import pygame.mixer
from settings import *
from player import Player
from enemy import Enemy
from game_platform import Ground, Platform
from coin import Coin
from jumping_block import JumpingBlock
from camera import Camera
from pipe import Pipe
from flag import Flag
from powerup import PowerUp
from collision_system import CollisionSystem

class MarioGame:
    def __init__(self):
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Enhanced Game")
        
        # Game state
        self.game_state = MENU
        self.current_level = 0
        self.score = 0
        self.lives = 3
        
        # Floating score text for visual feedback
        self.floating_scores = []  # List of (text, x, y, timer) tuples
        
        # Initialize collision system
        self.collision_system = CollisionSystem()
        
        # Initialize sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.jumping_blocks = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Initialize player
        self.player = Player(100, 300)
        self.player.collision_system = self.collision_system  # Connect collision system
        self.all_sprites.add(self.player)
        
        # Initialize ground
        self.ground = Ground()
        self.platforms.add(self.ground)
        self.all_sprites.add(self.ground)
        
        # Initialize camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Load sounds
        self.load_sounds()
        
        # Load background
        self.load_background()
        
        # Initialize font
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, UI_SMALL_FONT_SIZE)
        
        # Level completion tracking
        self.level_complete_timer = 0
        self.level_complete_duration = 120  # 2 seconds at 60 FPS
        
    def load_sounds(self):
        try:
            self.jump_sound = pygame.mixer.Sound(SOUND_EFFECTS["jump"])
            self.jump_sound.set_volume(0.7)  # Jump sound volume
            self.coin_sound = pygame.mixer.Sound(SOUND_EFFECTS["coin"])
            self.coin_sound.set_volume(0.6)  # Coin sound volume
            self.powerup_sound = pygame.mixer.Sound(SOUND_EFFECTS["powerup"])
            self.powerup_sound.set_volume(0.6)  # Powerup sound volume
            self.enemy_hit_sound = pygame.mixer.Sound(SOUND_EFFECTS["enemy_hit"])
            self.enemy_hit_sound.set_volume(0.5)  # Enemy hit sound volume
            self.block_hit_sound = pygame.mixer.Sound(SOUND_EFFECTS["block_hit"])
            self.block_hit_sound.set_volume(0.5)  # Block hit sound volume
            self.level_complete_sound = pygame.mixer.Sound(SOUND_EFFECTS["level_complete"])
            self.level_complete_sound.set_volume(0.8)  # Level complete sound volume
            self.game_over_sound = pygame.mixer.Sound(SOUND_EFFECTS["game_over"])
            self.game_over_sound.set_volume(0.6)  # Game over sound volume
            self.main_theme = pygame.mixer.Sound(SOUND_EFFECTS["main_theme"])
            self.main_theme.set_volume(0.5)  # Main theme volume
        except:
            self.jump_sound = None
            self.coin_sound = None
            self.powerup_sound = None
            self.enemy_hit_sound = None
            self.block_hit_sound = None
            self.level_complete_sound = None
            self.game_over_sound = None
            self.main_theme = None
            
    def load_background(self):
        try:
            self.background = pygame.image.load("assets/images/mario/cloud.png").convert_alpha()
            # Make the background much smaller like original Mario
            bg_rect = self.background.get_rect()
            scale = min(SCREEN_WIDTH / bg_rect.width, SCREEN_HEIGHT / bg_rect.height) * 0.1  # Much smaller scale
            new_width = int(bg_rect.width * scale)
            new_height = int(bg_rect.height * scale)
            self.background = pygame.transform.scale(self.background, (new_width, new_height))
            self.background.set_alpha(60)  # More transparent
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = None
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_state == MENU:
                self.start_game()
            elif event.key == pygame.K_r and self.game_state == GAME_OVER:
                self.reset_game()
            elif event.key == pygame.K_p and self.game_state == PLAYING:
                self.game_state = PAUSED
            elif event.key == pygame.K_p and self.game_state == PAUSED:
                self.game_state = PLAYING
            elif event.key == pygame.K_F1:  # Debug key
                self.collision_system.toggle_debug_mode()
                self.camera.debug_mode = not self.camera.debug_mode
            elif event.key == pygame.K_F2:  # Camera mode toggle
                if self.camera.current_mode == self.camera.CAMERA_LERP:
                    self.camera.set_camera_mode(self.camera.CAMERA_FOLLOW)
                    print("Camera mode: Instant follow")
                elif self.camera.current_mode == self.camera.CAMERA_FOLLOW:
                    self.camera.set_camera_mode(self.camera.CAMERA_LOCKED)
                    print("Camera mode: Locked")
                else:
                    self.camera.set_camera_mode(self.camera.CAMERA_LERP)
                    print("Camera mode: Smooth follow")
            elif event.key == pygame.K_F3:  # Camera shake test
                self.camera.shake_camera(15, 30)
                print("Camera shake triggered")
            elif event.key == pygame.K_F4:  # Zoom in
                self.camera.set_zoom(self.camera.zoom_level + 0.2)
                print(f"Zoom: {self.camera.zoom_level:.1f}")
            elif event.key == pygame.K_F5:  # Zoom out
                self.camera.set_zoom(self.camera.zoom_level - 0.2)
                print(f"Zoom: {self.camera.zoom_level:.1f}")
            elif event.key == pygame.K_F6:  # Reset zoom
                self.camera.set_zoom(1.0, instant=True)
                print("Zoom reset to 1.0")
                
    def start_game(self):
        self.game_state = PLAYING
        self.current_level = 0
        self.score = 0
        self.lives = 3
        self.load_level(self.current_level)
        # Reset camera for new game
        self.camera.reset()
        if self.main_theme:
            self.main_theme.play(-1)
            
    def stop_music(self):
        """Stop the main theme music"""
        if self.main_theme:
            self.main_theme.stop()
            
    def reset_game(self):
        self.game_state = MENU
        self.stop_music()
        self.clear_level()
        
    def load_level(self, level_index):
        if level_index >= len(LEVELS):
            self.game_state = GAME_WIN
            return
            
        level_data = LEVELS[level_index]
        
        # Clear existing level objects
        self.clear_level()
        
        # Set camera level dimensions
        self.camera.set_level_dimensions(level_data.get('level_width', 2000))
        
        # Load platforms (tuple format: x, y, width, height)
        for platform_data in level_data.get('platforms', []):
            if len(platform_data) == 4:  # Tuple format
                x, y, width, height = platform_data
                platform = Platform(x, y, width, height)
                self.platforms.add(platform)
                self.all_sprites.add(platform)
        
        # Load enemies (tuple format: x, y, direction, enemy_type)
        for enemy_data in level_data.get('enemies', []):
            if len(enemy_data) == 4:  # Tuple format with enemy type
                x, y, direction, enemy_type = enemy_data
            elif len(enemy_data) == 3:  # Tuple format without enemy type
                x, y, direction = enemy_data
                enemy_type = "goomba"
            elif len(enemy_data) == 2:  # Tuple format without direction
                x, y = enemy_data
                direction = "left"
                enemy_type = "goomba"
            else:
                continue
                
            enemy = Enemy(x, y, direction, enemy_type)
            enemy.collision_system = self.collision_system  # Connect collision system
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        # Load coins (tuple format: x, y)
        for coin_data in level_data.get('coins', []):
            if len(coin_data) == 2:  # Tuple format
                x, y = coin_data
                coin = Coin(x, y)
                self.coins.add(coin)
                self.all_sprites.add(coin)
        
        # Load jumping blocks (tuple format: x, y, block_type, content_type)
        for block_data in level_data.get('jumping_blocks', []):
            if len(block_data) == 4:  # Tuple format with content type
                x, y, block_type, content_type = block_data
                block = JumpingBlock(x, y, block_type, content_type)
            elif len(block_data) == 3:  # Tuple format without content type
                x, y, block_type = block_data
                block = JumpingBlock(x, y, block_type)
            elif len(block_data) == 2:  # Tuple format without block type
                x, y = block_data
                block = JumpingBlock(x, y)
            else:
                continue
                
            block.reset_points()  # Reset points for new level
            self.jumping_blocks.add(block)
            self.all_sprites.add(block)
        
        # Load pipes (tuple format: x, y, height, pipe_type)
        for pipe_data in level_data.get('pipes', []):
            if len(pipe_data) == 4:  # Tuple format with pipe type
                x, y, height, pipe_type = pipe_data
                pipe = Pipe(x, y, height, pipe_type)
            elif len(pipe_data) == 3:  # Tuple format without pipe type
                x, y, height = pipe_data
                pipe = Pipe(x, y, height)
            elif len(pipe_data) == 2:  # Tuple format without height
                x, y = pipe_data
                pipe = Pipe(x, y)
            else:
                continue
                
            self.pipes.add(pipe)
            self.all_sprites.add(pipe)
        
        # Load power-ups (tuple format: x, y, powerup_type)
        for powerup_data in level_data.get('powerups', []):
            if len(powerup_data) == 3:  # Tuple format
                x, y, powerup_type = powerup_data
                powerup = PowerUp(x, y, powerup_type)
                self.powerups.add(powerup)
                self.all_sprites.add(powerup)
        
        # Load flag (tuple format: x, y)
        if 'flag_position' in level_data:
            flag_data = level_data['flag_position']
            if len(flag_data) == 2:  # Tuple format
                x, y = flag_data
                flag = Flag(x, y)
                self.flags.add(flag)
                self.all_sprites.add(flag)
        
        # Reset player to beginning of level
        self.player.reset(100, 300)
            
    def clear_level(self):
        # Remove all sprites except player and ground
        for sprite in list(self.all_sprites):
            if sprite != self.player and sprite != self.ground:
                sprite.kill()
                
    def next_level(self):
        self.current_level += 1
        if self.current_level < len(LEVELS):
            self.load_level(self.current_level)
            self.game_state = PLAYING
        else:
            self.game_state = GAME_WIN
            self.stop_music()
            
    def update(self):
        if self.game_state == PLAYING:
            # Update camera
            self.camera.update(self.player)
            
            # Update all sprites with new collision system
            self.player.update(self.platforms, self.jumping_blocks, self.pipes, self.enemies)
            self.enemies.update(self.platforms)
            self.coins.update()
            self.jumping_blocks.update()
            self.flags.update()  # Update flags for animation
            self.powerups.update()  # Update power-ups
            
            # Check coin collection using new collision system
            collected_coins = self.collision_system.check_coin_collisions(self.player, self.coins)
            for coin in collected_coins:
                coin.kill()
                self.score += 10
                if self.coin_sound:
                    self.coin_sound.play()
                
            # Check jumping block collision using new collision detection system
            for block in self.jumping_blocks:
                if block.check_collision_from_below(self.player):
                    block.hit()
                    # Get points from block (200 points, only once per block)
                    points_earned = block.get_points()
                    self.score += points_earned
                    
                    # Get content from block
                    content = block.get_content()
                    if content:
                        if content == "coin":
                            self.score += 10
                            if self.coin_sound:
                                self.coin_sound.play()
                        elif content in ["mushroom", "star"]:
                            # Create power-up at block position
                            powerup = PowerUp(block.rect.centerx, block.rect.top, content)
                            self.powerups.add(powerup)
                            self.all_sprites.add(powerup)
                    
                    # Add floating score text if points were earned
                    if points_earned > 0:
                        score_text = f"+{points_earned}"
                        self.floating_scores.append((score_text, block.rect.centerx, block.rect.top, 60))
                    
                    # Add camera shake when hitting blocks
                    self.camera.shake_camera(3, 8)
                    if self.block_hit_sound:
                        self.block_hit_sound.play()
                
            # Check power-up collection
            for powerup in self.powerups:
                if self.player.rect.colliderect(powerup.rect):
                    powerup.collect()
                    self.player.apply_powerup(powerup.powerup_type)
                    self.score += powerup.points
                    powerup.kill()
                
            # Check enemy collision using new collision system
            enemy_collision_result = self.collision_system.check_enemy_collisions(self.player, self.enemies)
            if enemy_collision_result == "player_hit":
                if self.player.take_damage():
                    self.lives -= 1
                    # Add camera shake when player takes damage
                    self.camera.shake_camera(5, 10)
                    if self.lives <= 0:
                        self.game_state = GAME_OVER
                        self.stop_music()
                        if self.game_over_sound:
                            self.game_over_sound.play()
                    else:
                        self.player.reset(100, 300)
            elif enemy_collision_result == "enemy_killed":
                self.score += 20
                # Add small camera shake when enemy is killed
                self.camera.shake_camera(2, 5)
                    
            # Check if player fell off screen
            if self.player.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                # Add camera shake when player falls
                self.camera.shake_camera(8, 15)
                if self.lives <= 0:
                    self.game_state = GAME_OVER
                    self.stop_music()
                    if self.game_over_sound:
                        self.game_over_sound.play()
                else:
                    self.player.reset(100, 300)
                    
            # Check if level is complete using new collision system
            flag_collision = False
            
            # Check flag collision using new flag method
            for flag in self.flags:
                if flag.check_collision(self.player):
                    flag.reach_flag()
                    flag_collision = True
                    break
            
            if flag_collision:
                # Add camera shake when completing level
                self.camera.shake_camera(10, 20)
                if self.level_complete_sound:
                    self.level_complete_sound.play()
                self.game_state = LEVEL_COMPLETE
                self.level_complete_timer = self.level_complete_duration
                
            # Update floating scores
            self.floating_scores = [(text, x, y - 1, timer - 1) for text, x, y, timer in self.floating_scores if timer > 0]
        
        elif self.game_state == LEVEL_COMPLETE:
            self.level_complete_timer -= 1
            if self.level_complete_timer <= 0:
                self.next_level()
                
    def draw(self):
        # Get current level background color
        if self.game_state == PLAYING and self.current_level < len(LEVELS):
            background_color = LEVELS[self.current_level].get('background_color', BLUE)
        else:
            background_color = BLUE
        
        # Clear screen with level background color
        self.screen.fill(background_color)
        
        # Draw background pattern for scrolling levels
        if self.game_state == PLAYING:
            self.draw_background_pattern()
        
        # Draw background if available
        if self.background:
            bg_rect = self.background.get_rect()
            bg_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(self.background, bg_rect)
            
        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == PAUSED:
            self.draw_game()
            self.draw_pause_screen()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        elif self.game_state == LEVEL_COMPLETE:
            self.draw_game()
            self.draw_level_complete()
        elif self.game_state == GAME_WIN:
            self.draw_game_win()
            
        # Update display
        pygame.display.flip()
            
    def draw_menu(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(UI_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        title = self.font.render("SUPER MARIO ENHANCED", True, UI_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)
        
        subtitle = self.small_font.render("5 Levels of Adventure!", True, UI_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(subtitle, subtitle_rect)
        
        instruction = self.small_font.render("Press SPACE to start", True, UI_COLOR)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(instruction, instruction_rect)
        
        controls = self.small_font.render("Controls: Arrow Keys/WASD to move, SPACE to jump", True, UI_COLOR)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(controls, controls_rect)
        
        pause_info = self.small_font.render("P to pause, F1 for debug mode", True, UI_COLOR)
        pause_rect = pause_info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(pause_info, pause_rect)
        
    def draw_game(self):
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            # Special handling for sprites with custom draw methods
            if hasattr(sprite, 'draw') and callable(sprite.draw):
                sprite.draw(self.screen, self.camera)
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # Draw debug collision boxes if enabled
        if self.collision_system.debug_mode:
            self.collision_system.draw_debug_collisions(
                self.screen, self.player, self.platforms, self.enemies, self.coins
            )
        
        # Draw camera debug info
        self.camera.draw_debug_info(self.screen)
        
        # Draw UI (not affected by camera)
        self.draw_ui()
        
        # Draw floating scores
        for text, x, y, timer in self.floating_scores:
            # Calculate alpha based on timer
            alpha = min(255, timer * 4)
            score_surface = self.small_font.render(text, True, (255, 255, 0))
            score_surface.set_alpha(alpha)
            score_rect = score_surface.get_rect(center=(x, y))
            self.screen.blit(score_surface, score_rect)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, UI_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, UI_COLOR)
        self.screen.blit(lives_text, (10, 50))
        
        # Level
        level_text = self.font.render(f"Level: {self.current_level + 1}/5", True, UI_COLOR)
        self.screen.blit(level_text, (10, 90))
        
        # Power-up status
        if self.player.powerup_state != "normal":
            powerup_text = self.small_font.render(f"Power: {self.player.powerup_state.upper()}", True, (255, 255, 0))
            self.screen.blit(powerup_text, (10, 130))
        
        # Debug info
        if self.collision_system.debug_mode:
            debug_text = self.small_font.render("DEBUG MODE: F1 to toggle", True, (255, 255, 0))
            self.screen.blit(debug_text, (10, SCREEN_HEIGHT - 30))
    
    def draw_pause_screen(self):
        """Draw pause screen overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(UI_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, UI_COLOR)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, pause_rect)
        
        resume_text = self.small_font.render("Press P to resume", True, UI_COLOR)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(resume_text, resume_rect)
        
    def draw_game_over(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(UI_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, UI_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.small_font.render("Press R to restart", True, UI_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_level_complete(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(UI_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        complete_text = self.font.render("LEVEL COMPLETE!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(complete_text, complete_rect)
        
        score_text = self.font.render(f"Score: {self.score}", True, UI_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        next_text = self.small_font.render("Loading next level...", True, UI_COLOR)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(next_text, next_rect)
    
    def draw_game_win(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(UI_BACKGROUND_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        win_text = self.font.render("CONGRATULATIONS!", True, GOLD)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(win_text, win_rect)
        
        subtitle = self.font.render("You've completed all levels!", True, UI_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(subtitle, subtitle_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, UI_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.small_font.render("Press R to play again", True, UI_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_background_pattern(self):
        # Draw a simple background pattern for scrolling levels
        for x in range(0, SCREEN_WIDTH + 100, 100):
            for y in range(0, SCREEN_HEIGHT + 100, 100):
                pygame.draw.circle(self.screen, (200, 200, 255), (x, y), 2) 