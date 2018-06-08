import logging
import pygame

from . import constants
from . import events
from . import settings


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, main_event_manager, model):
        main_event_manager.register_listener(self)
        self._model = model
        self._is_initialized = False
        self._screen = None
        self._basic_font = None

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
        # clear display
        self._screen.fill(settings.BG_COLOR)
        self._draw_grid()
        self._draw_score()
        pygame.display.update()

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



    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('wormy')
        self._screen = pygame.display.set_mode((settings.WINDOW_WIDTH,
                                               settings.WINDOW_HEIGHT))
        self._basic_font = pygame.font.Font('freesansbold.ttf', 18)
        self._is_initialized = True
