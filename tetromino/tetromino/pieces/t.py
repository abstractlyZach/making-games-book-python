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
        super().__init__()
        self._piece_type= 'T'
