import random
import time
import pygame
import math
from src.config.settings import (
    GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    FOOD_TYPES
)

# Calculate grid dimensions
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.type = 'normal'
        self.properties = FOOD_TYPES[self.type]
        self.pulse_offset = 0
        self.glow_surface = None
        self.last_update = time.time()
        
    def randomize_position(self, snake_positions, enemy_position=None):
        """Randomize food position avoiding snake and enemy positions"""
        occupied_positions = set(snake_positions)
        if enemy_position:
            occupied_positions.add(enemy_position)
            
        grid_width = SCREEN_WIDTH // GRID_SIZE
        grid_height = SCREEN_HEIGHT // GRID_SIZE
            
        while True:
            self.position = (
                random.randint(0, grid_width - 1) * GRID_SIZE,
                random.randint(0, grid_height - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def set_random_type(self):
        """Randomly select food type based on probabilities"""
        weights = {
            'normal': 0.7,    # 70% chance for normal food
            'boost': 0.2,     # 20% chance for speed boost
            'special': 0.1    # 10% chance for special food
        }
        self.type = random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
        self.properties = FOOD_TYPES[self.type]

    @property
    def color(self):
        """Get the color based on food type"""
        return self.properties['color']

    @property
    def points(self):
        """Get the points value based on food type"""
        return self.properties['points']

    @property
    def effect(self):
        """Get the effect based on food type"""
        return self.properties['effect']

    def draw(self, screen):
        """Draw food with visual effects"""
        x, y = self.position
        current_time = time.time()
        
        # Update pulse
        self.pulse_offset = math.sin(current_time * 5) * 4
        
        # Calculate size with pulse effect
        base_size = GRID_SIZE - 2
        size = base_size + self.pulse_offset
        
        # Draw glow effect
        glow_size = int(size * 1.5)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        for i in range(10):
            alpha = 100 - i * 10
            radius = glow_size - i * 2
            pygame.draw.circle(glow_surface, (*self.color, alpha),
                             (glow_size, glow_size), radius)
        
        # Draw the glow
        screen.blit(glow_surface, 
                   (x - glow_size + GRID_SIZE//2,
                    y - glow_size + GRID_SIZE//2))
        
        # Draw main food
        pygame.draw.rect(screen, self.color,
                        (x + (GRID_SIZE - size)//2,
                         y + (GRID_SIZE - size)//2,
                         size, size))
        
        # Draw shine effect
        shine_color = (255, 255, 255, 150)
        shine_size = size // 3
        pygame.draw.rect(screen, shine_color,
                        (x + GRID_SIZE//4,
                         y + GRID_SIZE//4,
                         shine_size, shine_size))