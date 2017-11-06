from memory_puzzle import BOX_SIZE
from memory_puzzle import GAP_SIZE
from memory_puzzle import X_MARGIN
from memory_puzzle import Y_MARGIN


class Coords(object):
    @property
    def x(self):
        pass

    @property
    def y(self):
        pass


class PixelCoords(Coords):
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._box_x = None
        self._box_y = None

    @property
    def pixel_x(self):
        return self._x

    @property
    def pixel_y(self):
        return self._y

    @property
    def box_x(self):
        if not self._box_x:
            self._calculate_box_x()
        return self._box_x

    def _calculate_box_x(self):
        pixel_on_board = self._x - X_MARGIN


    @property
    def box_y(self):
        if not self._box_y:
            self._calculate_box_y()
        return self._box_y

    def _calculate_box_y(self):
        pass


class BoxCoords(Coords):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def box_x(self):
        return self._x

    @property
    def box_y(self):
        return self._y
