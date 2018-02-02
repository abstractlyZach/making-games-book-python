import logging

import pygame

from . import settings
from . import events


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
        pygame.display.update()

