
import enum
from . import settings

class ButtonState(enum.Enum):
    BRIGHTENING = 0
    DARKENING = 1
    IDLE = 2



class Button(object):
    def __init__(self, original_color, flash_color):
        self._original_color = original_color
        self._flash_color = flash_color
        self._state = ButtonState.IDLE
        self._brightness_alpha = 0

    @property
    def original_color(self):
        return self._original_color

    @property
    def flash_color(self):
        return self._flash_color

    @property
    def is_flashing(self):
        return self._state is ButtonState.BRIGHTENING or \
            self._state is ButtonState.DARKENING

    @property
    def brightness_alpha(self):
        return self._brightness_alpha

    def flash(self):
        self._state = ButtonState.BRIGHTENING

    def update(self):
        if self._state is ButtonState.DARKENING:
            self._darken()
        elif self._state is ButtonState.BRIGHTENING:
            self._brighten()

    def _darken(self):
        self._brightness_alpha -= settings.ANIMATION_SPEED
        if self._brightness_alpha <= 0:
            self._brightness_alpha = 0
            self._state = ButtonState.IDLE

    def _brighten(self):
        self._brightness_alpha += settings.ANIMATION_SPEED
        if self._brightness_alpha >= 255:
            self._brightness_alpha = 255
            self._state = ButtonState.DARKENING


