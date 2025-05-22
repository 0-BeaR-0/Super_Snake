# settings.py

# Configuration settings for the Snake game

# Display settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Speed settings
BASE_FPS = 8  # Slower initial speed
BOOSTED_FPS = 12  # Moderate boost
MAX_FPS = 20  # Maximum speed cap
SPEED_INCREMENT = 0.2  # Speed increase per food eaten

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Game settings
SPEED_BOOST_DURATION = 5  # Duration of speed boost in seconds
ENEMY_SPEED = 5  # Speed of the enemy
FONT_SIZE = 36  # Default font size for text display
MENU_FONT_SIZE = 72  # Font size for menu title

# Visual settings
BACKGROUND_COLOR = BLACK
SNAKE_HEAD_COLOR = GREEN
SNAKE_BODY_COLOR = (50, 200, 50)
GRID_LINE_COLOR = (30, 30, 30)

# Food types and their properties
FOOD_TYPES = {
    'normal': {'color': RED, 'points': 1, 'effect': None},
    'boost': {'color': YELLOW, 'points': 2, 'effect': 'speed'},
    'special': {'color': PURPLE, 'points': 3, 'effect': 'grow'},
}

# Enemy settings
ENEMY_COLOR = BLUE
ENEMY_SIZE = GRID_SIZE

# Menu settings
MENU_BACKGROUND = BLACK
MENU_TEXT_COLOR = WHITE
MENU_HIGHLIGHT_COLOR = GREEN