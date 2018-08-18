import random

from . import i
from . import j
from . import l
from . import o
from . import s
from . import t
from . import z


BLANK = '.'

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

ALL_PIECE_CLASSES = [
    i.IPiece,
    j.JPiece,
    l.LPiece,
    o.OPiece,
    s.SPiece,
    t.TPiece,
    z.ZPiece,
]


def get_random_piece():
    random_class = random.choice(ALL_PIECE_CLASSES)
    return random_class()
