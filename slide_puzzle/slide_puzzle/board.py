from . import constants
from . import coords
from . import settings

class Board(object):
    """
    Sliding puzzle board object. Its coordinates look like this:

                                 |
    x-axis -->            y-axis v
    -------------------
    |(0,0)|(1,0)|(2,0)|
    +-----+-----+-----+
    |(0,1)|(1,1)|(2,1)|
    +-----+-----+-----+
    ...
    -------------------
    """
    def __init__(self, board=None):
        if board is None:
            self._create_new_board()
        else:
            self._board = board

    def _create_new_board(self):
        current_number = 1
        self._board = []
        for y in range(settings.BOARD_HEIGHT):
            row = []
            for x in range(settings.BOARD_WIDTH):
                row.append(current_number)
                current_number += 1
            self._board.append(row)
        self._board[-1][-1] = constants.BLANK

    def get_tile_number(self, coord):
        return self._board[coord.tile_y][coord.tile_x]

    def get_blank_tile_coord(self):
        for coord in coords.get_all_tile_coords():
            if self.get_tile_number(coord) == constants.BLANK:
                return coord

    def make_move(self, move):
        blank_tile_coord = self.get_blank_tile_coord()
        if move == constants.UP:
            sliding_tile_coord = coords.TileCoords(
                blank_tile_coord.tile_x,
                blank_tile_coord.tile_y + 1
            )
        elif move == constants.DOWN:
            sliding_tile_coord = coords.TileCoords(
                blank_tile_coord.tile_x,
                blank_tile_coord.tile_y - 1
            )
        elif move == constants.LEFT:
            sliding_tile_coord = coords.TileCoords(
                blank_tile_coord.tile_x + 1,
                blank_tile_coord.tile_y
            )
        elif move == constants.RIGHT:
            sliding_tile_coord = coords.TileCoords(
                blank_tile_coord.tile_x - 1,
                blank_tile_coord.tile_y
            )
        else:
            raise Exception('Invalid move input.')
        self._swap_tiles(blank_tile_coord, sliding_tile_coord)

    def _swap_tiles(self, coord1, coord2):
        coord1_number = self.get_tile_number(coord1)
        coord2_number = self.get_tile_number(coord2)
        self._set_tile(coord1, coord2_number)
        self._set_tile(coord2, coord1_number)

    def _set_tile(self, coord, number):
        self._board[coord.tile_y][coord.tile_x] = number
