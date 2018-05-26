
import enum

class ButtonState(enum.Enum):
    BRIGHTENING = 0
    DARKENING = 1
    IDLE = 2



class Button(object):
    def __init__(self, original_color, flash_color):
        self._original_color = original_color
        self._flash_color = flash_color
        self._state = ButtonState.IDLE

    def update(self):
        if self._state is ButtonState.DARKENING:
            pass
        elif self._state is ButtonState.BRIGHTENING:
            pass
