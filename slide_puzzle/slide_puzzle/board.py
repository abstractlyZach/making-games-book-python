from . import constants
from . import tile
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
        self._sliding_tile_coord = None

    def _create_new_board(self):
        current_number = 1
        self._board = []
        for y in range(settings.BOARD_HEIGHT):
            row = []
            for x in range(settings.BOARD_WIDTH):
                current_tile = tile.Tile(current_number)
                row.append(current_tile)
                current_number += 1
            self._board.append(row)
        self._board[-1][-1] = tile.Tile(constants.BLANK)

    def get_tile(self, coord):
        return self._board[coord.tile_y][coord.tile_x]

    def get_blank_tile_coord(self):
        for coord in coords.get_all_tile_coords():
            if self.get_tile(coord).number == constants.BLANK:
                return coord

    def make_move(self, move):
        blank_tile_coord = self.get_blank_tile_coord()
        sliding_tile_coord = \
            coords.get_adjacent_tile_coord(blank_tile_coord, move)
        self._sliding_tile_coord = sliding_tile_coord
        target_tile = self.get_tile(self._sliding_tile_coord)
        target_tile.slide(move)

    def update(self):
        for coord in coords.get_all_tile_coords():
            tile = self.get_tile(coord)
            tile.update()
        if self._sliding_tile_coord is not None:
            sliding_tile = self.get_tile(self._sliding_tile_coord)
            if not sliding_tile.is_sliding: # slide motion is finished
                blank_tile_coord = self.get_blank_tile_coord()
                self._swap_tiles(blank_tile_coord, self._sliding_tile_coord)
                self._sliding_tile_coord = None

    def _swap_tiles(self, coord1, coord2):
        coord1_tile = self.get_tile(coord1)
        coord2_tile = self.get_tile(coord2)
        self._set_tile(coord1, coord2_tile)
        self._set_tile(coord2, coord1_tile)

    def _set_tile(self, coord, tile):
        self._board[coord.tile_y][coord.tile_x] = tile

    def is_valid_move(self, move):
        blank_tile_coord = self.get_blank_tile_coord()
        try:
            coords.get_adjacent_tile_coord(blank_tile_coord, move)
        except coords.OutOfBoundsException:
            return False
        return True

