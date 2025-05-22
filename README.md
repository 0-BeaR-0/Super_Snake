# Snake Game

## Overview
This is an advanced version of the classic Snake game, featuring an enhanced menu, improved text display, speed boosters, different types of food, and an enemy.

## Features
- **Enhanced Menu**: A user-friendly menu that allows players to start the game, view instructions, and exit.
- **Improved Text Display**: Custom fonts for better visual appeal.
- **Speed Boosters**: Special food items that temporarily increase the snake's speed.
- **Different Types of Food**: Various food items that provide different effects.
- **Enemy**: An enemy that moves around the screen, adding an extra challenge to the game.

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
- Use the arrow keys or WASD to control the snake.
- Press SPACE to start the game from the menu.
- Press P to pause and resume the game.

## Testing
To run the unit tests, execute:
```
python -m unittest discover -s tests
```

## License
This project is licensed under the MIT License.