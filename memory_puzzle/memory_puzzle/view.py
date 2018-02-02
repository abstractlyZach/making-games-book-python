import logging

import pygame

from . import coords
from . import events
from . import settings


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, event_manager, model):
        event_manager.register_listener(self)
        self._model = model
        self._is_initialized = False
        self._screen = None

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            # ends the pygame graphical display
            pygame.quit()
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.TickEvent):
            self.render_all()

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Memory Game')
        window_dimensions = (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        self._display_surface = pygame.display.set_mode(window_dimensions)
        self._is_initialized = True
        logging.info('View initialized.')

    def render_all(self):
        if not self._is_initialized:
            return
        # draw stuff
        self._display_surface.fill(settings.BG_COLOR)
        for coord in coords.get_all_box_coords():
            self._draw_box_cover(coord, settings.BOX_SIZE)
        pygame.display.update()

    def _draw_box_cover(self, box_coords, coverage):
        if coverage > settings.BOX_SIZE:
            raise Exception
        topleft_corner = coords.top_left_coords_of_box(box_coords)
        if coverage > 0:
            rect_tuple = (topleft_corner.pixel_x, topleft_corner.pixel_y,
                          settings.BOX_SIZE, settings.BOX_SIZE)
            pygame.draw.rect(self._display_surface, settings.BOX_COLOR,
                             rect_tuple)



