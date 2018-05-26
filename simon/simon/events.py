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


class SoundEvent(Event):
    def __init__(self, id):
        self._id = id
        self._name = f'Sound Event: {id}'

    @property
    def id(self):
        return self._id

class SetRectEvent(Event):
    def __init__(self, color, rect):
        self._color = color
        self._rect = rect
        self._name = f'Set {constants.COLOR_NAMES[color]} rect at {rect}.'

    @property
    def color(self):
        return self._color

    @property
    def rect(self):
        return self._rect


class ButtonPressEvent(Event):
    def __init__(self, color):
        self._color = color
        self._name = f'{constants.COLOR_NAMES[color].capitalize()} ' \
                     f'button pressed.'

    @property
    def color(self):
        return self._color

