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

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
