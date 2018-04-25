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
        """Handle incoming events."""
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

        self.check_win_condition()

    def _handle_selection(self, coords):
        """Handles a box being selected."""
        self._board.reveal(coords)
        if self._first_selection == None:
            self._first_selection = coords
            self._close_first_selection_event = events.BoxCloseRequest(coords)
        else:
            self._handle_second_selection(coords)

    def _handle_second_selection(self, coords):
        """Checks that the second selection isn't the first selection
        clicked twice and then compares the icons in the selections."""
        if coords != self._first_selection:
            self._compare_selections(coords)
            self._first_selection = None

    def _compare_selections(self, second_selection):
        """Compare the selections and perform the proper action depending
        on the results of the comparation."""
        first_icon = self._board.get_icon(self._first_selection)
        second_icon = self._board.get_icon(second_selection)
        if first_icon == second_icon:
            self._handle_match(first_icon)
        else:
            self._handle_no_match(second_selection)

    def _handle_match(self, icon):
        """Post a match event."""
        self._event_manager.post(events.MatchEvent(icon))

    def _handle_no_match(self, second_coords):
        """Pause animations and then close the selections."""
        self._event_manager.post(events.AnimationPause(.5))
        self._event_manager.post(events.BoxCloseRequest(second_coords))
        self._event_manager.post(self._close_first_selection_event)

    def _handle_click(self, coords):
        """Try to open a box at the coords."""
        openable = coords.in_a_box and not self.is_revealed(coords)
        if openable:
            self._event_manager.post(events.BoxOpenRequest(coords))

    def _handle_game_over(self):
        """Handle the game over event."""
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
        """Get the icon at the coord."""
        return self._board.get_icon(coord)

    def is_revealed(self, coord):
        """Return True if the box at the coord is revealed."""
        return self._board.is_revealed(coord)

    def check_win_condition(self):
        """Check to see if the player has won."""
        if self._board.are_all_revealed():
            self._event_manager.post(events.GameOverEvent())
