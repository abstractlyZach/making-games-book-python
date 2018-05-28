import pygame

from . import events
from . import settings
from . import board
from . import constants
from simon import soundboard


class Model(object):
    """Tracks the game state."""
    def __init__(self, main_event_manager, input_event_manager):
        self._main_event_manager = main_event_manager
        self._main_event_manager.register_listener(self)
        input_event_manager.register_listener(self)
        self._running = False
        self._clock = pygame.time.Clock()
        self._board = board.Board()

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.TickEvent):
            self._board.update()
        elif isinstance(event, events.ButtonPressEvent):
            self.flash(event.color)

    def run(self):
        """Starts the game loop. Pumps a tick into the event manager for
        each loop."""
        self._running = True
        self._main_event_manager.post(events.InitializeEvent())
        while self._running:
            tick = events.TickEvent()
            self._main_event_manager.post(tick)
            self._clock.tick(settings.FPS)

    def flash(self, color):
        """Handle the details of doing a flash."""
        self._board.flash(color)
        color_index = constants.BASIC_COLORS.index(color)
        self._main_event_manager.post(events.SoundEvent(color_index))


    def get_flashing_buttons(self):
        flashing_buttons = list()
        for color in constants.BASIC_COLORS:
            button = self._board.get_button(color)
            if button.is_flashing:
                flashing_buttons.append(button)
        return flashing_buttons
