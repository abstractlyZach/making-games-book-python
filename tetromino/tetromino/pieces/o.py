from tetromino.pieces.abstractpiece import Piece


class OPiece(Piece):
    _templates = [
        ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']
    ]

    def __init__(self):
        super().__init__()
        self._piece_type= 'O'
