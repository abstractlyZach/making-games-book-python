from tetromino.pieces.abstractpiece import Piece


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

    def __init__(self):
        super().__init__()
        self._piece_type= 'S'
