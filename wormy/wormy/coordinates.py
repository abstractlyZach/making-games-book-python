from . import settings


class Coordinates(object):
    def __init__(self, x, y):
        if isinstance(x, int) and isinstance(y, int):
            self._x = x
            self._y = y
        else:
            raise Exception(f'({self._x}, {self._y}): should both be '
                            f'integers.')
        self._check_in_bounds()

    def _check_in_bounds(self):
        x_in_bounds = self._x >= 0 or \
            self._x <= settings.WINDOW_WIDTH / settings.CELL_SIZE
        y_in_bounds = self._y >= 0 or \
            self._y <= settings.WINDOW_HEIGHT / settings.CELL_SIZE
        if x_in_bounds and y_in_bounds:
            return True
        else:
            raise Exception(f'Coordinates({self._x}, {self._y}) are out of '
                            f'bounds')
