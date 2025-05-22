# Snake Game

## Overview
This is an advanced version of the classic Snake game, featuring modern gameplay mechanics including shooting, ammo collection, dynamic enemy AI, special power-ups, and enhanced visual effects.

## Features
- **Combat System**: 
  - Shoot bullets to defend against enemies
  - Collect ammo pickups to replenish your shooting ability
  - Bullets can temporarily disable enemies
- **Dynamic Enemy AI**: 
  - Intelligent enemy that pursues both the snake and food
  - Enemy grows stronger by consuming food
  - Adaptive behavior that increases challenge over time
- **Enhanced Gameplay Mechanics**:
  - Gradual speed progression system
  - Multiple types of food with different effects
  - Speed boosters for temporary advantage
  - Score multipliers and bonus points
- **Visual Effects**:
  - Gradient and glow effects
  - Pulsing animations for pickups
  - Dynamic grid with fade effects
  - Particle effects for collisions
- **Modern UI**:
  - Clean, intuitive menu system
  - Real-time HUD with score and ammo display
  - Custom fonts for better visual appeal
  - Pause functionality

## Project Structure
```
snake-game
├── src
│   ├── assets
│   │   └── fonts
│   │       └── game_font.ttf
│   ├── components
│   │   ├── enemy.py
│   │   ├── food.py
│   │   ├── menu.py
│   │   └── snake.py
│   ├── config
│   │   └── settings.py
│   ├── utils
│   │   ├── collision.py
│   │   └── display.py
│   └── main.py
├── tests
│   └── test_game.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd snake-game
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To start the game, run the following command:
```
python src/main.py
```

## Controls
### Movement
- **Arrow Keys** or **WASD**: Control the snake's direction
  - ↑ or W: Move up
  - ↓ or S: Move down
  - ← or A: Move left
  - → or D: Move right

### Combat
- **SPACE**: Fire a bullet in the current direction
- Collect ammo pickups (marked with a cross symbol) to replenish bullets

### Game Control
- **ESC**: Pause/Resume game
- **SPACE**: Start game (when in menu)
- **ESC**: Return to menu (when game is over)

## Gameplay Tips
1. **Resource Management**:
   - Monitor your ammo count carefully
   - Use bullets strategically to defend against the enemy
   - Collect ammo pickups whenever possible

2. **Scoring System**:
   - Regular food: 1 point
   - Hitting enemy with bullet: 5 bonus points
   - Special food items give extra points and effects

3. **Enemy Behavior**:
   - The enemy will chase both you and food
   - Enemy becomes larger and faster as it consumes food
   - Use bullets to temporarily disable the enemy

4. **Power-ups and Effects**:
   - Speed boosters (blue food): Temporarily increase movement speed
   - Growth power-ups (special food): Add multiple segments at once
   - Various other special effects from different food types

## Testing
To run the unit tests, execute:
```
python -m unittest discover -s tests
```

## License
This project is licensed under the MIT License.