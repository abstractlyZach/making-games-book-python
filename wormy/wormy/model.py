import pygame

from . import board
from . import coordinates
from . import events
from . import settings
from . import worm


class Model(object):
    """Tracks the game state."""
    def __init__(self, main_event_manager, input_event_manager):
        self._main_event_manager = main_event_manager
        self._main_event_manager.register_listener(self)
        input_event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()
        self._score = 0

    @property
    def score(self):
        return self._score

    @property
    def worm_coords(self):
        return self._worm.body_coords

    @property
    def apple_coord(self):
        return self._board.apple_coord

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.TickEvent):
            self._worm.move()
        elif isinstance(event, events.DirectionChangeEvent):
            self._worm.change_direction(event.direction)
        elif isinstance(event, events.InitializeEvent):
            head_coordinates = coordinates.Coordinates(5, 5)
            self._worm = worm.Worm(head_coordinates)
            self._board = board.Board()

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._main_event_manager.post(events.InitializeEvent())
        while self._running:
            tick = events.TickEvent()
            self._main_event_manager.post(tick)
            self._clock.tick(settings.FPS)

