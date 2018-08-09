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


class IPiece(Piece):
    _templates = [
        ['..O..',
         '..O..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         'OOOO.',
         '.....',
         '.....']
    ]


class OPiece(Piece):
    _template = [
        ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']
    ]


class JPiece(Piece):
    _template = [
        ['.....',
         '.O...',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '..OO.',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '...O.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '.OO..',
         '.....']
    ]

class LPiece(Piece):

    _template = [
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..OO.',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....']
    ]


class TPiece(Piece):
    _template = [
        ['.....',
         '..O..',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....']
    ]
