# src/components/menu.py

import pygame
import time
import math
from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BACKGROUND,
    MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR, MENU_FONT_SIZE
)

class Menu:
    def __init__(self):
        self.main_options = ["Play Game", "High Scores", "Options", "Help", "Quit"]
        self.options_menu = ["Difficulty", "Controls", "Sound", "Back"]
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.current_menu = "main"
        self.selected_option = 0
        self.difficulty = 1  # Default to Medium
        self.sound_enabled = True
        self.animation_offset = 0
        self.last_input_time = 0
        self.input_delay = 0.15  # Seconds between inputs
        
    def render_text(self, screen, text, position, size, color, pulsing=False):
        font = pygame.font.Font(None, size)
        if pulsing:
            # Create a pulsing effect for selected options
            pulse = (math.sin(time.time() * 5) + 1) / 2  # Value between 0 and 1
            color = tuple(max(0, min(255, c + 40 * pulse)) for c in color)
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)
        
    def display_menu(self, screen):
        screen.fill(MENU_BACKGROUND)
        current_time = time.time()
        
        # Update animation
        self.animation_offset = math.sin(current_time * 2) * 10
        
        # Draw title
        title = "Snake Game"
        self.render_text(
            screen, title,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + self.animation_offset),
            MENU_FONT_SIZE * 2, MENU_HIGHLIGHT_COLOR
        )
        
        # Get current menu options
        options = self.get_current_menu_options()
        
        # Draw menu options
        start_y = SCREEN_HEIGHT // 2
        for index, option in enumerate(options):
            color = MENU_HIGHLIGHT_COLOR if index == self.selected_option else MENU_TEXT_COLOR
            pulsing = index == self.selected_option
            
            # Add visual indicators for settings
            if self.current_menu == "options":
                if option == "Sound":
                    option = f"Sound: {'On' if self.sound_enabled else 'Off'}"
                elif option == "Difficulty":
                    option = f"Difficulty: {self.difficulties[self.difficulty]}"
                    
            self.render_text(
                screen,
                option,
                (SCREEN_WIDTH // 2, start_y + index * 50),
                MENU_FONT_SIZE,
                color,
                pulsing
            )
            
        # Draw controls hint
        self.render_text(
            screen,
            "↑↓: Select   Enter: Confirm   Esc: Back",
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50),
            MENU_FONT_SIZE // 2,
            MENU_TEXT_COLOR
        )
        
        pygame.display.update()
        
    def get_current_menu_options(self):
        if self.current_menu == "main":
            return self.main_options
        elif self.current_menu == "options":
            return self.options_menu
        return self.main_options
        
    def handle_input(self, events):
        current_time = time.time()
        if current_time - self.last_input_time < self.input_delay:
            return None
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.last_input_time = current_time
                
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_option = (self.selected_option - 1) % len(self.get_current_menu_options())
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_option = (self.selected_option + 1) % len(self.get_current_menu_options())
                elif event.key == pygame.K_RETURN:
                    return self.handle_selection()
                elif event.key == pygame.K_ESCAPE:
                    if self.current_menu != "main":
                        self.current_menu = "main"
                        self.selected_option = 0
                        return None
                    
        return None
        
    def handle_selection(self):
        options = self.get_current_menu_options()
        selected = options[self.selected_option]
        
        if self.current_menu == "main":
            if selected == "Play Game":
                return "start_game"
            elif selected == "Options":
                self.current_menu = "options"
                self.selected_option = 0
            elif selected == "Quit":
                return "quit"
                
        elif self.current_menu == "options":
            if selected == "Sound":
                self.sound_enabled = not self.sound_enabled
            elif selected == "Difficulty":
                self.difficulty = (self.difficulty + 1) % len(self.difficulties)
            elif selected == "Back":
                self.current_menu = "main"
                self.selected_option = 0
                
        return None