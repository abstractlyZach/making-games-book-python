import abc
import random


TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5


class Piece(object, metaclass=abc.ABCMeta):
    def get_random_template(self):
        return random.choice(self._templates)

class SPiece(Piece):
    _templates = [
        ['.....',
         '.....',
         '..OO.',
         '.OO..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '...O.',
         '.....']
    ]


class ZPiece(Piece):
    _templates = [
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ]
