import abc
import random


class Piece(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self._current_rotation = self._get_random_rotation()

    @property
    def piece_type(self):
        return self._piece_type

    @property
    def shape(self):
        return self._templates[self._current_rotation]

    def _get_random_rotation(self):
        return random.randint(0, len(self._templates) - 1)

    def __str__(self):
        return '\n'.join(self.shape)



