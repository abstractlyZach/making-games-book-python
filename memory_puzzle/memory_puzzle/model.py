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
        self._won = False

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.ClickEvent):
            self._handle_click(event.coords)
        elif isinstance(event, events.BoxOpenConfirm):
            self._handle_selection(event.coords)
        elif isinstance(event, events.BoxCloseConfirm):
            self._board.cover(event.coords)
        elif isinstance(event, events.GameOverEvent):
            self._handle_game_over()

        if not self._won:
            self.check_win_condition()

    def _handle_selection(self, coords):
        self._board.reveal(coords)
        if self._first_selection == None:
            self._first_selection = coords
            self._close_first_selection_event = events.BoxCloseRequest(coords)
        else:
            if coords == self._first_selection:
                pass
            else:
                first_icon = self._board.get_icon(self._first_selection)
                second_icon = self._board.get_icon(coords)
                if first_icon == second_icon:
                    self._event_manager.post(events.MatchEvent(first_icon))
                else:
                    self._event_manager.post(events.AnimationPause(.5))
                    self._event_manager.post(events.BoxCloseRequest(coords))
                    self._event_manager.post(self._close_first_selection_event)
                self._first_selection = None

    def _handle_click(self, coords):
        openable = coords.in_a_box and not self.is_revealed(coords)
        if openable:
            self._event_manager.post(events.BoxOpenRequest(coords))

    def _handle_game_over(self):
        pass

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

    def check_win_condition(self):
        if self._board.are_all_revealed():
            print('you won!')
            self._won = True
