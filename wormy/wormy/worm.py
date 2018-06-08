from . import constants
from . import coordinates


class Worm(object):
    def __init__(self, head_coord):
        self._direction = constants.RIGHT
        self._body = [
            head_coord,
            coordinates.Coordinates(head_coord.x - 1, head_coord.y),
            coordinates.Coordinates(head_coord.x - 2, head_coord.y)
        ]

    def __len__(self):
        return len(self._body)


