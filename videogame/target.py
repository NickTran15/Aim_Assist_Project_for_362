import pygame
import random
from videogame import assets
from videogame import colors



class Target(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, target):
        super().__init__()
        image = self.image = pygame.image.load(assets.get('target'))
        self.image = pygame.transform.scale(image, (90, 90))
        self.rect = self.image.get_rect(center=start_pos)
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        self.position = pygame.Vector2(start_pos)
        self.speed = 3
        self.target = target
        self.move_state = "spawn"
        


    def update(self):
        current_time = pygame.time.get_ticks()

        if self.move_state == "spawn":
            self.move_to(self.end_pos)
            if self.position.distance_to(self.end_pos) < 5:
                self.move_state = "idle"
                self.position = self.end_pos
                self.last_dive =current_time
        
        elif self.move_state == "idle":
            if current_time - self.last_dive >= self.dive_delay:
                self.move_state = "dive"
        
        elif self.move_state == "dive":
            player_pos =pygame.Vector2(self.target.rect.center)
            self.move_to(player_pos)

            screen_height = pygame.display.get_surface().get_height()
            if self.rect.top > screen_height or self.position.distance_to(player_pos) < 5:
                self.move_state = "return"
            
        elif self.move_state == "return":
            self.move_to(self.end_pos)
            if self.position.distance_to(self.end_pos) < 5:
                self.state = "idle"
                self.dive_delay = random.randint(6000, 12000)
                self.last_dive = current_time
            
        self.rect.center = self.position

    def move_to(self, target):
        direction = target - self.position
        if direction.length() > 0:
            self.position += direction.normalize() * self.speed