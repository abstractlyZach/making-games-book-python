from tetromino.pieces.abstractpiece import Piece


class LPiece(Piece):
    _templates = [
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

    def __init__(self):
        self._piece_type= 'L'
