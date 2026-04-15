"""Visual particle burst effect when player hits a target."""

import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y     # Where target was hit
        # Setting random direction and speed for particle effect
        angle = random.uniform(0, 2 * math.pi) 
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)  #Lifetime of particle
        self.max_lifetime = self.lifetime
        self.color = color  # Particle color

    def update(self):
        # Move the particle according to its velocity
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15 # Adding downward pull (gravity)
        self.lifetime -= 1  # Reducing particle's lifetime on each frame

    def draw(self, screen):
        if self.lifetime > 0:  # Drawing particle only if target still alive
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

    def is_alive(self):
        return self.lifetime > 0
