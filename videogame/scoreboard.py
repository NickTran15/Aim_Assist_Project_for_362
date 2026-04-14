# Scoreboard for Aim Assist Game

import pygame
from videogame import assets

class Scoreboard:
    """
    Keeps track of hits, misses, and displays accuracy on the screen.
    """
    def __init__(self, x=20, y=20, font_size=30):
        # Track stats
        self.hits = 0
        self.misses = 0

        # Set up drawing text with custom font from assets
        font_path = assets.get('pixel-font')
        self.font = pygame.font.Font(font_path, font_size)

        # Position for where the scoreboard will be drawn
        self.position = (x, y)

    @property
    def accuracy(self):
        """
        Calculating the accuracy  as a percentage.
        If no shots yet, return 100%.
        """
        total_shots = self.hits + self.misses

        if total_shots == 0:
            return 100.0

        return (self.hits / total_shots) * 100

    def record_hit(self):
        """Increase hit count by 1."""
        self.hits += 1

    def record_miss(self):
        """Increase miss count by 1."""
        self.misses += 1

    def draw(self, screen):
        """
        Draw the scoreboard text on the screen.
        """
        #  display string
        text = f"Hits: {self.hits} | Accuracy: {self.accuracy:.1f}%"

        # Render the text (white color)
        text_surface = self.font.render(text, True, (255, 255, 255))

        # Draw it to the screen at the specific  position
        screen.blit(text_surface, self.position)