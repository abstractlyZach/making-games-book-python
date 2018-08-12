from tetromino.pieces.abstractpiece import Piece


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

    def __init__(self):
        super().__init__()
        self._piece_type= 'Z'
