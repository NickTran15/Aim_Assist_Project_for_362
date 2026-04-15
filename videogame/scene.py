"Different Game Scenes"
#git config pull.rebase false
#
import pygame
from videogame import assets, color_library, button, target, scoreboard, particle
import random


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

"Displays the main menu and game modes for the player to choose from"
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
        self._selected_mode = None


    def draw(self):
        super().draw()
        self._screen.blit(self._background_image, (0, -250))
        if self.freemode_button.draw(self._screen):
            self._selected_mode = "freemode"
            self._is_valid = False
            print("freemode")
            

        if self.rush_button.draw(self._screen):
            self._selected_mode = "rush"
            self._is_valid = False
            print("rush")

        if self.tracker_button.draw(self._screen):
            self._selected_mode = "tracker"
            self._is_valid = False
            print("tracker")

        if self.random_button.draw(self._screen):
            self._selected_mode = "random"
            self._is_valid = False
            print("random")

        if self.quit_button.draw(self._screen):
            self._is_valid = False
            print("quit")
            pygame.quit()
    
    def get_selected_mode(self):
        return self._selected_mode
 
"Displays all difficulties for the player to choose from"
class DifficultyScene(Scene):
    menu_title = pygame.image.load(assets.get('menu-title'))
    easy_image = pygame.image.load(assets.get('easy'))
    medium_image = pygame.image.load(assets.get('medium'))
    hard_image = pygame.image.load(assets.get('hard'))

    easy_button = button.Button(200, 400, easy_image, 0.8)
    medium_button = button.Button(500, 400, medium_image, 0.8)
    hard_button = button.Button(800, 400, hard_image, 0.8)
    def __init__(self, screen, background_color, soundtrack=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._background_image = pygame.image.load(assets.get('menu-title'))
        self._background_image = pygame.transform.scale(self._background_image, self._screen.get_size())
        self._selected_difficulty = None

    def draw(self):
        super().draw()
        self._screen.blit(self._background_image, (0, -250))
        if self.easy_button.draw(self._screen):
            self._selected_difficulty = "easy"
            self._is_valid = False
            print("easy")

        if self.medium_button.draw(self._screen):
            self._selected_difficulty = "medium"
            self._is_valid = False
            print("medium")

        if self.hard_button.draw(self._screen):
            self._selected_difficulty = "hard"
            self._is_valid = False
            print("hard")
    
    def get_selected_difficulty(self):
        return self._selected_difficulty



class Freemode(Scene):
    restart = False
    def __init__(self, screen, background_color, soundtrack=None, difficulty=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._difficulty = difficulty
        self._targets = pygame.sprite.Group()
        self._spawn_rate = self._get_spawn_rate(difficulty)
        self._last_spawn_time = pygame.time.get_ticks()
        self._total_spawned = 0
        self._max_targets = 150
        self._scoreboard = scoreboard.Scoreboard()
        self._particle_system = ParticleSystem()
        
        #Creates retry and main menu buttons
        retry_image = pygame.image.load(assets.get('retry'))
        self._retry_button = button.Button(300, 375, retry_image, 0.8)
        self._show_retry_button = False

        main_image = pygame.image.load(assets.get('main'))
        self._main_button = button.Button(700, 375, main_image, 0.8)
        self._show_main_button = False
        
        #Button delay timer
        self._all_spawned = False
        self._button_delay = 500  
        self._delay_start_time = None
        
        #Button action flags
        self._retry_clicked = False
        self._main_clicked = False

    def _get_spawn_rate(self, difficulty):
        #Return spawn rate based on difficulty
        rates = {
            "easy": 1000,
            "medium": 850,
            "hard": 100
        }
        return rates.get(difficulty, 1000)
    
    def _get_despawn_time(self, difficulty):
        #Return despawn time based on difficulty
        times = {
            "easy": 950,
            "medium": 800,
            "hard": 100       
        }
        despawn = times.get(difficulty, 2000)
        return despawn

    def update_scene(self):
        """Spawn targets and update existing targets."""
        current_time = pygame.time.get_ticks()
        if current_time - self._last_spawn_time > self._spawn_rate and self._total_spawned < self._max_targets:
            self._spawn_target()
            self._last_spawn_time = current_time
        
        #Checks if all targets have been spawned
        if self._total_spawned >= self._max_targets and not self._all_spawned:
            self._all_spawned = True
            self._delay_start_time = pygame.time.get_ticks()
        
        #Checks if delay has passed and show buttons
        if self._all_spawned and self._delay_start_time:
            if current_time - self._delay_start_time > self._button_delay:
                self._show_retry_button = True
                self._show_main_button = True
        
        #Remove targets that have been alive longer than despawn time
        despawn_time = self._get_despawn_time(self._difficulty)
        targets_to_remove = []
        for target in self._targets:
            if target.get_reaction_time() > despawn_time:
                targets_to_remove.append(target)
        
        for target in targets_to_remove:
            self._scoreboard.record_miss()
            self._targets.remove(target)

        self._particle_system.update()
        self._targets.update()

    def _spawn_target(self):
        """Spawn a new target at a random location."""
        x = random.randint(50, self._screen.get_width() - 50)
        y = random.randint(50, self._screen.get_height() - 50)
        new_target = target.Target(x, y)
        self._targets.add(new_target)
        self._total_spawned += 1

    def draw(self):
        super().draw()
        self._targets.draw(self._screen)
        self._particle_system.draw(self._screen)
        self._scoreboard.draw(self._screen)
        
        # Show retry and main buttons when all targets are spawned
        if self._show_retry_button:
            if self._retry_button.draw(self._screen):
                self._retry_clicked = True
                self._is_valid = False
                print("Retry clicked")

        if self._show_main_button:
            if self._main_button.draw(self._screen):
                self._main_clicked = True
                self._is_valid = False
                print("Main menu clicked")
    
    def process_event(self, event):
        super().process_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for target in self._targets:
                if not target.is_clicked() and target.contains_point(event.pos):
                    target.click()
                    self._scoreboard.record_hit()
                    self._particle_system.emit(*event.pos, color=(220, 50, 50))  # particle hit
                    self._targets.remove(target)
    
    def is_retry_clicked(self):
        return self._retry_clicked
    
    def is_main_clicked(self):
        return self._main_clicked
    

class Rush(Scene):
    pass

class Tracker(Scene):
    pass

class Random(Scene):
    pass

