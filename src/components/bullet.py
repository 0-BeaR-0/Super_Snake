import pygame
from src.config.settings import GRID_SIZE

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = GRID_SIZE * 1.5  # Faster than snake
        self.active = True
        self.color = (255, 255, 0)  # Yellow bullet
        self.size = GRID_SIZE // 2
        
    def move(self):
        """Move the bullet in its direction"""
        if not self.active:
            return
            
        moves = {
            'up': (0, -self.speed),
            'down': (0, self.speed),
            'left': (-self.speed, 0),
            'right': (self.speed, 0)
        }
        dx, dy = moves[self.direction]
        self.x += dx
        self.y += dy
        
    def is_off_screen(self, screen_width, screen_height):
        """Check if bullet is off screen"""
        return (self.x < 0 or self.x > screen_width or
                self.y < 0 or self.y > screen_height)
                
    def get_position(self):
        """Get bullet's current position"""
        return (self.x, self.y)
        
    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.rect(screen, self.color,
                        (self.x, self.y, self.size, self.size))
