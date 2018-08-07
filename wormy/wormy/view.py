import logging
import pygame

from . import constants
from . import coordinates
from . import events
from . import game_states
from . import start_screen
from . import settings


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, main_event_manager, model):
        main_event_manager.register_listener(self)
        self._model = model
        self._is_initialized = False
        self._screen = None
        self._basic_font = None
        self._start_screen = None

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._handle_quit()
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.TickEvent):
            self.render_all()

    def _handle_quit(self):
        self._is_initialized = False
        # ends the pygame graphical display
        pygame.quit()


    def render_all(self):
        if not self._is_initialized:
            return
        if self._model.game_state is game_states.GameState.start_screen:
            self._draw_start_screen()
        elif self._model.game_state is game_states.GameState.game_over:
            self._draw_gameplay_screen()
            self._draw_game_over()
        else:
            self._draw_gameplay_screen()
        pygame.display.update()

    def _draw_gameplay_screen(self):
        # clear display
        self._screen.fill(settings.BG_COLOR)
        self._draw_grid()
        self._draw_apple()
        self._draw_worm()
        self._draw_score()

    def _draw_game_over(self):
        top = 10
        game_over_font = pygame.font.Font('freesansbold.ttf', 150)
        game_surface = game_over_font.render('Game', True, constants.WHITE)
        over_surface = game_over_font.render('Over', True, constants.WHITE)
        game_rect = game_surface.get_rect()
        over_rect = over_surface.get_rect()
        game_rect.midtop = (settings.WINDOW_WIDTH / 2, top)
        over_rect.midtop = (settings.WINDOW_WIDTH / 2,
                            top + game_rect.height + 25)
        self._screen.blit(game_surface, game_rect)
        self._screen.blit(over_surface, over_rect)
        self._draw_press_key_message()

    def _draw_grid(self):
        for vertical_line_x in range(0, settings.WINDOW_WIDTH,
                                  settings.CELL_SIZE):
            pygame.draw.line(self._screen, constants.DARK_GRAY,
                             (vertical_line_x, 0), (vertical_line_x,
                                                    settings.WINDOW_HEIGHT))

        for horizontal_line_y in range(0, settings.WINDOW_HEIGHT,
                                       settings.CELL_SIZE):
            pygame.draw.line(self._screen, constants.DARK_GRAY,
                             (0, horizontal_line_y),
                             (settings.WINDOW_WIDTH, horizontal_line_y))

    def _draw_score(self):
        score_surf = self._basic_font.render(
            f'Score: {self._model.score}',
            True,
            constants.WHITE
        )
        score_rect = score_surf.get_rect()
        score_rect.topleft = (settings.WINDOW_WIDTH - 120, 10)
        self._screen.blit(score_surf, score_rect)

    def _draw_worm(self):
        for coord in self._model.worm_coords:
            self._draw_box_at_coord(coord, constants.GREEN)

    def _draw_box_at_coord(self, coord, color):
        top_left = coordinates.get_top_left_of_coord(coord)
        top = top_left.pixel_y
        left = top_left.pixel_x
        box_rect = (left, top, settings.CELL_SIZE, settings.CELL_SIZE)
        pygame.draw.rect(self._screen, color, box_rect)

    def _draw_apple(self):
        self._draw_box_at_coord(self._model.apple_coord, constants.RED)

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('wormy')
        self._screen = pygame.display.set_mode((settings.WINDOW_WIDTH,
                                               settings.WINDOW_HEIGHT))
        self._basic_font = pygame.font.Font('freesansbold.ttf', 18)
        self._is_initialized = True
        self._start_screen = start_screen.StartScreen(self._screen)

    def _draw_start_screen(self):
        """Draws the starting title screen.
        """
        self._start_screen.draw()
        self._draw_press_key_message()

    def _draw_press_key_message(self):
        """Draws the message instructing the user to press a key.
        """
        press_key_surface = self._basic_font.render('Press a key to play.',
                                                    True, constants.DARK_GRAY)
        press_key_rect = press_key_surface.get_rect()
        press_key_rect.topleft = (settings.WINDOW_WIDTH - 200,
                                  settings.WINDOW_HEIGHT - 30)
        self._screen.blit(press_key_surface, press_key_rect)
