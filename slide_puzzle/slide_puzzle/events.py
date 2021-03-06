import pygame
from . import constants


class Event(object):
    """Superclass for events."""
    def __init__(self):
        self._name = 'Generic Event'

    def __str__(self):
        return self._name


class InitializeEvent(Event):
    def __init__(self):
        self._name = 'Initialize Event'


class QuitEvent(Event):
    """Event created when user quits the program."""
    def __init__(self):
        self._name = 'Quit Event'


class TickEvent(Event):
    """Event for every tick of the model."""
    def __init__(self):
        self._name = 'Tick Event'


class InputEvent(Event):
    """Event created when user gives input."""
    def __init__(self):
        self._name = 'Input Event'


class KeyPressEvent(InputEvent):
    def __init__(self, key):
        self._name = 'Key Press Event'
        self._key = key

    def __str__(self):
        key_name = pygame.key.name(self._key)
        return '{}: {}'.format(self._name, key_name)

    @property
    def key(self):
        return self._key


class ClickEvent(InputEvent):
    def __init__(self, position):
        self._name = 'Click Event'
        self._position = position

    @property
    def position(self):
        return self._position

    def __str__(self):
        return '{}: {}'.format(self._name, self._position)


class MoveEvent(Event):
    def __init__(self, direction, player_move=True, record_move=True):
        self._name = f'{direction} Move Event'
        self._record_move = record_move
        self._player_move = player_move
        if direction in constants.ALL_DIRECTIONS:
            self._direction = direction
        else:
            raise Exception(f'{direction} is not a direction.')

    @property
    def direction(self):
        return self._direction

    @property
    def record_move(self):
        return self._record_move

    @property
    def player_move(self):
        return self._player_move


class ResetEvent(Event):
    def __init__(self):
        self._name = f'Reset Event'


class SolveEvent(Event):
    def __init__(self):
        self._name = 'Solve Event'


class NewGameEvent(Event):
    def __init__(self):
        self._name = 'New Game Event'



class SetRectEvent(Event):
    def __init__(self, rectangle):
        self._rectangle = rectangle

    @property
    def rectangle(self):
        return self._rectangle


class SetResetRect(SetRectEvent):
    def __init__(self, rectangle):
        self._name = 'Setting Reset Rectangle Event'
        super().__init__(rectangle)


class SetSolveRect(SetRectEvent):
    def __init__(self, rectangle):
        self._name = 'Setting Solve Rectangle Event'
        super().__init__(rectangle)

class SetNewGameRect(SetRectEvent):
    def __init__(self, rectangle):
        self._name = 'Setting New Game Rectangle Event'
        super().__init__(rectangle)
