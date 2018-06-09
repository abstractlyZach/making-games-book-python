import math
import random

from . import constants
from . import settings


def get_top_left_of_coord(coord):
    return PixelCoordinates(coord.x * settings.CELL_SIZE,
                            coord.y * settings.CELL_SIZE)

def coord_in_direction(original_coord, direction):
    x_delta, y_delta = deltas_for_direction(direction)
    new_coord = Coordinates(
        original_coord.x + x_delta,
        original_coord.y + y_delta
    )
    return new_coord


def deltas_for_direction(direction):
    x_delta = 0
    y_delta = 0
    if direction == constants.RIGHT:
        x_delta = 1
    elif direction == constants.LEFT:
        x_delta = -1
    elif direction == constants.UP:
        y_delta = -1
    elif direction == constants.DOWN:
        y_delta = 1
    else:
        raise Exception(f'Invalid direction: {direction}')
    return x_delta, y_delta


def get_all_coords():
    all_coords = []
    horizontal_cells = math.floor(settings.WINDOW_WIDTH / settings.CELL_SIZE)
    vertical_cells = math.floor(settings.WINDOW_HEIGHT / settings.CELL_SIZE)
    for x in range(horizontal_cells):
        for y in range(vertical_cells):
            all_coords.append(Coordinates(x, y))
    return all_coords


def get_random_coord(exception_list=None):
    eligible_coords = get_all_coords()
    if exception_list is not None:
        for exception_coord in exception_list:
            eligible_coords.remove(exception_coord)
    return random.choice(eligible_coords)


class Coordinates(object):
    def __init__(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            self._x = x
            self._y = y
        else:
            raise Exception(f'({self._x}, {self._y}): should both be '
                            f'integers.')

    @property
    def is_in_bounds(self):
        x_in_bounds = self._x >= 0 and \
            self._x <= (settings.WINDOW_WIDTH / settings.CELL_SIZE)
        y_in_bounds = self._y >= 0 and \
            self._y <= (settings.WINDOW_HEIGHT / settings.CELL_SIZE)
        return x_in_bounds and y_in_bounds

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y


class PixelCoordinates(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def pixel_x(self):
        return self._x

    @property
    def pixel_y(self):
        return self._y
