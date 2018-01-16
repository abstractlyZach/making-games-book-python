import math

import settings
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BOX_SIZE, GAP_SIZE, X_MARGIN, Y_MARGIN

def get_all_box_coords():
    all_coords = []
    for x in range(settings.BOARD_WIDTH):
        for y in range(settings.BOARD_HEIGHT):
            all_coords.append(BoxCoords(x, y))
    return all_coords

def top_left_coords_of_box(coords):
    left = (coords.box_x * (BOX_SIZE + GAP_SIZE)) + X_MARGIN + int(GAP_SIZE
                                                                   / 2)
    top = (coords.box_y * (BOX_SIZE + GAP_SIZE)) + Y_MARGIN + int(GAP_SIZE / 2)
    return PixelCoords(left, top)


class PixelCoords(object):
    def __init__(self, x, y):
        self._pixel_x = x
        self._pixel_y = y
        self._box_x = None
        self._box_y = None

    @property
    def pixel_x(self):
        return self._pixel_x

    @property
    def pixel_y(self):
        return self._pixel_y

    @property
    def box_x(self):
        if self._box_x is None:
            self._calculate_box_x()
        return self._box_x

    def _calculate_box_x(self):
        if not self._x_is_in_bounds():
            return
        pixel_position_on_board = self._pixel_x - X_MARGIN
        container_x = math.floor(pixel_position_on_board / (BOX_SIZE + GAP_SIZE))
        distance_from_container_boundaries = pixel_position_on_board % (BOX_SIZE + GAP_SIZE)
        box_distance_from_container_bounds = GAP_SIZE / 2
        left_side_in_box = distance_from_container_boundaries > \
                           box_distance_from_container_bounds
        right_side_in_box = distance_from_container_boundaries < \
                            (BOX_SIZE + GAP_SIZE) - box_distance_from_container_bounds
        if left_side_in_box and right_side_in_box:
            self._box_x = container_x
        else:
            return

    def _x_is_in_bounds(self):
        if self._pixel_x <= X_MARGIN:
            return False
        elif self._pixel_x >= WINDOW_WIDTH - X_MARGIN:
            return False
        else:
            return True

    @property
    def box_y(self):
        if self._box_y is None:
            self._calculate_box_y()
        return self._box_y

    def _calculate_box_y(self):
        if not self._y_is_in_bounds():
            return
        pixel_position_on_board = self._pixel_y - Y_MARGIN
        container_y = math.floor(pixel_position_on_board / (BOX_SIZE + GAP_SIZE))
        distance_from_container_boundaries = pixel_position_on_board % (BOX_SIZE + GAP_SIZE)
        box_distance_from_container_bounds = GAP_SIZE / 2
        top_side_in_box = distance_from_container_boundaries > \
                           box_distance_from_container_bounds
        bottom_side_in_box = distance_from_container_boundaries < \
                            (BOX_SIZE + GAP_SIZE) - box_distance_from_container_bounds
        if top_side_in_box and bottom_side_in_box:
            self._box_y = container_y
        else:
            return

    def _y_is_in_bounds(self):
        if self._pixel_y <= Y_MARGIN:
            return False
        elif self._pixel_y >= WINDOW_HEIGHT- Y_MARGIN:
            return False
        else:
            return True


class BoxCoords(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def box_x(self):
        return self._x

    @property
    def box_y(self):
        return self._y
