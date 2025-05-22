"""Graphics Engine module for enhanced visual effects"""
import pygame
import numpy as np
import math
from typing import Tuple, List, Optional, Union
from pygame import Surface

# Type hint for color values (RGB or RGBA)
ColorValue = Union[Tuple[int, int, int], Tuple[int, int, int, int]]

class GraphicsEngine:
    def __init__(self, screen: Surface):
        """Initialize the graphics engine."""
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Create surfaces for various effects
        self.light_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.particle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.buffer_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Initialize sprite and texture storage
        self.sprites = {}
        self.textures = {}
        
        # Animation system
        self.animations = {}
        self.current_frame = 0
        
        # Particle system
        self.particles = []

    def _ensure_rgba(self, color: ColorValue) -> Tuple[int, int, int, int]:
        """Convert RGB color to RGBA if needed."""
        if len(color) == 3:
            return (color[0], color[1], color[2], 255)
        return color

    def create_gradient(self, start_color: ColorValue, end_color: ColorValue, size: int) -> Surface:
        """Create a gradient surface."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Ensure colors have alpha values
        start_color = self._ensure_rgba(start_color)
        end_color = self._ensure_rgba(end_color)
        
        for i in range(size):
            factor = i / size
            color = [
                int(start_color[j] + (end_color[j] - start_color[j]) * factor)
                for j in range(3)
            ]
            alpha = int(start_color[3] + (end_color[3] - start_color[3]) * factor)
            pygame.draw.line(surface, (*color, alpha), (i, 0), (i, size))
        return surface

    def create_glow(self, color: ColorValue, radius: int, intensity: float = 1.0) -> Surface:
        """Create a glowing effect surface."""
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        color = self._ensure_rgba(color)
        
        for i in range(radius):
            alpha = int((1 - i/radius) * color[3] * intensity)
            if alpha > 0:
                pygame.draw.circle(
                    surface,
                    (color[0], color[1], color[2], alpha),
                    (radius, radius),
                    radius - i
                )
        return surface

    def add_particle_effect(
        self,
        position: Tuple[float, float],
        color: ColorValue,
        size: int,
        lifetime: int,
        velocity: Tuple[float, float] = (0, 0),
        gravity: float = 0,
        fade: bool = True
    ) -> None:
        """Add a particle effect."""
        color = self._ensure_rgba(color)
        particle = {
            "position": list(position),
            "color": color,
            "size": size,
            "lifetime": lifetime,
            "max_lifetime": lifetime,
            "velocity": list(velocity),
            "gravity": gravity,
            "fade": fade
        }
        self.particles.append(particle)

    def update_particles(self) -> None:
        """Update all particle effects."""
        self.particle_surface.fill((0, 0, 0, 0))

        for particle in self.particles[:]:
            # Update position
            particle["position"][0] += particle["velocity"][0]
            particle["position"][1] += particle["velocity"][1]
            particle["velocity"][1] += particle["gravity"]

            # Update lifetime
            particle["lifetime"] -= 1
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                continue

            # Calculate fade effect
            if particle["fade"]:
                alpha = int(255 * (particle["lifetime"] / particle["max_lifetime"]))
                particle["color"] = (*particle["color"][:3], alpha)

            # Render particle
            pygame.draw.circle(
                self.particle_surface,
                particle["color"],
                (int(particle["position"][0]), int(particle["position"][1])),
                particle["size"]
            )

    def apply_screen_shake(self, intensity: float = 1.0, duration: int = 5) -> None:
        """Apply a screen shake effect."""
        self.screen_shake = {
            "intensity": intensity,
            "duration": duration,
            "original_pos": self.screen.get_offset()
        }

    def update(self) -> None:
        """Update all visual effects."""
        # Clear effect surfaces
        self.light_surface.fill((0, 0, 0, 0))
        self.particle_surface.fill((0, 0, 0, 0))
        
        # Update particles
        self.update_particles()
        
        # Apply screen shake
        if hasattr(self, "screen_shake"):
            if self.screen_shake["duration"] > 0:
                dx = (np.random.random() * 2 - 1) * self.screen_shake["intensity"]
                dy = (np.random.random() * 2 - 1) * self.screen_shake["intensity"]
                self.screen.scroll(int(dx), int(dy))
                self.screen_shake["duration"] -= 1
            else:
                # Reset to original position
                current_pos = self.screen.get_offset()
                self.screen.scroll(
                    self.screen_shake["original_pos"][0] - current_pos[0],
                    self.screen_shake["original_pos"][1] - current_pos[1]
                )
                del self.screen_shake
        
        # Update animation frame
        self.current_frame += 1

    def render(self) -> None:
        """Render all visual effects to the screen."""
        # Blend particle effects
        self.screen.blit(self.particle_surface, (0, 0))
        
        # Blend lighting effects
        self.screen.blit(self.light_surface, (0, 0))
        
        # Update display
        pygame.display.flip()
