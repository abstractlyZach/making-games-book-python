import pygame


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


class PositionalEvent(Event):
    """Superclass for any event that has a coord."""
    def __init__(self, position):
        self._position = position

    @property
    def coords(self):
        return self._position

    def __str__(self):
        return '{}: {}'.format(self._name, self._position)


class ClickEvent(PositionalEvent, InputEvent):
    def __init__(self, position):
        super().__init__(position)
        self._name = 'Click Event'


class MouseMovementEvent(PositionalEvent, InputEvent):
    def __init__(self, position):
        super().__init__(position)
        self._name = 'Mouse Movement Event'


class NewGameEvent(Event):
    def __init__(self):
        self._name = 'New Game Event'

class BoxOpenRequest(PositionalEvent):
    """A request from the model to the view to animate a box opening."""
    def __init__(self, position):
        super().__init__(position)
        self._name = 'Box Open Event'

class BoxCloseRequest(PositionalEvent):
    """A request from the model to the view to animate a box closing."""
    def __init__(self, position):
        super().__init__(position)
        self._name = 'Box Close Event'
