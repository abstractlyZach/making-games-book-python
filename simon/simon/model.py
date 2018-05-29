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
        self._sequence = list()
        self._awaiting_input = False
        self._flash_queue = list()
        self._score = 0

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._running = False
        elif isinstance(event, events.TickEvent):
            self._update()
        elif isinstance(event, events.ButtonPressEvent):
            if self._awaiting_input:
                self.flash(event.color)
                self._sequence.append(event.color)

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

    def play_sequence(self):
        for button_color in self._sequence:
            self._flash_queue.append(button_color)

    def _update(self):
        self._board.update()
        if self._awaiting_input:
            pass
        elif len(self._flash_queue) > 0:
            time_since_last_flash = self._board.time_since_last_flash
            if time_since_last_flash is not None:
                is_time_to_flash = time_since_last_flash >= settings.FLASH_DELAY
                if is_time_to_flash:
                    button_color = self._flash_queue.pop(0)
                    self.flash(button_color)

    @property
    def score(self):
        return self._score

