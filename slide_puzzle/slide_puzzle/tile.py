from . import constants
from . import settings

class Tile(object):
    def __init__(self, number):
        self._number = number
        self._is_sliding = False
        self._x_delta = 0
        self._y_delta = 0

    @property
    def number(self):
        return self._number

    @property
    def is_sliding(self):
        return self._is_sliding

    def slide(self, direction):
        self._is_sliding = True
        self._x_velocity = 0
        self._y_velocity = 0
        if direction == constants.UP:
            self._y_velocity = -settings.ANIMATION_SPEED
        elif direction == constants.DOWN:
            self._y_velocity = settings.ANIMATION_SPEED
        elif direction == constants.LEFT:
            self._x_velocity = -settings.ANIMATION_SPEED
        elif direction == constants.RIGHT:
            self._x_velocity = settings.ANIMATION_SPEED

    def update(self):
        if self._is_sliding:
            self._move_tile()
            self._check_for_slide_end()

    def _move_tile(self):
        self._x_delta += self._x_velocity
        self._y_delta += self._y_delta

    def _check_for_slide_end(self):
        x_animation_complete = abs(self._x_delta) >= settings.TILE_SIZE
        y_animation_complete = abs(self._y_delta) >= settings.TILE_SIZE
        if x_animation_complete or y_animation_complete:
            self._is_sliding = False

