import math

from . import settings
from . import constants
from .settings import WINDOW_WIDTH, WINDOW_HEIGHT, X_MARGIN, Y_MARGIN

def get_all_tile_coords():
    all_coords = []
    for x in range(settings.BOARD_WIDTH):
        for y in range(settings.BOARD_HEIGHT):
            all_coords.append(TileCoords(x, y))
    return all_coords

def top_left_coord_of_tile(coord):
    left = (coord.tile_x * (settings.TILE_SIZE)) + X_MARGIN
    top = (coord.tile_y * (settings.TILE_SIZE)) + Y_MARGIN
    return PixelCoords(left, top)

def get_adjacent_tile_coord(coord, direction):
    if direction == constants.UP:
        adjacent_coord = TileCoords(
            coord.tile_x,
            coord.tile_y + 1
        )
    elif direction == constants.DOWN:
        adjacent_coord = TileCoords(
            coord.tile_x,
            coord.tile_y - 1
        )
    elif direction == constants.LEFT:
        adjacent_coord = TileCoords(
            coord.tile_x + 1,
            coord.tile_y
        )
    elif direction == constants.RIGHT:
        adjacent_coord = TileCoords(
            coord.tile_x - 1,
            coord.tile_y
        )
    else:
        raise Exception('Invalid move input.')
    return adjacent_coord



class PixelCoords(object):
    def __init__(self, x, y):
        self._pixel_x = x
        self._pixel_y = y

    @property
    def pixel_x(self):
        return self._pixel_x

    @property
    def pixel_y(self):
        return self._pixel_y

    def __str__(self):
        return '{}: ({}, {})'.format(self.__class__.__name__, self._pixel_x,
                                     self._pixel_y)


class TileCoords(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._check_tile_is_in_bounds()

    def _check_tile_is_in_bounds(self):
        x_in_bounds = self._x < settings.BOARD_WIDTH  and self._x >= 0
        y_in_bounds = self._y < settings.BOARD_HEIGHT and self._y >= 0
        if not(x_in_bounds and y_in_bounds):
            raise OutOfBoundsException('Coordinate ({}) is out of '
                                       'bounds.'.format((self._x, self._y)))

    def is_next_to(self, other):
        other._check_tile_is_in_bounds()
        x_adjacent = abs(self.tile_x - other.tile_x)
        y_adjacent = abs(self.tile_y - other.tile_y)
        return (x_adjacent or y_adjacent) and not (x_adjacent and y_adjacent)

    @property
    def tile_x(self):
        return self._x

    @property
    def tile_y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __str__(self):
        return '{}: ({}, {})'.format(self.__class__.__name__, self._x, self._y)


class OutOfBoundsException(Exception):
    pass
