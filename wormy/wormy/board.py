from . import coordinates


class Board(object):
    def __init__(self):
        self._apple_coords = set()

    def spawn_apple(self, coord):
        if coord.is_in_bounds:
            self._apple_coords.add(coord)
        else:
            raise Exception('Cannot spawn apple out of bounds.')

    def despawn_apple(self, coord):
        self._apple_coords.remove(coord)

    def is_apple_at_coord(self, coord):
        return coord in self._apple_coords
