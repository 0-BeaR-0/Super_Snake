import pygame
import random
import time
from src.config.settings import (
    GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR,
    BASE_FPS, BOOSTED_FPS, SPEED_BOOST_DURATION,
    MAX_FPS, SPEED_INCREMENT
)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset snake to initial state"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.base_speed = BASE_FPS  # Store base speed separately
        self.speed = self.base_speed
        self.speed_boost_end = 0
        self.score = 0
        self.food_eaten = 0  # Track food eaten for speed progression
        self.is_boosted = False
        self.ammo_count = 0  # Initialize ammo count
        self.growth_queue = 0  # Track pending growth segments
        
    @property
    def head(self):
        """Get the snake's head position"""
        return self.positions[0]
    
    def turn(self, direction):
        """Change snake's direction if valid"""
        opposites = {
            'left': 'right',
            'right': 'left',
            'up': 'down',
            'down': 'up'
        }
        
        if self.length > 1 and direction == opposites.get(self.direction):
            return
        
        self.direction = direction

    def move(self):
        """Move the snake in the current direction"""
        x, y = self.positions[0]
        
        # Update position based on direction
        moves = {
            'up': (0, -GRID_SIZE),
            'down': (0, GRID_SIZE),
            'left': (-GRID_SIZE, 0),
            'right': (GRID_SIZE, 0)
        }
        dx, dy = moves[self.direction]
        
        # Add new head position
        new_position = (x + dx, y + dy)
        self.positions.insert(0, new_position)
        
        # Handle growth queue
        if self.growth_queue > 0:
            self.growth_queue -= 1
            self.length += 1
        elif len(self.positions) > self.length:
            self.positions.pop()
            
        # Update speed boost
        self._update_speed_boost()
        
        # Update base speed based on food eaten
        if not self.is_boosted:
            self.speed = min(
                MAX_FPS,
                self.base_speed + (self.food_eaten * SPEED_INCREMENT)
            )

    def grow(self, amount=1):
        """Queue growth segments"""
        self.growth_queue += amount

    def apply_food_effect(self, effect, duration=SPEED_BOOST_DURATION):
        """Apply effects from food"""
        self.food_eaten += 1  # Increment food counter
        
        if effect == 'speed':
            self.speed = BOOSTED_FPS
            self.speed_boost_end = time.time() + duration
            self.is_boosted = True
        elif effect == 'grow':
            self.grow(3)  # Grow by 3 segments for special food
        else:
            self.grow(1)  # Normal food grows by 1 segment

    def _update_speed_boost(self):
        """Update speed boost status"""
        if self.is_boosted and time.time() >= self.speed_boost_end:
            self.speed = BASE_FPS
            self.is_boosted = False

    def collides_with_self(self):
        """Check if snake collides with itself"""
        return self.head in self.positions[1:]

    def collides_with_walls(self):
        """Check if snake collides with walls"""
        x, y = self.head
        return (x < 0 or x >= SCREEN_WIDTH or 
                y < 0 or y >= SCREEN_HEIGHT)

    def get_color(self, segment_index):
        """Get color for snake segment"""
        return SNAKE_HEAD_COLOR if segment_index == 0 else SNAKE_BODY_COLOR

    def can_shoot(self):
        """Check if snake has ammo to shoot"""
        return self.ammo_count > 0
        
    def shoot(self):
        """Shoot a bullet, returns True if successful"""
        if self.can_shoot():
            self.ammo_count -= 1
            return True
        return False
        
    def add_ammo(self, amount):
        """Add ammo to snake's inventory"""
        self.ammo_count += amount