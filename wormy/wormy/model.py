import pygame

from . import board
from . import coordinates
from . import events
from . import game_states
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
        self._game_state = game_states.GameState('start_screen')

    @property
    def game_state(self):
        return self._game_state

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
        if self._game_state is game_states.GameState.start_screen:
            self._handle_event_during_start_screen(event)
        else:
            self._handle_event_during_gameplay(event)

    def _handle_event_during_start_screen(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.KeyPressEvent):
            self._game_state = game_states.GameState.play_mode
            self._main_event_manager.post(events.NewGameEvent())
        elif isinstance(event, events.DirectionChangeEvent):
            self._game_state = game_states.GameState.play_mode
            self._main_event_manager.post(events.NewGameEvent())

    def _handle_event_during_gameplay(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.TickEvent):
            self._handle_tick()
        elif isinstance(event, events.DirectionChangeEvent):
            self._worm.change_direction(event.direction)
        elif isinstance(event, events.NewGameEvent):
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

    def _handle_tick(self):
        if not self._worm.crashed:
            self._worm.move()
            if self._worm.head_coord == self._board.apple_coord:
                self._board.despawn_apple()
                self._worm.eat_apple()
                self._score += 1
        else:
            raise Exception('woops crashed.')

