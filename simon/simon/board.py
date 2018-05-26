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

    def get_button(self, color):
        for button in self._buttons:
            if button.original_color == color:
                return button
        raise Exception(f'No such button of color {color}.')

    def update(self):
        for button in self._buttons:
            button.update()