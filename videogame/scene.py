"Different Game Scenes"

import pygame
from videogame import assets, color_library, button
import random

"""from videogame.target import Target"""

class Scene:

    def __init__(
        self, screen, background_color, screen_flags=None, soundtrack=None
    ):

        self._screen = screen
        if not screen_flags:
            screen_flags = pygame.SCALED
        self._background = pygame.Surface(
            self._screen.get_size(), flags=screen_flags
        )
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None


    def draw(self):
        self._screen.blit(self._background, (0, 0))


    def process_event(self, event):
        
        if event.type == pygame.QUIT:
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False

    def is_valid(self):
        return self._is_valid

    def render_updates(self):
        return self._render_updates
    
    def update_scene(self):
        return self.update_scene
    
    def start_scene(self):
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.05)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        return self._frame_rate


class NextScene(Scene):
    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False

    




class TitleScene(NextScene):
    def __init__(self, screen, background_color, soundtrack=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        screen.fill(color_library.dark_gray)
        self._background_image = pygame.image.load(assets.get('menu-title'))
        self._background_image = pygame.transform.scale(self._background_image, screen.get_size())
    
    def draw(self):
        self._screen.blit(self._background_image, (0, 0))


class MainMenuScene(Scene):
    menu_title = pygame.image.load(assets.get('menu-title'))
    freemode_image = pygame.image.load(assets.get('freemode'))
    rush_image = pygame.image.load(assets.get('rush'))
    tracker_image = pygame.image.load(assets.get('tracker'))
    random_image = pygame.image.load(assets.get('random'))
    quit_image = pygame.image.load(assets.get('quit'))

    freemode_button = button.Button(475, 200, freemode_image, 0.8)
    rush_button = button.Button(475, 300, rush_image, 0.8)
    tracker_button = button.Button(475, 400, tracker_image, 0.8)
    random_button = button.Button(475, 500, random_image, 0.8)
    quit_button = button.Button(475, 600, quit_image, 0.8)
    def __init__(self, screen, background_color, soundtrack=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._background_image = pygame.image.load(assets.get('menu-title'))
        self._background_image = pygame.transform.scale(self._background_image, self._screen.get_size())


    def draw(self):
        super().draw()
        self._screen.blit(self._background_image, (0, -250))
        if self.freemode_button.draw(self._screen):
            self._is_clicked = True
            print("freemode")

        if self.rush_button.draw(self._screen):
            self._is_clicked = True
            print("rush")

        if self.tracker_button.draw(self._screen):
            self._is_clicked = True
            print("tracker")

        if self.random_button.draw(self._screen):
            self._is_clicked = True
            print("random")

        if self.quit_button.draw(self._screen):
            self._is_clicked = True
            print("quit")
            pygame.quit()
            return 0



class Freemode(Scene):
    pass

class Rush(Scene):
    pass

class Tracker(Scene):
    pass

class Random(Scene):
    pass
