import random
import math
import pygame
from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    ENEMY_SPEED, ENEMY_COLOR, ENEMY_SIZE
)

class Enemy:
    def __init__(self):
        # Start enemy at a random edge position
        self.spawn_at_edge()
        self.color = ENEMY_COLOR
        self.base_speed = ENEMY_SPEED
        self.speed = self.base_speed
        self.target = None
        self.active = True
        self.size = ENEMY_SIZE
        self.food_eaten = 0
        
    def spawn_at_edge(self):
        """Spawn the enemy at a random edge position"""
        edge = random.choice(['top', 'right', 'bottom', 'left'])
        if edge == 'top':
            self.position = (random.randint(0, SCREEN_WIDTH - GRID_SIZE), 0)
        elif edge == 'right':
            self.position = (SCREEN_WIDTH - GRID_SIZE, random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        elif edge == 'bottom':
            self.position = (random.randint(0, SCREEN_WIDTH - GRID_SIZE), SCREEN_HEIGHT - GRID_SIZE)
        else:  # left
            self.position = (0, random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
            
    def move(self, snake_head, food_position):
        """Move enemy towards either snake or food"""
        if not self.active:
            return
            
        # Calculate distances to snake and food
        snake_dx = snake_head[0] - self.position[0]
        snake_dy = snake_head[1] - self.position[1]
        snake_distance = math.sqrt(snake_dx * snake_dx + snake_dy * snake_dy)
        
        food_dx = food_position[0] - self.position[0]
        food_dy = food_position[1] - self.position[1]
        food_distance = math.sqrt(food_dx * food_dx + food_dy * food_dy)
        
        # Choose target based on distance
        if food_distance < snake_distance * 0.8:  # Prefer food if it's closer
            dx, dy = food_dx, food_dy
            distance = food_distance
        else:
            dx, dy = snake_dx, snake_dy
            distance = snake_distance
        
        if distance != 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
        
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        
        # Keep enemy within screen bounds
        new_x = max(0, min(SCREEN_WIDTH - GRID_SIZE, new_x))
        new_y = max(0, min(SCREEN_HEIGHT - GRID_SIZE, new_y))
        
        self.position = (new_x, new_y)
        
    def get_position_grid(self):
        """Get the enemy's position aligned to the grid"""
        x = round(self.position[0] / GRID_SIZE) * GRID_SIZE
        y = round(self.position[1] / GRID_SIZE) * GRID_SIZE
        return (x, y)

    def collides_with(self, position):
        """Check if enemy collides with a position"""
        enemy_pos = self.get_position_grid()
        return (abs(enemy_pos[0] - position[0]) < GRID_SIZE and
                abs(enemy_pos[1] - position[1]) < GRID_SIZE)
    
    def grow(self):
        """Increase enemy size and speed when consuming food"""
        self.food_eaten += 1
        # Increase size up to 150% of original
        self.size = min(ENEMY_SIZE * 1.5, ENEMY_SIZE * (1 + self.food_eaten * 0.1))
        # Increase speed up to 150% of base speed
        self.speed = min(self.base_speed * 1.5, self.base_speed * (1 + self.food_eaten * 0.1))
    
    def draw(self, screen):
        """Draw the enemy with visual effects"""
        x, y = self.position
        
        # Draw shadow
        shadow_color = (20, 20, 50)
        shadow_offset = 4
        pygame.draw.rect(screen, shadow_color,
                        (x + shadow_offset, y + shadow_offset,
                         self.size, self.size))
        
        # Draw main body with gradient
        for i in range(int(self.size)):
            color_value = max(50, int(255 * (1 - i/self.size)))
            color = (0, color_value, color_value)  # Cyan gradient
            pygame.draw.rect(screen, color,
                           (x + i, y + i, self.size - i*2, self.size - i*2))
        
        # Draw eyes
        eye_size = max(4, int(self.size / 5))
        eye_color = (255, 255, 255)
        pygame.draw.rect(screen, eye_color,
                        (x + self.size/4, y + self.size/4, eye_size, eye_size))
        pygame.draw.rect(screen, eye_color,
                        (x + self.size*2/3, y + self.size/4, eye_size, eye_size))