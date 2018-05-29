import time

from . import buttons
from . import constants

class Board(object):
    def __init__(self):
        self._buttons = [
            buttons.Button(constants.YELLOW, constants.BRIGHT_YELLOW),
            buttons.Button(constants.BLUE, constants.BRIGHT_BLUE),
            buttons.Button(constants.RED, constants.BRIGHT_RED),
            buttons.Button(constants.GREEN, constants.BRIGHT_GREEN)
        ]
        self._end_of_last_flash = None

    def get_button(self, color):
        for button in self._buttons:
            if button.original_color == color:
                return button
        raise Exception(f'No such button of color {color}.')

    def update(self):
        for button in self._buttons:
            button.update()
        if not self.is_flashing and self._end_of_last_flash is None:
            self._end_of_last_flash = time.time()

    def flash(self, color):
        button = self.get_button(color)
        button.flash()
        self._end_of_last_flash = None

    @property
    def is_flashing(self):
        for button in self._buttons:
            if button.is_flashing:
                return True
        return False

    @property
    def time_since_last_flash(self):
        return self._end_of_last_flash