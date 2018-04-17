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
        self._first_selection = None

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.ClickEvent):
            self._handle_click(event.coords)
        elif isinstance(event, events.BoxOpenConfirm):
            self._board.reveal(event.coords)
        elif isinstance(event, events.BoxCloseConfirm):
            self._board.cover(event.coords)


    def _handle_click(self, coords):
        if coords.in_a_box:
            if self.is_revealed(coords):
                self._event_manager.post(events.BoxCloseRequest(coords))
            else:
                self._event_manager.post(events.BoxOpenRequest(coords))
                if self._first_selection == None:
                    self._first_selection = self._board.get_icon(coords)
                else:
                    # check for match
                    second_selection = self._board.get_icon(coords)
                    if self._first_selection == second_selection:
                        self._event_manager.post(events.Event())
                    self._first_selection = None

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._event_manager.post(events.InitializeEvent())
        self._event_manager.post(events.NewGameEvent())
        while self._running:
            tick = events.TickEvent()
            self._event_manager.post(tick)
            self._clock.tick(settings.FPS)

    def get_icon(self, coord):
        return self._board.get_icon(coord)

    def is_revealed(self, coord):
        return self._board.is_revealed(coord)
