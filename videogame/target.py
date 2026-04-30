"""Target sprite for Aim Assist game"""

import pygame
import math
import random
from videogame import color_library


class Target(pygame.sprite.Sprite):
    """A clickable target that disappears when clicked"""

    #Ring colors
    RING_COLORS = [
        color_library.red,
        color_library.white,
        color_library.red,
        color_library.white,
        color_library.red,
    ]
    
    """Initialize target with a given radius"""
    def __init__(self, x, y, radius=35):
        super().__init__()
        self._radius = radius
        self._x = x
        self._y = y
        self._clicked = False
        self._spawn_time = pygame.time.get_ticks()
        self._alpha = 255
        self._scale = 0.0
        self._popping_in = True
        self._pop_speed = 0.12

        self.image = pygame.Surface(
            (radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(center=(x, y))
        self._draw()

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        cx = self._radius + 2
        cy = self._radius + 2
        r = self._radius

        #Circle shadow
        shadow_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 60), (cx + 3, cy + 3), r)
        self.image.blit(shadow_surf, (0, 0))

        num_rings = len(self.RING_COLORS)
        for i, color in enumerate(self.RING_COLORS):
            ring_r = int(r * (num_rings - i) / num_rings)
            pygame.draw.circle(self.image, color, (cx, cy), ring_r)

        #Circle outer border
        pygame.draw.circle(self.image, (180, 30, 30), (cx, cy), r, 2)

    
    """Scaled version during animation"""
    def _draw_scaled(self, scale):
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
        if self._popping_in:
            self._scale = min(1.0, self._scale + self._pop_speed)
            self._draw_scaled(self._scale)
            if self._scale >= 1.0:
                self._popping_in = False
                self._draw()

    """Mark the target as clicked"""
    def click(self):
        self._clicked = True

    """Return True if target has been clicked"""
    def is_clicked(self):
        return self._clicked

    """Return time when the target is spawned"""
    def get_spawn_time(self):
        return self._spawn_time

    """Return time since spawn."""
    def get_reaction_time(self):
        return pygame.time.get_ticks() - self._spawn_time
    
    
    """Return True if pos (x, y) is within this target's circle"""
    def contains_point(self, pos):
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


"""Create target at random positions inside screen borders"""
def random_target(screen_width, screen_height, radius=35, margin=60):
    x = random.randint(margin + radius, screen_width - margin - radius)
    y = random.randint(margin + radius + 60, screen_height - margin - radius)
    return Target(x, y, radius)