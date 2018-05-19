import copy
import logging
import random
import pygame

from . import events
from . import coords
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
    def __init__(self, general_event_manager):
        self._event_manager = general_event_manager
        self._event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()
        self._solved_board = board.Board()

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._event_manager.post(events.InitializeEvent())
        while self._running:
            tick = events.TickEvent()
            self._event_manager.post(tick)
            self._clock.tick(settings.FPS)

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.TickEvent):
            self._handle_tick()
        elif isinstance(event, events.MoveEvent):
            self._handle_move_event(event)
        elif isinstance(event, events.InitializeEvent):
            self.new_game()
        elif isinstance(event, events.ResetEvent):
            self.reset()
        elif isinstance(event, events.SolveEvent):
            self.solve()
        elif isinstance(event, events.NewGameEvent):
            self.new_game()

    def _handle_tick(self):
        self._board.update()
        if not self._board.sliding and len(self._move_queue) > 0:
            move = self._move_queue.pop(0)
            self._start_move(move)
        if self._board == self._solved_board:
            self._is_solved = True
        else:
            self._is_solved = False

    def _handle_move_event(self, event):
        self._move_queue.append(event)

    def _start_move(self, move_event):
        direction = move_event.direction
        should_record = move_event.record_move
        is_player_move = move_event.player_move
        if self._board.is_valid_move(direction):
            self._board.begin_move(direction)
            if should_record:
                self._record_move(direction, is_player_move)
        else:
            logging.error(f'invalid move: {direction}')

    def _record_move(self, direction, is_player_move):
        if is_player_move:
            self._player_move_history.append(direction)
        else:
            self._puzzle_move_history.append(direction)

    def get_tile(self, coord):
        return self._board.get_tile(coord)

    def get_tile_number(self, coord):
        return self._board.get_tile(coord).number

    def get_random_move(self, board, move_history):
        """Returns a random move that doesn't undo the last move."""
        valid_moves = copy.copy(constants.ALL_DIRECTIONS)
        invalid_moves = []
        if len(move_history) > 0:
            valid_moves.remove(opposite_direction(move_history[-1]))
        for move in valid_moves:
            if not board.is_valid_move(move):
                invalid_moves.append(move)
        for invalid_move in invalid_moves:
            valid_moves.remove(invalid_move)
        return random.choice(valid_moves)

    def new_game(self):
        self._board = board.Board()
        self._puzzle_move_history = list()
        self._player_move_history = list()
        self._move_queue = list()
        self._is_solved = False
        # self.shuffle_tiles()

    def shuffle_tiles(self):
        copied_board = self._board.copy()
        move_history = list()
        for i in range(50):
            random_move = self.get_random_move(copied_board, move_history)
            self._event_manager.post(events.MoveEvent(random_move,
                                                      player_move=False))
            copied_board.make_move(random_move)
            move_history.append(random_move)

    def reset(self):
        moves_to_reset = copy.copy(self._player_move_history)
        while len(moves_to_reset) > 0:
            move = moves_to_reset.pop()
            opposite_move = opposite_direction(move)
            self._event_manager.post(events.MoveEvent(opposite_move,
                                                      record_move=False))
        self._player_move_history = list()

    def solve(self):
        moves_to_reset = copy.copy(self._puzzle_move_history) \
            + copy.copy(self._player_move_history)
        while len(moves_to_reset) > 0:
            move = moves_to_reset.pop()
            opposite_move = opposite_direction(move)
            self._event_manager.post(events.MoveEvent(opposite_move,
                                                      record_move=False))
        self._player_move_history = list()
        self._puzzle_move_history = list()

    @property
    def is_solved(self):
        return self._is_solved
