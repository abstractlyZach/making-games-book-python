from . import coords
from . import constants
from . import settings
from .pieces import pieces


class Board(object):
    def __init__(self):
        """
        +------------------------+
        |  ...         ...       |
        | (0,4) ...   (2,4) ...  |
        | (0,3)                  |
        | (0,2)        ...       |
        | (0,1)                  |
        | (0,0) (1,0) (2,0) ...  |
        +------------------------+
        coordinates are (x, y)
        """
        self._board = [
            [constants.WHITE
             for column in range(settings.BOARD_WIDTH)]
            for row in range(settings.BOARD_HEIGHT)
        ]
        self._pieces = list()

    def get_box_color(self, x, y):
        return self._board[y][x]

    def _set_box_color(self, coord, color):
        print(coord)
        print('setting box color')
        self._board[coord.box_y][coord.box_x] = color

    def insert(self, piece):
        starting_x = int(settings.BOARD_WIDTH / 2)
        starting_y = (settings.BOARD_HEIGHT - 4)
        starting_coord = coords.BoxCoords(starting_x, starting_y)
        piece.set_coord(starting_coord)
        self._pieces.append(piece)
        self._add_piece_color_to_board(piece)

    def _update_colors(self):
        for piece in self._pieces:
            self._add_piece_color_to_board(piece)

    def _add_piece_color_to_board(self, piece):
        for x in range(pieces.TEMPLATE_WIDTH):
            for y in range(pieces.TEMPLATE_HEIGHT):
                if piece.is_template_filled_at(x, y):
                    box_coord = coords.BoxCoords(x + piece.x, y + piece.y)
                    print('coloring box: {}'.format(box_coord))
                    if box_coord.box_y < settings.BOARD_HEIGHT:
                        self._set_box_color(box_coord, piece.color)
