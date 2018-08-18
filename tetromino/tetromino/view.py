import logging
import pygame

from . import coords
from . import events
from . import settings


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, main_event_manager, model):
        main_event_manager.register_listener(self)
        self._model = model
        self._is_initialized = False
        self._screen = None

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
        self._screen.fill((0, 0, 0))
        self._draw_border()
        for box_coord in coords.get_all_box_coords():
            color = self._model.get_box_color(box_coord.box_x,
                                              box_coord.box_y)
            self._draw_box(box_coord, color)
        pygame.display.update()

    def _draw_border(self):
        border_rect = (settings.X_MARGIN - 3,
                       settings.TOP_MARGIN - 7,
                       (settings.BOARD_WIDTH * settings.BOX_SIZE) + 8,
                       (settings.BOARD_HEIGHT * settings.BOX_SIZE) + 8)
        pygame.draw.rect(self._screen, settings.BORDER_COLOR, border_rect, 5)

    def _draw_box(self, coord, color):
        top_left = coords.top_left_coord_of_box(coord)
        box_rect = (top_left.pixel_x, top_left.pixel_y, settings.BOX_SIZE,
                    settings.BOX_SIZE)
        pygame.draw.rect(self._screen, color, box_rect)

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tetromino')
        self._screen = pygame.display.set_mode((settings.WINDOW_WIDTH,
                                                settings.WINDOW_HEIGHT))
        self._is_initialized = True
        logging.info('VIEW INITIALIZED')
