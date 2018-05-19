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

    def __str__(self):
        return '{}: {}'.format(self._name, self._position)


class MoveEvent(Event):
    def __init__(self, direction):
        self._name = f'{direction} Move Event'
        if direction in constants.ALL_DIRECTIONS:
            self._direction = direction
        else:
            raise Exception(f'{direction} is not a direction.')

    @property
    def direction(self):
        return self._direction


class ResetEvent(Event):
    def __init__(self):
        self._name = f'Reset Event'


class SetResetRect(Event):
    def __init__(self, rectangle):
        self._name = 'Setting Reset Rectangle Event'
        self._rectangle = rectangle

    @property
    def rectangle(self):
        return self._rectangle
