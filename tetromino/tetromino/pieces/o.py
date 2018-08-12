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
        self._piece_type= 'O'
