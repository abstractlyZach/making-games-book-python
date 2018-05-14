import copy
import logging
import random
import pygame

from . import events
from . import settings
from . import board
from . import constants

def opposite_direction(direction):
    if direction == constants.RIGHT:
        return constants.LEFT
    elif direction == constants.LEFT:
        return constants.RIGHT
    elif direction == constants.UP:
        return constants.DOWN
    elif direction == constants.DOWN:
        return constants.UP


class Model(object):
    """Tracks the game state."""
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()
        self._board = board.Board()
        self._move_history = []

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.MoveEvent):
            self._handle_move_event(event)
        elif isinstance(event, events.InitializeEvent):
            self.shuffle_tiles()

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._event_manager.post(events.InitializeEvent())
        while self._running:
            tick = events.TickEvent()
            self._event_manager.post(tick)
            self._clock.tick(settings.FPS)

    def get_tile_number(self, coord):
        return self._board.get_tile_number(coord)

    def _handle_move_event(self, event):
        if self._board.is_valid_move(event.direction):
            self._board.make_move(event.direction)
            self._move_history.append(event.direction)
        else:
            logging.error('Invalid move.')

    def get_random_move(self):
        """Returns a random move that doesn't undo the last move."""
        valid_moves = copy.copy(constants.ALL_DIRECTIONS)
        if len(self._move_history) > 0:
            valid_moves.remove(opposite_direction(self._move_history[-1]))
        for move in valid_moves:
            if not self._board.is_valid_move(move):
                valid_moves.remove(move)
        return random.choice(valid_moves)

    def shuffle_tiles(self):
        for i in range(50):
            random_move = self.get_random_move()
            self._event_manager.post(events.MoveEvent(random_move))

