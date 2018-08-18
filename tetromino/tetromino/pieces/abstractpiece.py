import abc
import random

from . import pieces
from .. import constants


class Piece(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self._coord = None
        self._current_rotation = self._get_random_rotation()
        self._color = constants.GREEN

    @property
    def piece_type(self):
        return self._piece_type

    @property
    def shape(self):
        return self._templates[self._current_rotation]

    def is_template_filled_at(self, x, y):
        column = self.shape[pieces.TEMPLATE_HEIGHT - y - 1]
        template_piece = column[x]
        return template_piece != pieces.BLANK

    def _get_random_rotation(self):
        return random.randint(0, len(self._templates) - 1)

    def __str__(self):
        return '\n'.join(self.shape)

    def set_coord(self, box_coord):
        self._coord = box_coord

    @property
    def x(self):
        return self._coord.box_x

    @property
    def y(self):
        return self._coord.box_y

    @property
    def color(self):
        return self._color
