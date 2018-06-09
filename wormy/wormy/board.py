from . import coordinates


class Board(object):
    def __init__(self):
        self._spawn_apple()

    def _spawn_apple(self):
        self._apple_coord = coordinates.get_random_coord()

    def despawn_apple(self):
        self._spawn_apple()

    @property
    def apple_coord(self):
        return self._apple_coord
