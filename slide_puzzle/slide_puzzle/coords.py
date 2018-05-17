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
    #     self._calculate_box_x()
    #     self._calculate_box_y()
    #
    # def _calculate_box_x(self):
    #     self._check_x_is_in_board_bounds()
    #     if self._x_out_of_bounds:
    #         self._box_x = None
    #     else:
    #         self._check_x_within_board()
    #
    # def _check_x_is_in_board_bounds(self):
    #     in_left_margin = self._pixel_x <= X_MARGIN
    #     in_right_margin = self._pixel_x >= WINDOW_WIDTH - X_MARGIN
    #     if in_left_margin or in_right_margin:
    #         self._x_out_of_bounds = True
    #     else:
    #         self._x_out_of_bounds = False
    #
    # def _check_x_within_board(self):
    #     pixel_position_on_board = self._pixel_x - X_MARGIN
    #     container_x = math.floor(pixel_position_on_board / (BOX_SIZE + GAP_SIZE))
    #     if self._pixel_position_is_within_box_area(pixel_position_on_board):
    #         self._box_x = container_x
    #     else:
    #         self._box_x = None
    #
    # def _pixel_position_is_within_box_area(self, pixel_position):
    #     distance_from_container_boundaries = pixel_position % \
    #                                          (BOX_SIZE + GAP_SIZE)
    #     box_distance_from_container_bounds = GAP_SIZE / 2
    #     before_box = distance_from_container_boundaries > \
    #                        box_distance_from_container_bounds
    #     after_box = distance_from_container_boundaries < \
    #                         (BOX_SIZE + GAP_SIZE) - \
    #                         box_distance_from_container_bounds
    #     return before_box and after_box
    #
    #
    # def _calculate_box_y(self):
    #     self._check_y_is_in_board_bounds()
    #     if self._y_out_of_bounds:
    #         self._box_y = None
    #     else:
    #         self._check_y_within_board()
    #
    # def _check_y_within_board(self):
    #     pixel_position_on_board = self._pixel_y - Y_MARGIN
    #     container_y = math.floor(pixel_position_on_board / (BOX_SIZE + GAP_SIZE))
    #     if self._pixel_position_is_within_box_area(pixel_position_on_board):
    #         self._box_y = container_y
    #     else:
    #         self._box_y = None
    #
    # def _check_y_is_in_board_bounds(self):
    #     in_top_margin = self._pixel_y <= Y_MARGIN
    #     in_bottom_margin = self._pixel_y >= WINDOW_HEIGHT - Y_MARGIN
    #     if in_top_margin or in_bottom_margin:
    #         self._y_out_of_bounds = True
    #     else:
    #         self._y_out_of_bounds = False

    @property
    def pixel_x(self):
        return self._pixel_x

    @property
    def pixel_y(self):
        return self._pixel_y

    @property
    def tile_x(self):
        return self._tile_x

    @property
    def tile_y(self):
        return self._tile_y

    @property
    def in_a_box(self):
        return (self.tile_x is not None) and (self.tile_y is not None)

    def __str__(self):
        return '{}: ({}, {})'.format(self.__class__.__name__, self._pixel_x,
                                     self._pixel_y)

    @property
    def box_coords_str(self):
        if self.in_a_box:
            return '({}, {})'.format(self.tile_x, self.tile_y)
        else:
            return 'Not in a box.'



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
