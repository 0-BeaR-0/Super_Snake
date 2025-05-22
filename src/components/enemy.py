import random
import math
import pygame
from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    ENEMY_SPEED, ENEMY_COLOR, ENEMY_SIZE
)

class Enemy:
    def __init__(self):
        self.length = 3  # Start with 3 segments
        self.growth_queue = 0
        self.color = ENEMY_COLOR
        self.base_speed = ENEMY_SPEED
        self.speed = self.base_speed
        self.target = None
        self.active = True
        self.size = ENEMY_SIZE
        self.food_eaten = 0
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.spawn_at_edge()  # Call after initializing length and other attributes
        self.positions = [self.position] * self.length

    def spawn_at_edge(self):
        edge = random.choice(['top', 'right', 'bottom', 'left'])
        if edge == 'top':
            self.position = (random.randint(0, SCREEN_WIDTH - GRID_SIZE), 0)
        elif edge == 'right':
            self.position = (SCREEN_WIDTH - GRID_SIZE, random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        elif edge == 'bottom':
            self.position = (random.randint(0, SCREEN_WIDTH - GRID_SIZE), SCREEN_HEIGHT - GRID_SIZE)
        else:
            self.position = (0, random.randint(0, SCREEN_HEIGHT - GRID_SIZE))
        self.positions = [self.position] * self.length

    def move(self, snake_head, food_position):
        if not self.active:
            return
        # Calculate distances to snake and food
        snake_dx = snake_head[0] - self.positions[0][0]
        snake_dy = snake_head[1] - self.positions[0][1]
        snake_distance = math.sqrt(snake_dx * snake_dx + snake_dy * snake_dy)
        food_dx = food_position[0] - self.positions[0][0]
        food_dy = food_position[1] - self.positions[0][1]
        food_distance = math.sqrt(food_dx * food_dx + food_dy * food_dy)
        # Choose target based on distance
        if food_distance < snake_distance * 0.8:
            dx, dy = food_dx, food_dy
            distance = food_distance
        else:
            dx, dy = snake_dx, snake_dy
            distance = snake_distance
        if distance != 0:
            dx = (dx / distance) * GRID_SIZE
            dy = (dy / distance) * GRID_SIZE
        # Determine direction for segment logic
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'
        # Add new head position
        new_x = self.positions[0][0] + dx * (self.speed / (self.base_speed * 2))  # Halved the speed multiplier
        new_y = self.positions[0][1] + dy * (self.speed / (self.base_speed * 2))  # Halved the speed multiplier
        new_x = max(0, min(SCREEN_WIDTH - GRID_SIZE, new_x))
        new_y = max(0, min(SCREEN_HEIGHT - GRID_SIZE, new_y))
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        # Handle growth queue
        if self.growth_queue > 0:
            self.growth_queue -= 1
            self.length += 1
        elif len(self.positions) > self.length:
            self.positions.pop()
        self.position = self.positions[0]

    def get_position_grid(self):
        x = round(self.positions[0][0] / GRID_SIZE) * GRID_SIZE
        y = round(self.positions[0][1] / GRID_SIZE) * GRID_SIZE
        return (x, y)

    def collides_with(self, position):
        enemy_pos = self.get_position_grid()
        return (abs(enemy_pos[0] - position[0]) < GRID_SIZE and
                abs(enemy_pos[1] - position[1]) < GRID_SIZE)

    def grow(self, amount=1):
        self.food_eaten += 1
        self.growth_queue += amount
        # Increase speed slightly for every 4th food consumed
        if self.food_eaten % 4 == 0:
            self.speed = min(self.base_speed * 0.5, self.speed + self.base_speed * 0.01)  # Further reduced speed increment and cap

    def reset_speed(self):
        self.speed = min(self.base_speed * 0.5, self.base_speed * (1 + self.food_eaten * 0.05))  # Reduced reset speed cap

    def draw(self, screen):
        # Draw each segment
        for i, pos in enumerate(self.positions):
            x, y = pos
            seg_size = self.size if i == 0 else self.size - 2
            color = (0, 255 - i * 10, 255 - i * 10) if i < 10 else (0, 50, 50)
            pygame.draw.rect(screen, color, (x, y, seg_size, seg_size))
        # Draw eyes on head
        x, y = self.positions[0]
        eye_size = max(4, int(self.size / 5))
        eye_color = (255, 255, 255)
        pygame.draw.rect(screen, eye_color,
                        (x + self.size/4, y + self.size/4, eye_size, eye_size))
        pygame.draw.rect(screen, eye_color,
                        (x + self.size*2/3, y + self.size/4, eye_size, eye_size))