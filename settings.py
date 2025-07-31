# Enhanced Mario Game Settings
import pygame

# Screen settings
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Player settings
PLAYER_WIDTH = 45
PLAYER_HEIGHT = 45
PLAYER_SPEED = 6
PLAYER_JUMP_SPEED = -20
GRAVITY = 0.9
MAX_FALL_SPEED = 25

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 2.0
ENEMY_JUMP_SPEED = -15

# Power-up settings
POWERUP_SIZE = 40
POWERUP_DURATION = 5000  # 5 seconds in milliseconds

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
LEVEL_COMPLETE = "level_complete"
GAME_WIN = "game_win"
PAUSED = "paused"

# Enhanced 5-level design with progressive difficulty
LEVELS = [
    {
        "name": "Level 1 - Mushroom Kingdom",
        "background_color": (135, 206, 235),  # Sky blue
        "platforms": [
            # Ground platforms - varied sizes and positions
            (100, 550, 180, 40),   # Starting platform (large)
            (350, 480, 120, 30),   # First jump platform (medium)
            (550, 420, 80, 30),    # Second jump platform (small)
            (720, 350, 150, 30),   # Third jump platform (large)
            (950, 280, 100, 30),   # Fourth jump platform (medium)
            (1130, 200, 60, 30),   # Fifth jump platform (tiny)
            (1280, 320, 140, 30),  # Sixth jump platform (large)
            (1500, 250, 90, 30),   # Seventh jump platform (medium)
            (1670, 180, 70, 30),   # Eighth jump platform (small)
            (1820, 300, 130, 30),  # Ninth jump platform (large)
            (1980, 150, 50, 30),   # Tenth jump platform (tiny)
            (2100, 400, 160, 30),  # Eleventh jump platform (large)
            (2300, 550, 120, 40),  # Final platform near flag (medium)
        ],
        "enemies": [
            (200, 430, "right", "koopa"),    # On first platform
            (420, 330, "left", "goomba"),    # On second platform
            (590, 270, "right", "koopa"),    # On third platform
            (800, 230, "left", "goomba"),    # On fourth platform
            (1000, 150, "right", "koopa"),   # On fifth platform
            (1160, 150, "left", "goomba"),   # On sixth platform
            (1350, 270, "right", "koopa"),   # On seventh platform
            (1550, 200, "left", "goomba"),   # On eighth platform
            (1705, 130, "right", "koopa"),   # On ninth platform
            (1890, 250, "left", "goomba"),   # On tenth platform
            (2005, 100, "right", "koopa"),   # On eleventh platform
        ],
        "coins": [
            (190, 430),  # On first platform
            (410, 330),  # On second platform
            (590, 270),  # On third platform
            (800, 230),  # On fourth platform
            (1000, 150), # On fifth platform
            (1160, 150), # On sixth platform
            (1350, 270), # On seventh platform
            (1545, 200), # On eighth platform
            (1705, 130), # On ninth platform
            (1885, 250), # On tenth platform
            (2025, 100), # On eleventh platform
            (2360, 450), # Near flag
        ],
        "jumping_blocks": [
            # Positioned above platforms for hitting from underneath
            (350, 430, "single", "coin"),    # Above first platform
            (550, 330, "double", "powerup"), # Above second platform
            (720, 270, "single", "coin"),    # Above third platform
            (950, 230, "triple", "powerup"), # Above fourth platform
            (1130, 150, "single", "coin"),   # Above fifth platform
            (1280, 270, "double", "powerup"), # Above sixth platform
            (1500, 200, "single", "coin"),   # Above seventh platform
            (1670, 130, "triple", "powerup"), # Above eighth platform
            (1820, 250, "single", "coin"),   # Above ninth platform
            (1980, 100, "double", "powerup"), # Above tenth platform
            (2100, 350, "single", "coin"),   # Above eleventh platform
            # Floating blocks for extra challenge
            (450, 350, "double", "coin"),    # Between platforms
            (650, 280, "single", "powerup"), # Between platforms
            (850, 200, "triple", "coin"),    # Between platforms
            (1050, 120, "double", "powerup"), # Between platforms
            (1250, 220, "single", "coin"),   # Between platforms
            (1450, 150, "triple", "powerup"), # Between platforms
            (1650, 80, "double", "coin"),    # Between platforms
            (1850, 200, "single", "powerup"), # Between platforms
        ],
        "pipes": [
            (300, 550, 120, "normal"),   # Tall pipe
            (700, 550, 80, "normal"),    # Medium pipe
            (1100, 550, 150, "normal"),  # Very tall pipe
            (1500, 550, 100, "normal"),  # Tall pipe
            (1900, 550, 60, "normal"),   # Short pipe
        ],
        "powerups": [
            (575, 400, "mushroom"),
        ],
        "flag_position": (2300, 450),
        "level_width": 2500
    },
    {
        "name": "Level 2 - Underground Caverns",
        "background_color": (25, 25, 50),  # Dark blue
        "platforms": [
            # Ground platforms - varied sizes and interesting positions
            (100, 550, 160, 40),   # Starting platform (large)
            (320, 470, 100, 30),   # First jump platform (medium)
            (500, 380, 60, 30),    # Second jump platform (small)
            (640, 290, 140, 30),   # Third jump platform (large)
            (860, 200, 80, 30),    # Fourth jump platform (medium)
            (1020, 320, 120, 30),  # Fifth jump platform (large)
            (1220, 240, 70, 30),   # Sixth jump platform (small)
            (1370, 150, 110, 30),  # Seventh jump platform (medium)
            (1560, 280, 90, 30),   # Eighth jump platform (medium)
            (1730, 190, 50, 30),   # Ninth jump platform (tiny)
            (1900, 310, 130, 30),  # Tenth jump platform (large)
            (2080, 220, 75, 30),   # Eleventh jump platform (small)
            (2320, 550, 100, 40),  # Final platform (medium)
        ],
        "enemies": [
            (180, 430, "right", "koopa"),    # On first platform
            (370, 330, "left", "goomba"),    # On second platform
            (530, 240, "right", "koopa"),    # On third platform
            (710, 150, "left", "goomba"),    # On fourth platform
            (900, 270, "right", "koopa"),    # On fifth platform
            (1260, 200, "left", "goomba"),   # On sixth platform
            (1415, 110, "right", "koopa"),   # On seventh platform
            (1615, 240, "left", "goomba"),   # On eighth platform
            (1775, 150, "right", "koopa"),   # On ninth platform
            (1965, 270, "left", "goomba"),   # On tenth platform
            (2115, 180, "right", "koopa"),   # On eleventh platform
        ],
        "coins": [
            (345, 430),
            (545, 360),
            (745, 290),
            (945, 220),
            (1145, 150),
            (1345, 80),
            (1545, 10),
            (1745, -60),
            (1945, -130),
            (2145, -200),
            (2370, 450),
        ],
        "jumping_blocks": [
            # Positioned above platforms
            (320, 430, "double", "coin"),
            (520, 360, "single", "powerup"),
            (720, 290, "triple", "coin"),
            (920, 220, "double", "powerup"),
            (1120, 150, "single", "coin"),
            (1320, 80, "triple", "powerup"),
            (1520, 10, "double", "coin"),
            (1720, -60, "single", "powerup"),
            (1920, -130, "triple", "coin"),
            (2120, -200, "double", "powerup"),
            # Floating blocks
            (420, 330, "single", "coin"),
            (620, 260, "double", "powerup"),
            (820, 190, "triple", "coin"),
            (1020, 120, "single", "powerup"),
            (1220, 50, "double", "coin"),
            (1420, -20, "triple", "powerup"),
            (1620, -90, "single", "coin"),
            (1820, -160, "double", "powerup"),
            (2020, -230, "triple", "coin"),
        ],
        "pipes": [
            (400, 550, 140, "warp"),     # Tall warp pipe
            (800, 550, 90, "normal"),    # Medium pipe
            (1200, 550, 180, "fire"),    # Very tall fire pipe
            (1600, 550, 110, "normal"),  # Tall pipe
            (2000, 550, 70, "warp"),     # Short warp pipe
        ],
        "powerups": [
            (545, 360, "star"),
        ],
        "flag_position": (2500, 450),
        "level_width": 2700
    },
    {
        "name": "Level 3 - Sky Castle",
        "background_color": (70, 130, 180),  # Steel blue
        "platforms": [
            # Ground platforms - sky castle theme with floating platforms
            (100, 550, 100, 40),
            (300, 470, 80, 30),
            (480, 390, 80, 30),
            (660, 310, 80, 30),
            (840, 230, 80, 30),
            (1020, 150, 80, 30),
            (1200, 70, 80, 30),
            (1380, -10, 80, 30),
            (1560, -90, 80, 30),
            (1740, -170, 80, 30),
            (1920, -250, 80, 30),
            (2100, -330, 80, 30),
            (2280, 550, 120, 40),  # Final platform
        ],
        "enemies": [
            (320, 420, "left", "koopa"),     # On first platform
            (500, 340, "right", "goomba"),   # On second platform
            (680, 260, "left", "koopa"),     # On third platform
            (860, 180, "right", "goomba"),   # On fourth platform
            (1040, 100, "left", "koopa"),    # On fifth platform
            (1220, 20, "right", "goomba"),   # On sixth platform
            (1400, -60, "left", "koopa"),    # On seventh platform
            (1580, -140, "right", "goomba"), # On eighth platform
            (1760, -220, "left", "koopa"),   # On ninth platform
            (1940, -300, "right", "goomba"), # On tenth platform
            (2120, -380, "left", "koopa"),   # On eleventh platform
        ],
        "coins": [
            (325, 420),
            (505, 340),
            (685, 260),
            (865, 180),
            (1045, 100),
            (1225, 20),
            (1405, -60),
            (1585, -140),
            (1765, -220),
            (1945, -300),
            (2125, -380),
            (2330, 450),
        ],
        "jumping_blocks": [
            # Positioned above platforms
            (300, 420, "triple", "coin"),
            (480, 340, "single", "powerup"),
            (660, 260, "double", "coin"),
            (840, 180, "triple", "powerup"),
            (1020, 100, "single", "coin"),
            (1200, 20, "double", "powerup"),
            (1380, -60, "triple", "coin"),
            (1560, -140, "single", "powerup"),
            (1740, -220, "double", "coin"),
            (1920, -300, "triple", "powerup"),
            (2100, -380, "single", "coin"),
            # Floating blocks
            (390, 270, "single", "coin"),
            (570, 190, "double", "powerup"),
            (750, 110, "triple", "coin"),
            (930, 30, "single", "powerup"),
            (1110, -50, "double", "coin"),
            (1290, -130, "triple", "powerup"),
            (1470, -210, "single", "coin"),
            (1650, -290, "double", "powerup"),
            (1830, -370, "triple", "coin"),
            (2010, -450, "single", "powerup"),
        ],
        "pipes": [
            (400, 550, 160, "fire"),     # Very tall fire pipe
            (800, 550, 85, "normal"),    # Medium pipe
            (1200, 550, 200, "warp"),    # Extremely tall warp pipe
            (1600, 550, 95, "normal"),   # Medium pipe
            (2000, 550, 130, "fire"),    # Tall fire pipe
        ],
        "powerups": [
            (505, 340, "mushroom"),
            (1225, 20, "star"),
        ],
        "flag_position": (2450, 450),
        "level_width": 2600
    },
    {
        "name": "Level 4 - Bowser's Castle",
        "background_color": (25, 25, 25),  # Dark gray
        "platforms": [
            # Ground platforms - challenging castle layout
            (100, 550, 80, 40),
            (280, 460, 70, 30),
            (450, 370, 70, 30),
            (620, 280, 70, 30),
            (790, 190, 70, 30),
            (960, 100, 70, 30),
            (1130, 10, 70, 30),
            (1300, -80, 70, 30),
            (1470, -170, 70, 30),
            (1640, -260, 70, 30),
            (1810, -350, 70, 30),
            (1980, -440, 70, 30),
            (2150, -530, 70, 30),
            (2320, 550, 100, 40),  # Final platform
        ],
        "enemies": [
            (300, 410, "right", "koopa"),    # On first platform
            (470, 320, "left", "goomba"),    # On second platform
            (640, 230, "right", "koopa"),    # On third platform
            (810, 140, "left", "goomba"),    # On fourth platform
            (980, 50, "right", "koopa"),     # On fifth platform
            (1150, -40, "left", "goomba"),   # On sixth platform
            (1320, -130, "right", "koopa"),  # On seventh platform
            (1490, -220, "left", "goomba"),  # On eighth platform
            (1660, -310, "right", "koopa"),  # On ninth platform
            (1830, -400, "left", "goomba"),  # On tenth platform
            (2000, -490, "right", "koopa"),  # On eleventh platform
            (2170, -580, "left", "goomba"),  # On twelfth platform
        ],
        "coins": [
            (305, 410),
            (475, 320),
            (645, 230),
            (815, 140),
            (985, 50),
            (1155, -40),
            (1325, -130),
            (1495, -220),
            (1665, -310),
            (1835, -400),
            (2005, -490),
            (2175, -580),
            (2370, 450),
        ],
        "jumping_blocks": [
            # Positioned above platforms
            (280, 410, "double", "coin"),
            (450, 320, "triple", "powerup"),
            (620, 230, "single", "coin"),
            (790, 140, "double", "powerup"),
            (960, 50, "triple", "coin"),
            (1130, -40, "single", "powerup"),
            (1300, -130, "double", "coin"),
            (1470, -220, "triple", "powerup"),
            (1640, -310, "single", "coin"),
            (1810, -400, "double", "powerup"),
            (1980, -490, "triple", "coin"),
            (2150, -580, "single", "powerup"),
            # Floating blocks
            (365, 200, "single", "coin"),
            (535, 110, "double", "powerup"),
            (705, 20, "triple", "coin"),
            (875, -70, "single", "powerup"),
            (1045, -160, "double", "coin"),
            (1215, -250, "triple", "powerup"),
            (1385, -340, "single", "coin"),
            (1555, -430, "double", "powerup"),
            (1725, -520, "triple", "coin"),
            (1895, -610, "single", "powerup"),
        ],
        "pipes": [
            (400, 550, 170, "warp"),     # Very tall warp pipe
            (800, 550, 75, "normal"),    # Short pipe
            (1200, 550, 220, "fire"),    # Extremely tall fire pipe
            (1600, 550, 105, "normal"),  # Medium pipe
            (2000, 550, 140, "warp"),    # Tall warp pipe
            (2400, 550, 90, "normal"),   # Medium pipe
        ],
        "powerups": [
            (475, 320, "star"),
            (985, 50, "mushroom"),
            (1495, -220, "star"),
        ],
        "flag_position": (2500, 450),
        "level_width": 2700
    },
    {
        "name": "Level 5 - Final Challenge",
        "background_color": (75, 0, 130),  # Indigo
        "platforms": [
            # Ground platforms - ultimate challenge
            (100, 550, 70, 40),
            (270, 440, 60, 30),
            (430, 330, 60, 30),
            (590, 220, 60, 30),
            (750, 110, 60, 30),
            (910, 0, 60, 30),
            (1070, -110, 60, 30),
            (1230, -220, 60, 30),
            (1390, -330, 60, 30),
            (1550, -440, 60, 30),
            (1710, -550, 60, 30),
            (1870, -660, 60, 30),
            (2030, -770, 60, 30),
            (2190, -880, 60, 30),
            (2350, 550, 80, 40),  # Final platform
        ],
        "enemies": [
            (290, 390, "left", "koopa"),     # On first platform
            (450, 280, "right", "goomba"),   # On second platform
            (610, 170, "left", "koopa"),     # On third platform
            (770, 60, "right", "goomba"),    # On fourth platform
            (930, -50, "left", "koopa"),     # On fifth platform
            (1090, -160, "right", "goomba"), # On sixth platform
            (1250, -270, "left", "koopa"),   # On seventh platform
            (1410, -380, "right", "goomba"), # On eighth platform
            (1570, -490, "left", "koopa"),   # On ninth platform
            (1730, -600, "right", "goomba"), # On tenth platform
            (1890, -710, "left", "koopa"),   # On eleventh platform
            (2050, -820, "right", "goomba"), # On twelfth platform
            (2210, -930, "left", "koopa"),   # On thirteenth platform
        ],
        "coins": [
            (295, 390),
            (455, 280),
            (615, 170),
            (775, 60),
            (935, -50),
            (1095, -160),
            (1255, -270),
            (1415, -380),
            (1575, -490),
            (1735, -600),
            (1895, -710),
            (2055, -820),
            (2215, -930),
            (2400, 450),
        ],
        "jumping_blocks": [
            # Positioned above platforms
            (270, 390, "triple", "coin"),
            (430, 280, "single", "powerup"),
            (590, 170, "double", "coin"),
            (750, 60, "triple", "powerup"),
            (910, -50, "single", "coin"),
            (1070, -160, "double", "powerup"),
            (1230, -270, "triple", "coin"),
            (1390, -380, "single", "powerup"),
            (1550, -490, "double", "coin"),
            (1710, -600, "triple", "powerup"),
            (1870, -710, "single", "coin"),
            (2030, -820, "double", "powerup"),
            (2190, -930, "triple", "coin"),
            # Floating blocks
            (355, 170, "single", "coin"),
            (515, 60, "double", "powerup"),
            (675, -50, "triple", "coin"),
            (835, -160, "single", "powerup"),
            (995, -270, "double", "coin"),
            (1155, -380, "triple", "powerup"),
            (1315, -490, "single", "coin"),
            (1475, -600, "double", "powerup"),
            (1635, -710, "triple", "coin"),
            (1795, -820, "single", "powerup"),
            (1955, -930, "double", "coin"),
        ],
        "pipes": [
            (400, 550, 180, "fire"),     # Very tall fire pipe
            (800, 550, 65, "normal"),    # Short pipe
            (1200, 550, 240, "warp"),    # Extremely tall warp pipe
            (1600, 550, 115, "normal"),  # Medium pipe
            (2000, 550, 150, "fire"),    # Tall fire pipe
            (2400, 550, 85, "warp"),     # Medium warp pipe
        ],
        "powerups": [
            (455, 280, "star"),
            (775, 60, "mushroom"),
            (1095, -160, "star"),
            (1415, -380, "mushroom"),
            (1735, -600, "star"),
        ],
        "flag_position": (2550, 450),
        "level_width": 2800
    }
]

