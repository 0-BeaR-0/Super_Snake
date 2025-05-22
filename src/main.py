"""Main game module"""
import pygame
import sys
import time
from src.components.snake import Snake
from src.components.food import Food
from src.components.enemy import Enemy
from src.components.menu import Menu
from src.components.bullet import Bullet
from src.components.ammo import Ammo
from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    BASE_FPS, BLACK, WHITE, GRID_LINE_COLOR,
)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Advanced Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Game components
        self.menu = Menu()
        self.snake = Snake()
        self.food = Food()
        self.enemy = Enemy()
        self.bullets = []
        self.ammo = None
        
        # Game state
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.score = 0
        self.high_score = 0
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                        
                if self.game_state == "playing":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.turn('up')
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.turn('down')
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.turn('left')
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.turn('right')
                    elif event.key == pygame.K_SPACE:
                        if self.snake.can_shoot():
                            new_bullet = Bullet(
                                self.snake.head[0],
                                self.snake.head[1],
                                self.snake.direction
                            )
                            self.bullets.append(new_bullet)
                            self.snake.shoot()
        return True
        
    def update(self):
        if self.game_state != "playing":
            return
            
        # Move snake
        self.snake.move()
        
        # Move enemy
        self.enemy.move(self.snake.head, self.food.position)
        
        # Move bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)
            elif self.enemy.collides_with(bullet.get_position()):
                self.bullets.remove(bullet)
                self.enemy.spawn_at_edge()
                self.score += 5  # Bonus points for hitting enemy
        
        # Check collisions
        if (self.snake.collides_with_walls() or 
            self.snake.collides_with_self() or 
            self.enemy.collides_with(self.snake.head)):
            self.game_over()
            return
            
        # Check food collision for snake
        if self.snake.head == self.food.position:
            self.score += self.food.points
            self.high_score = max(self.score, self.high_score)
            self.snake.apply_food_effect(self.food.effect)
            self.food.set_random_type()
            self.food.randomize_position(self.snake.positions, self.enemy.position)
            
        # Check food collision for enemy
        if self.enemy.collides_with(self.food.position):
            self.enemy.grow()
            self.food.set_random_type()
            self.food.randomize_position(self.snake.positions, self.enemy.position)
            
        # Handle ammo pickup
        if not self.ammo:
            self.ammo = Ammo()
            self.ammo.randomize_position(
                self.snake.positions,
                self.food.position,
                self.enemy.get_position_grid()
            )
        elif self.snake.head == self.ammo.position:
            self.snake.add_ammo(self.ammo.amount)
            self.ammo = None
            
    def draw_game(self):
        self.screen.fill(BLACK)
        
        # Draw grid with fading effect
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            fade = 1 - abs(x - SCREEN_WIDTH/2) / (SCREEN_WIDTH/2)
            color = tuple(int(c * fade) for c in GRID_LINE_COLOR)
            pygame.draw.line(self.screen, color, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            fade = 1 - abs(y - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)
            color = tuple(int(c * fade) for c in GRID_LINE_COLOR)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Draw game objects with enhanced effects
        self.enemy.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw snake with gradient effect
        for i, pos in enumerate(self.snake.positions):
            if i == 0:  # Head
                pygame.draw.rect(self.screen, self.snake.get_color(i),
                               (pos[0], pos[1], GRID_SIZE-1, GRID_SIZE-1))
                # Draw eyes
                eye_color = WHITE
                eye_size = 4
                pygame.draw.rect(self.screen, eye_color,
                               (pos[0] + GRID_SIZE//4, pos[1] + GRID_SIZE//4,
                                eye_size, eye_size))
                pygame.draw.rect(self.screen, eye_color,
                               (pos[0] + GRID_SIZE*2//3, pos[1] + GRID_SIZE//4,
                                eye_size, eye_size))
            else:  # Body segments
                color = self.snake.get_color(i)
                pygame.draw.rect(self.screen, color,
                               (pos[0], pos[1], GRID_SIZE-1, GRID_SIZE-1))
                # Add shine effect to body
                pygame.draw.line(self.screen, WHITE,
                               (pos[0], pos[1]),
                               (pos[0] + GRID_SIZE//2, pos[1]), 2)
        
        # Draw bullets with trail effect
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        # Draw ammo pickup with glow effect
        if self.ammo:
            self.ammo.draw(self.screen)
            
        # Draw HUD
        score_text = f"Score: {self.score}  High Score: {self.high_score}  Ammo: {self.snake.ammo_count}"
        score_surface = self.font.render(score_text, True, WHITE)
        self.screen.blit(score_surface, (10, 10))
        
        pygame.display.flip()
        
    def game_over(self):
        self.game_state = "game_over"
        if self.score > self.high_score:
            self.high_score = self.score
            
    def reset_game(self):
        self.snake.reset()
        self.enemy = Enemy()
        self.food = Food()
        self.food.randomize_position(self.snake.positions, self.enemy.position)
        self.bullets = []
        self.ammo = None
        self.score = 0
        self.game_state = "playing"
        
    def run(self):
        while True:
            if not self.handle_input():
                break
                
            if self.game_state == "menu":
                self.menu.display_menu(self.screen)
                events = pygame.event.get()
                action = self.menu.handle_input(events)
                
                if action == "start_game":
                    self.reset_game()
                elif action == "quit":
                    break
                    
            elif self.game_state == "playing":
                self.update()
                self.draw_game()
                self.clock.tick(self.snake.speed)
                
            elif self.game_state == "game_over":
                self.screen.fill(BLACK)
                game_over_text = self.font.render(f"Game Over! Score: {self.score}", True, WHITE)
                restart_text = self.font.render("Press SPACE to restart or ESC for menu", True, WHITE)
                
                self.screen.blit(game_over_text, 
                    (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
                self.screen.blit(restart_text,
                    (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
                
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.game_state = "menu"
                            
            elif self.game_state == "paused":
                pause_text = self.font.render("PAUSED", True, WHITE)
                self.screen.blit(pause_text, 
                    (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2))
                pygame.display.flip()
                
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()