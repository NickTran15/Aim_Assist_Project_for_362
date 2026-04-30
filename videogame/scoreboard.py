# Scoreboard for Aim Assist Game

import pygame
from videogame import assets

class Scoreboard:
    """Keeps track of hits and misses"""
    def __init__(self, x=20, y=20, font_size=30):
        self.hits = 0
        self.misses = 0

        font_path = assets.get('pixel-font')
        self.font = pygame.font.Font(font_path, font_size)

        self.position = (x, y)

    @property
    def accuracy(self):
        """Calculates accuracy"""
        total_shots = self.hits + self.misses

        if total_shots == 0:
            return 100.0

        return (self.hits / total_shots) * 100

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def draw(self, screen):
        """Draws scoreboard on screen"""
        text = f"Hits: {self.hits} | Accuracy: {self.accuracy:.1f}%"
        text_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, self.position)