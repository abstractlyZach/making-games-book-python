import math
import random

from . import coords
from . import icon


class Board(object):
    """Provides an interface for accessing reveal data and icon data,
    using coords."""
    def __init__(self, width, height, colors, shapes):
        self._width = width
        self._height = height
        self._colors = colors
        self._shapes = shapes
        self._new_board()

    def _new_board(self):
        """Replaces the old board with a new configuration"""
        icons = []
        for color in self._colors:
            for shape in self._shapes:
                icons.append((shape, color))
        random.shuffle(icons)
        # select icons for the board and duplicate them
        num_icons_possible = math.floor((self._width * self._height) / 2)
        icons = icons[:num_icons_possible]
        icons = icons * 2
        random.shuffle(icons)
        # set icons on the board
        self._board = []
        for x in range(self._width):
            column = []
            for y in range(self._height):
                shape, color = icons.pop()
                current_icon = icon.create_icon(shape, color,
                                                coords.BoxCoords(x, y))
                column.append(current_icon)
            self._board.append(column)
        # mark all cells as unrevealed
        self._revealed = [[False for y in range(self._height)]
                          for x in range(self._width)]

    def get_icon(self, coord):
        """
        Args:
            coord: box's coordinates
        Returns:
            The icon in this box.
        """
        return self._board[coord.box_x][coord.box_y]

    def is_revealed(self, coord):
        """
        Args:
            coord: box's coordinates
        Returns:
            True if the box is revealed, else False.
        """
        return self._revealed[coord.box_x][coord.box_y]

    def reveal(self, coord):
        """
        Reveal the box at the coordinates
        Args:
            coord: box's coordinates
        """
        self._revealed[coord.box_x][coord.box_y] = True

    def cover(self, coord):
        """
        Hide the box at the coordinates
        Args:
            coord: box's coordindates
        """
        self._revealed[coord.box_x][coord.box_y] = False

    def toggle_reveal(self, coord):
        """
        Toggle the reveal state of the box at the coordinates
        Args:
            coord: box's coordinates
        """
        self._revealed[coord.box_x][coord.box_y] = not self.is_revealed(coord)

    def are_all_revealed(self):
        for coord in coords.get_all_box_coords():
            if not self.is_revealed(coord):
                return False
        return True

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
