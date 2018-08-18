from . import settings
from . import constants

def get_all_box_coords():
    all_coords = []
    for x in range(settings.BOARD_WIDTH):
        for y in range(settings.BOARD_HEIGHT):
            all_coords.append(BoxCoords(x, y))
    return all_coords

def top_left_coord_of_box(coord):
    left = (coord.box_x * (settings.BOX_SIZE)) + settings.X_MARGIN
    top = (coord.box_y * (settings.BOX_SIZE)) + settings.TOP_MARGIN
    return PixelCoords(left, top)

def get_adjacent_box_coord(coord, direction):
    if direction == constants.UP:
        adjacent_coord = BoxCoords(
            coord.box_x,
            coord.box_y + 1
        )
    elif direction == constants.DOWN:
        adjacent_coord = BoxCoords(
            coord.box_x,
            coord.box_y - 1
        )
    elif direction == constants.LEFT:
        adjacent_coord = BoxCoords(
            coord.box_x + 1,
            coord.box_y
        )
    elif direction == constants.RIGHT:
        adjacent_coord = BoxCoords(
            coord.box_x - 1,
            coord.box_y
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


class BoxCoords(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        # self._check_box_is_in_bounds()

    # def _check_box_is_in_bounds(self):
    #     x_in_bounds = self._x < settings.BOARD_WIDTH  and self._x >= 0
    #     y_in_bounds = self._y < settings.BOARD_HEIGHT and self._y >= 0
    #     if not(x_in_bounds and y_in_bounds):
    #         raise OutOfBoundsException('Coordinate ({}) is out of '
    #                                    'bounds.'.format(self._x, self._y))

    def is_next_to(self, other):
        x_adjacent = abs(self.box_x - other.box_x) == 1 \
                     and self.box_y == other.box_y
        y_adjacent = abs(self.box_y - other.box_y) == 1 \
                     and self.box_x == other.box_x
        return x_adjacent or y_adjacent

    @property
    def box_x(self):
        return self._x

    @property
    def box_y(self):
        return self._y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __str__(self):
        return '{}: ({}, {})'.format(self.__class__.__name__, self._x, self._y)


class OutOfBoundsException(Exception):
    pass
