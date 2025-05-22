import random
import time
import math
import pygame
from src.config.settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

# Calculate grid dimensions
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

class Ammo:
    def __init__(self):
        self.position = (0, 0)
        self.color = (128, 128, 255)  # Light blue
        self.amount = 5  # Bullets given per pickup
        
    def randomize_position(self, snake_positions, food_position, enemy_position):
        """Randomize ammo position avoiding snake, food and enemy"""
        occupied_positions = set(snake_positions)
        occupied_positions.add(food_position)
        if enemy_position:
            occupied_positions.add(enemy_position)
            
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break
                
    def draw(self, screen):
        """Draw ammo pickup with effects"""
        x, y = self.position
        current_time = time.time()
        
        # Pulsing effect
        pulse = (math.sin(current_time * 5) + 1) / 2  # Value between 0 and 1
        size = GRID_SIZE - 4 + (pulse * 4)  # Size varies by 4 pixels
        
        # Draw glow effect
        glow_radius = int(GRID_SIZE * 0.8)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        for i in range(5):
            alpha = int(80 * pulse) - i * 15
            radius = glow_radius - i * 2
            if alpha > 0:  # Only draw if visible
                color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
                pygame.draw.circle(glow_surface, color_with_alpha,
                                 (glow_radius, glow_radius), radius)
        
        # Draw the glow
        screen.blit(glow_surface,
                   (x - glow_radius + GRID_SIZE//2,
                    y - glow_radius + GRID_SIZE//2))
        
        # Draw main ammo box
        pygame.draw.rect(screen, self.color,
                        (x + (GRID_SIZE - size)/2,
                         y + (GRID_SIZE - size)/2,
                         size, size))
        
        # Draw cross pattern
        cross_color = (255, 255, 255)
        cross_size = size * 0.6
        center_x = x + GRID_SIZE/2
        center_y = y + GRID_SIZE/2
        
        # Horizontal line
        pygame.draw.line(screen, cross_color,
                        (center_x - cross_size/2, center_y),
                        (center_x + cross_size/2, center_y), 2)
        
        # Vertical line
        pygame.draw.line(screen, cross_color,
                        (center_x, center_y - cross_size/2),
                        (center_x, center_y + cross_size/2), 2)
