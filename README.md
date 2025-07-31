# Super Mario Game

**Version 1.0.1** - A complete Mario platformer game built with Pygame featuring 5 levels, enemies, collectibles, sound effects, and smooth animations.

## Features

- **5 Complete Levels**: Each with increasing difficulty and varied platform layouts
- **Mario Sprites**: Animated running, jumping, and idle states
- **Advanced Enemy AI**: Koopa and Goomba enemies with varied behaviors
- **Collectibles**: Coins to collect for points
- **Complete Sound System**: Jump sound, background music, and all game effects
- **Power-up System**: Mushrooms and stars with special effects
- **Jumping Blocks**: Interactive blocks with jiggle effects and rewards
- **Varied Platforms**: Different sizes and challenging layouts
- **Lives System**: 3 lives with respawn mechanics
- **Score System**: Points for collecting coins and hitting blocks
- **Smooth Controls**: Responsive movement and jumping
- **Camera System**: Advanced camera with smooth following and effects

## Controls

- **Movement**: Arrow Keys or WASD
- **Jump**: Spacebar, Up Arrow, or W
- **Start Game**: Spacebar (from menu)
- **Restart**: R (after game over)

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

```bash
python main.py
```

## Game Structure

The game is organized into separate modules:

- `main.py` - Main game loop and initialization
- `game.py` - Core game logic and state management
- `player.py` - Mario player class with animations
- `enemy.py` - Koopa enemy AI
- `platform.py` - Level geometry (platforms and ground)
- `coin.py` - Collectible coins
- `settings.py` - Game constants and configurations

## Assets Used

- Mario sprites (idle, run animations, jump, death)
- Koopa enemy sprite
- Cloud background
- Jump sound effect
- Background music

## Game Mechanics

- **Platforming**: Jump between platforms to reach coins
- **Enemy Avoidance**: Avoid or jump on Koopa enemies
- **Level Progression**: Complete levels by collecting all coins
- **Lives System**: Lose lives when touching enemies or falling off screen
- **Scoring**: Earn points by collecting coins

Enjoy the game! 