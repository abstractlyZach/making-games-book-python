import pygame

from . import board
from . import events
from . import settings
from .pieces import pieces


class Model(object):
    """Tracks the game state."""
    def __init__(self, main_event_manager, input_event_manager):
        self._main_event_manager = main_event_manager
        self._main_event_manager.register_listener(self)
        input_event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.NewGameEvent):
            self._board = board.Board()
        elif isinstance(event, events.KeyPressEvent):
            self._handle_keypress(event)
            random_piece = pieces.get_random_piece()
            self._board.insert(random_piece)


    def get_box_color(self, x, y):
        return self._board.get_box_color(x, y)

    def _handle_keypress(self, event):
        pass

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._main_event_manager.post(events.InitializeEvent())
        self._main_event_manager.post(events.NewGameEvent())
        while self._running:
            tick = events.TickEvent()
            self._main_event_manager.post(tick)
            self._clock.tick(settings.FPS)

