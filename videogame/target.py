"""Target sprite for Aim Assist game."""

import pygame
import math
import random
from videogame import color_library


class Target(pygame.sprite.Sprite):
    """A clickable target that disappears when clicked."""

    # Concentric ring colors (outermost to innermost)
    RING_COLORS = [
        (220, 50, 50),    # red outer
        (255, 255, 255),  # white
        (220, 50, 50),    # red
        (255, 255, 255),  # white
        (220, 50, 50),    # red center
    ]

    def __init__(self, x, y, radius=35):
        """Initialize a target at (x, y) with a given radius."""
        super().__init__()
        self._radius = radius
        self._x = x
        self._y = y
        self._clicked = False
        self._spawn_time = pygame.time.get_ticks()
        self._alpha = 255
        self._scale = 0.0          # for pop-in animation
        self._popping_in = True
        self._pop_speed = 0.12     # how fast the pop-in completes

        self.image = pygame.Surface(
            (radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(center=(x, y))
        self._draw()

    def _draw(self):
        """Draw the concentric ring target onto the surface."""
        self.image.fill((0, 0, 0, 0))
        cx = self._radius + 2
        cy = self._radius + 2
        r = self._radius

        # Shadow
        shadow_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 60), (cx + 3, cy + 3), r)
        self.image.blit(shadow_surf, (0, 0))

        num_rings = len(self.RING_COLORS)
        for i, color in enumerate(self.RING_COLORS):
            ring_r = int(r * (num_rings - i) / num_rings)
            pygame.draw.circle(self.image, color, (cx, cy), ring_r)

        # Outer border
        pygame.draw.circle(self.image, (180, 30, 30), (cx, cy), r, 2)

    def _draw_scaled(self, scale):
        """Draw a scaled version during pop-in animation."""
        self.image.fill((0, 0, 0, 0))
        cx = self._radius + 2
        cy = self._radius + 2
        r = max(1, int(self._radius * scale))

        num_rings = len(self.RING_COLORS)
        for i, color in enumerate(self.RING_COLORS):
            ring_r = max(1, int(r * (num_rings - i) / num_rings))
            pygame.draw.circle(self.image, color, (cx, cy), ring_r)
        pygame.draw.circle(self.image, (180, 30, 30), (cx, cy), r, 2)

    def update(self):
        """Update target animation state."""
        if self._popping_in:
            self._scale = min(1.0, self._scale + self._pop_speed)
            self._draw_scaled(self._scale)
            if self._scale >= 1.0:
                self._popping_in = False
                self._draw()

    def click(self):
        """Mark the target as clicked."""
        self._clicked = True

    def is_clicked(self):
        """Return True if target has been clicked."""
        return self._clicked

    def get_spawn_time(self):
        """Return the time (ms) when the target was spawned."""
        return self._spawn_time

    def get_reaction_time(self):
        """Return milliseconds since spawn."""
        return pygame.time.get_ticks() - self._spawn_time

    def contains_point(self, pos):
        """Return True if pos (x, y) is within this target's circle."""
        dx = pos[0] - self._x
        dy = pos[1] - self._y
        return math.sqrt(dx * dx + dy * dy) <= self._radius

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius


def random_target(screen_width, screen_height, radius=35, margin=60):
    """Create a target at a random position within the screen bounds."""
    x = random.randint(margin + radius, screen_width - margin - radius)
    y = random.randint(margin + radius + 60, screen_height - margin - radius)
    return Target(x, y, radius)