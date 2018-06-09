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
        self._crashed = False

    def __len__(self):
        return len(self._body)

    @property
    def head_coord(self):
        return self._body[0]

    @property
    def crashed(self):
        return self._crashed

    @property
    def body_coords(self):
        return self._body

    def move(self):
        if self._crashed:
            raise Exception('Worm is crashed. Cannot make move.')
        self._move_head(self._direction)
        self._phantom_tail = self._body.pop(-1)
        self._check_for_self_collision()

    def _move_head(self, direction):
        new_head_coordinates = coordinates.coord_in_direction(
            self.head_coord,
            direction
        )
        if new_head_coordinates.is_in_bounds:
            self._body.insert(0, new_head_coordinates)
        else:
            self._crashed = True

    def _check_for_self_collision(self):
        for coord in self._body[1:]:
            if self.head_coord == coord:
                self._crashed = True

    def eat_apple(self):
        """Adds the tail back onto the worm. Should be triggered after the
        worm eats an apple. Make sure this is triggered after it has moved."""
        self._body.append(self._phantom_tail)


