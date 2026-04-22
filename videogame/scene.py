"Different Game Scenes"
#git config pull.rebase false
#
import pygame
from videogame import assets, color_library, button, target, scoreboard
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
    random_image = pygame.image.load(assets.get('random'))
    quit_image = pygame.image.load(assets.get('quit'))

    freemode_button = button.Button(475, 200, freemode_image, 0.8)
    rush_button = button.Button(475, 300, rush_image, 0.8)
    random_button = button.Button(475, 400, random_image, 0.8)
    quit_button = button.Button(475, 500, quit_image, 0.8)
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
    def __init__(self, screen, background_color, soundtrack=None, difficulty=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._difficulty = difficulty
        self._targets = pygame.sprite.Group()
        self._spawn_rate = self._get_spawn_rate(difficulty)
        self._last_spawn_time = pygame.time.get_ticks()
        self._total_spawned = 0
        self._max_targets = 30
        self._scoreboard = scoreboard.Scoreboard()
        
        #Creates retry and main menu buttons
        retry_image = pygame.image.load(assets.get('retry'))
        self._retry_button = button.Button(300, 375, retry_image, 0.8)
        self._show_retry_button = False

        main_image = pygame.image.load(assets.get('main'))
        self._main_button = button.Button(700, 375, main_image, 0.8)
        self._show_main_button = False
        
        #Button delay 
        self._all_spawned = False
        self._button_delay = 750  
        self._delay_start_time = None
        
        #Button action
        self._retry_clicked = False
        self._main_clicked = False

    def _get_spawn_rate(self, difficulty):
        #Spawn time based on difficulty
        rates = {
            "easy": 950,
            "medium": 850,
            "hard": 750
        }
        return rates.get(difficulty, 1000)
    
    def _get_despawn_time(self, difficulty):
        #Despawn time based on difficulty
        times = {
            "easy": 900,
            "medium": 800,
            "hard": 700

        }
        despawn = times.get(difficulty, 1000)
        return despawn

    def update_scene(self):
        """Spawn targets and update existing targets."""
        current_time = pygame.time.get_ticks()
        if current_time - self._last_spawn_time > self._spawn_rate and self._total_spawned < self._max_targets:
            self._spawn_target()
            self._last_spawn_time = current_time
        
        #Checks if all targets have spawned
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
        self._scoreboard.draw(self._screen)
        
        #Show retry and main buttons when all targets are spawned
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
                    self._targets.remove(target)
    
    def is_retry_clicked(self):
        return self._retry_clicked
    
    def is_main_clicked(self):
        return self._main_clicked
    




class Rush(Scene):
    def __init__(self, screen, background_color, soundtrack=None, difficulty=None):
        super().__init__(screen, background_color, soundtrack=soundtrack)
        self._difficulty = difficulty
        self._targets = pygame.sprite.Group()
        self._max_targets = 5
        self._total_spawned = 0
        self._scoreboard = scoreboard.Scoreboard()
        
        #Countdown before targets spawn
        self._countdown_start_time = pygame.time.get_ticks()
        self._countdown_duration = 3000 
        self._countdown_complete = False
        self._font = pygame.font.Font(assets.get('pixel-font'), 150)
        self._timer_font = pygame.font.Font(assets.get('pixel-font'), 30)  
        
        #Creates retry and main menu buttons
        retry_image = pygame.image.load(assets.get('retry'))
        self._retry_button = button.Button(300, 375, retry_image, 0.8)
        self._show_retry_button = False

        main_image = pygame.image.load(assets.get('main'))
        self._main_button = button.Button(700, 375, main_image, 0.8)
        self._show_main_button = False
        
        #Button delay 
        self._button_delay = 750  
        self._delay_start_time = None
        
        #Button action
        self._retry_clicked = False
        self._main_clicked = False
        
        #Timer
        self._timer_start_time = None
        self._timer_running = False
        self._timer_end_time = None

    def _spawn_all_targets(self):
        """Spawn all 5 targets at random locations."""
        for _ in range(self._max_targets):
            x = random.randint(50, self._screen.get_width() - 50)
            y = random.randint(50, self._screen.get_height() - 50)
            new_target = target.Target(x, y)
            self._targets.add(new_target)
            self._total_spawned += 1

    def update_scene(self):
        """Update Rush scene - handle countdown and target management."""
        current_time = pygame.time.get_ticks()
        
        #Check if countdown is over
        if not self._countdown_complete:
            if current_time - self._countdown_start_time >= self._countdown_duration:
                self._countdown_complete = True
                #Spawns all 5 targets
                self._spawn_all_targets()
                self._delay_start_time = pygame.time.get_ticks()
                # Start the timer
                self._timer_start_time = pygame.time.get_ticks()
                self._timer_running = True
        
        #Update targets if countdown is complete
        if self._countdown_complete:
            self._targets.update()
            
            #All targets clicked, show buttons
            if len(self._targets) == 0 and self._total_spawned >= self._max_targets:
                #Stop timer when all targets are clicked
                if self._timer_running:
                    self._timer_end_time = current_time
                    self._timer_running = False
                
                if self._delay_start_time and current_time - self._delay_start_time > self._button_delay:
                    self._show_retry_button = True
                    self._show_main_button = True

    def draw(self):
        """Draw the Rush scene."""
        super().draw()
        
        current_time = pygame.time.get_ticks()
        
        #Draw countdown if not yet complete
        if not self._countdown_complete:
            elapsed_time = current_time - self._countdown_start_time
            remaining_time = max(0, (self._countdown_duration - elapsed_time) // 1000 + 1)
            
            countdown_text = self._font.render(str(remaining_time), True, color_library.white)
            text_rect = countdown_text.get_rect(center=self._screen.get_rect().center)
            self._screen.blit(countdown_text, text_rect)
        
        #Draw timer if countdown is complete
        if self._countdown_complete and self._timer_start_time:
            if self._timer_running:
                elapsed_time = (current_time - self._timer_start_time) / 1000.0
            else:
                elapsed_time = (self._timer_end_time - self._timer_start_time) / 1000.0
            
            timer_text = self._timer_font.render(f"{elapsed_time:.2f}s", True, color_library.white)
            timer_rect = timer_text.get_rect(topright=(self._screen.get_width() - 20, 20))
            self._screen.blit(timer_text, timer_rect)
        
        #Draw targets and scoreboard
        self._targets.draw(self._screen)
        self._scoreboard.draw(self._screen)
        
        #Show retry and main buttons when gamemode is finished
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
        """Handle events in Rush scene."""
        super().process_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN and self._countdown_complete:
            for target_obj in self._targets:
                if not target_obj.is_clicked() and target_obj.contains_point(event.pos):
                    target_obj.click()
                    self._scoreboard.record_hit()
                    self._targets.remove(target_obj)
    
    def is_retry_clicked(self):
        return self._retry_clicked
    
    def is_main_clicked(self):
        return self._main_clicked


class Random(Scene):
    pass

