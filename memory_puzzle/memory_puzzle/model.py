import pygame

from . import board
from . import constants
from . import events
from . import settings


class Model(object):
    """Tracks the game state."""
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()
        self._board = board.Board(settings.BOARD_WIDTH,
                                  settings.BOARD_HEIGHT,
                                  constants.ALL_COLORS,
                                  constants.ALL_SHAPES)

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.ClickEvent):
            if event.coords.in_a_box:
                self._board.toggle_reveal(event.coords)

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._event_manager.post(events.InitializeEvent())
        while self._running:
            tick = events.TickEvent()
            self._event_manager.post(tick)
            self._clock.tick(settings.FPS)

    def get_icon(self, coord):
        return self._board.get_icon(coord)

    def is_revealed(self, coord):
        return self._board.is_revealed(coord)
