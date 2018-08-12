from tetromino.pieces.abstractpiece import Piece


class TPiece(Piece):
    _templates = [
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

    def __init__(self):
        self._piece_type= 'T'
