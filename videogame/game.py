"""Game objects to create PyGame based games."""

import warnings
import pygame
from videogame import assets
from videogame import colors
from videogame import scene
from videogame import scenemanager

def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=800,
        window_height=800,
        window_title="Galaga",
    ):
        """Initialize a new game with the given window size and window title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False
        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        else:
            pygame.mixer.init()
        self._scene_manager = None

    def run(self):
        """Run the game; the main game loop."""
        raise NotImplementedError



class aim_assist(VideoGame):
    def __init__(self):
        """Init the Pygame demo."""
        super().__init__(window_title="Aim Assist")
        self._scene_manager = scenemanager.SceneManager(
            [
                scene.TitleScene(
                screen = self._screen,
                background_color = colors.black,
                soundtrack = assets.get('title-theme'),
                ),
                scene.ControlScene(
                screen = self._screen,
                background_color = colors.black,
                soundtrack = assets.get('soundtrack')
                ),
                scene.GameScene(
                screen = self._screen,
                background_color = colors.black,
                soundtrack = assets.get('soundtrack')
                ),
                scene.GameOverScene(
                screen = self._screen,
                background_color = colors.black,
                soundtrack = assets.get('game-over-theme')
                )
            ]
        )

    def run(self):
        """Run the game; the main game loop."""
        scene_iterator = iter(self._scene_manager)
        current_scene = next(scene_iterator)
        while not self._game_is_over:
            current_scene.start_scene()
            while current_scene.is_valid():
                current_scene.delta_time = self._clock.tick(
                    current_scene.frame_rate()
                )
                for event in pygame.event.get():
                    current_scene.process_event(event)
                current_scene.update_scene()
                current_scene.draw()
                pygame.display.update()
            current_scene.end_scene()
            try:
                current_scene = next(scene_iterator)
            except StopIteration:
                self._game_is_over = True
        pygame.quit()
        return 0