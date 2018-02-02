import logging

import pygame

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
        pygame.display.set_caption('demo game')
        self._screen = pygame.display.set_mode((600, 60))
        self._small_font = pygame.font.Font(None, 40)
        self._is_initialized = True
        logging.info('View initialized.')

    def render_all(self):
        if not self._is_initialized:
            return
        # draw stuff
        pygame.display.update()

