from tetromino.pieces.abstractpiece import Piece


class JPiece(Piece):
    _templates = [
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

    def __init__(self):
        super().__init__()
        self._piece_type= 'J'
