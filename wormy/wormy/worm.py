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

    @property
    def head_coord(self):
        return self._body[0]

    def move(self, direction):
        self._move_head(direction)
        self._body.pop(-1)

    def _move_head(self, direction):
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
        current_head_coordinates = self._body[0]
        new_head_coordinates = coordinates.Coordinates(
            current_head_coordinates.x + x_delta,
            current_head_coordinates.y + y_delta
        )
        self._body.insert(0, new_head_coordinates)

    def move_and_eat_apple(self, direction):
        self._move_head(direction)


