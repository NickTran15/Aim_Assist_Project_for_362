"Game Logic"

import pygame
from videogame import assets
from videogame import color_library
from videogame import scene
from videogame import scenemanager

def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


class VideoGame:

    def __init__(
        self,
        window_width=1250,
        window_height=750,
        window_title="Aim_Assist",
    ):
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False

    def run(self):
        raise NotImplementedError



class Aim_Assist(VideoGame):
    def __init__(self):
        super().__init__(window_title="Aim Assist")
        self._scene_manager = scenemanager.SceneManager(
            [
                scene.TitleScene(
                screen = self._screen,
                background_color = color_library.black,
                soundtrack = None,
                ),

                scene.MainMenuScene(
                screen = self._screen,
                background_color = color_library.gray_teal,
                soundtrack = None
                ),
                
                scene.DifficultyScene(
                screen = self._screen,
                background_color = color_library.gray_teal,
                soundtrack = None
                ),

                scene.Freemode(
                screen = self._screen,
                background_color = color_library.sky_blue,
                soundtrack = None,
                ),
                
                scene.MainMenuScene(
                screen = self._screen,
                background_color = color_library.gray_teal,
                soundtrack = None
                ),"""
                scene.Rush(
                screen = self._screen,
                background_color = color_library.sky_blue,
                soundtrack = None,
                ),

                scene.Tracker(
                screen = self._screen,
                background_color = color_library.sky_blue,
                soundtrack = None,
                ),

                scene.Random(
                screen = self._screen,
                background_color = color_library.sky_blue,
                soundtrack = None,
                )"""
                
            ]
        )

    def run(self):
        """Run the game; the main game loop."""
        scene_iterator = iter(self._scene_manager)
        current_scene = next(scene_iterator)
        selected_mode = None
        selected_difficulty = None
        
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
            
            # Capture selections before moving to next scene
            if isinstance(current_scene, scene.MainMenuScene):
                selected_mode = current_scene.get_selected_mode()
            elif isinstance(current_scene, scene.DifficultyScene):
                selected_difficulty = current_scene.get_selected_difficulty()
                # Create game scene based on selections
                if selected_mode == "freemode" and selected_difficulty:
                    current_scene = scene.Freemode(
                        self._screen,
                        color_library.sky_blue,
                        difficulty=selected_difficulty
                    )
                    current_scene.end_scene()
                    continue
            elif isinstance(current_scene, scene.Freemode):
                # Handle Freemode button actions
                if current_scene.is_retry_clicked():
                    # Restart Freemode with same difficulty
                    current_scene = scene.Freemode(
                        self._screen,
                        color_library.sky_blue,
                        difficulty=selected_difficulty
                    )
                    current_scene.end_scene()
                    continue
                elif current_scene.is_main_clicked():
                    # Go back to main menu - create fresh scene manager iterator
                    scene_iterator = iter(self._scene_manager)
                    next(scene_iterator)  # Skip TitleScene
                    current_scene = next(scene_iterator)  # MainMenuScene
                    continue
            
            current_scene.end_scene()
            try:
                current_scene = next(scene_iterator)
            except StopIteration:
                self._game_is_over = True
        pygame.quit()
        return 0