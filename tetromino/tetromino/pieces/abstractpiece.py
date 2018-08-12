import abc
import random


class Piece(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self._current_rotation = \
            random.randint(0, len(self._get_templates()) - 1)
        self._current_template = self._get_templates()[self._current_rotation]

    @property
    def piece_type(self):
        return self._piece_type

    def _get_templates(self):
        return self._templates

