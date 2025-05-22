import pygame
import math
import time
from src.config.settings import (
    GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, GREEN, RED, BLUE, YELLOW,
    GRID_LINE_COLOR
)

def render_text(screen, text, font, color, position, shadow=False, pulsing=False):
    """Render text with optional shadow and pulsing effect"""
    if pulsing:
        # Create a pulsing effect
        pulse = (math.sin(time.time() * 5) + 1) / 2  # Value between 0 and 1
        color = tuple(max(0, min(255, c + 40 * pulse)) for c in color)
    
    if shadow:
        # Render shadow first
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_pos = (position[0] + 2, position[1] + 2)
        screen.blit(shadow_surface, shadow_pos)
    
    # Render main text
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_background(screen, color=BLACK):
    """Fill the screen with a background color and grid"""
    screen.fill(color)
    draw_grid(screen)

def draw_grid(screen):
    """Draw a grid on the screen with fade effect towards edges"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        # Calculate fade based on distance from center
        fade = 1 - abs(x - SCREEN_WIDTH/2) / (SCREEN_WIDTH/2)
        color = tuple(int(c * fade) for c in GRID_LINE_COLOR)
        pygame.draw.line(screen, color, (x, 0), (x, SCREEN_HEIGHT))
    
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        fade = 1 - abs(y - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)
        color = tuple(int(c * fade) for c in GRID_LINE_COLOR)
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def display_score(screen, font, score, high_score, boost_active=False):
    """Display the current score and high score with visual effects"""
    # Score shadow
    score_text = f"Score: {score}"
    render_text(screen, score_text, font, WHITE, (10, 10), shadow=True, pulsing=boost_active)
    
    # High score with golden color
    high_score_text = f"High Score: {high_score}"
    render_text(screen, high_score_text, font, YELLOW, (10, 50), shadow=True)

def display_game_over(screen, font, score, high_score):
    """Display an animated game over screen"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Game over text with pulsing effect
    game_over_text = "GAME OVER!"
    text_pos = (SCREEN_WIDTH // 2 - font.size(game_over_text)[0] // 2, 
                SCREEN_HEIGHT // 2 - 50)
    render_text(screen, game_over_text, font, RED, text_pos, shadow=True, pulsing=True)
    
    # Score display
    score_text = f"Score: {score}"
    score_pos = (SCREEN_WIDTH // 2 - font.size(score_text)[0] // 2, 
                 SCREEN_HEIGHT // 2 + 10)
    render_text(screen, score_text, font, WHITE, score_pos, shadow=True)
    
    # High score display
    if score == high_score:
        high_score_text = "NEW HIGH SCORE!"
        high_score_pos = (SCREEN_WIDTH // 2 - font.size(high_score_text)[0] // 2,
                         SCREEN_HEIGHT // 2 + 70)
        render_text(screen, high_score_text, font, YELLOW, high_score_pos, 
                   shadow=True, pulsing=True)
    
    # Restart prompt
    restart_text = "Press SPACE to restart or ESC for menu"
    restart_pos = (SCREEN_WIDTH // 2 - font.size(restart_text)[0] // 2,
                  SCREEN_HEIGHT * 3 // 4)
    render_text(screen, restart_text, font, WHITE, restart_pos, shadow=True)

def display_boost_indicator(screen, font, remaining_time):
    """Display active speed boost indicator"""
    if remaining_time > 0:
        boost_text = f"SPEED BOOST: {remaining_time:.1f}s"
        boost_pos = (SCREEN_WIDTH - 200, 10)
        render_text(screen, boost_text, font, YELLOW, boost_pos, pulsing=True)

def draw_snake_segment(screen, position, size, is_head=False):
    """Draw a snake segment with effects"""
    x, y = position
    if is_head:
        # Draw head with gradient
        for i in range(size):
            color_value = 255 - (i * 2)
            color = (0, color_value, 0)
            pygame.draw.rect(screen, color, (x + i, y + i, size - i*2, size - i*2))
    else:
        # Draw body segment
        pygame.draw.rect(screen, GREEN, (x, y, size-1, size-1))
        # Add shine effect
        pygame.draw.line(screen, (0, 255, 0), (x, y), (x + size//2, y), 2)

def draw_food(screen, position, color, size, pulse=False):
    """Draw food with visual effects"""
    x, y = position
    if pulse:
        # Add pulsing effect
        pulse_value = (math.sin(time.time() * 5) + 1) / 4  # Value between 0 and 0.5
        size_mod = int(size * (1 + pulse_value))
        x_mod = x - (size_mod - size) // 2
        y_mod = y - (size_mod - size) // 2
        pygame.draw.rect(screen, color, (x_mod, y_mod, size_mod, size_mod))
    else:
        pygame.draw.rect(screen, color, (x, y, size, size))

def draw_enemy(screen, position, color, size):
    """Draw enemy with visual effects"""
    x, y = position
    # Draw main body
    pygame.draw.rect(screen, color, (x, y, size, size))
    # Add eye effect
    eye_color = (255, 255, 255)
    eye_size = size // 4
    pygame.draw.rect(screen, eye_color, (x + size//4, y + size//4, eye_size, eye_size))
    pygame.draw.rect(screen, eye_color, (x + size//2, y + size//4, eye_size, eye_size))