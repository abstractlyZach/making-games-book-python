import abc
import random


class Piece(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    def get_random_template(self):
        return random.choice(self._templates)

    @property
    def piece_type(self):
        return self._piece_type