# Power-up types
POWERUP_TYPES = {
    "mushroom": {
        "color": RED,
        "effect": "grow",
        "duration": 15000,
        "points": 1000
    },
    "star": {
        "color": GOLD,
        "effect": "invincible",
        "duration": 4000,
        "points": 2000
    }
}

# Sound effects
SOUND_EFFECTS = {
    "jump": "assets/sounds/jump.wav",
    "coin": "assets/sounds/coin.wav",
    "powerup": "assets/sounds/powerup.wav",
    "enemy_hit": "assets/sounds/enemy_hit.wav",
    "block_hit": "assets/sounds/block_hit.wav",
    "level_complete": "assets/sounds/level_complete.wav",
    "game_over": "assets/sounds/game_over.wav",
    "main_theme": "assets/sounds/main_theme.ogg"
}

# Animation settings
ANIMATION_SPEED = 0.15
JIGGLE_INTENSITY = 15
JIGGLE_DECAY = 0.85
JIGGLE_SPEED = 0.6

# Camera settings
CAMERA_SMOOTHNESS = 0.1
CAMERA_SHAKE_DECAY = 0.9
CAMERA_ZOOM_SPEED = 0.05

# Particle effects
PARTICLE_COUNT = 20
PARTICLE_LIFETIME = 60
PARTICLE_SPEED = 3

# UI settings
UI_FONT_SIZE = 36
UI_SMALL_FONT_SIZE = 24
UI_COLOR = WHITE
UI_BACKGROUND_ALPHA = 128 