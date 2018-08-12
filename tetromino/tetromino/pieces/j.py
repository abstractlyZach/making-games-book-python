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
        self._piece_type= 'J'
