import math
import random

class Board(object):
    def __init__(self, width, height, colors, shapes):
        self._width = width
        self._height = height
        self._colors = colors
        self._shapes = shapes
        self._new_board()

    def boxes(self):
        for x in range(self._width):
            for y in range(self._height):
                yield (x, y)

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
                column.append(icons.pop())
            self._board.append(column)
        # mark all cells as unrevealed
        self._revealed = [[False for y in range(self._height)]
                          for x in range(self._width)]

    def get_shape_and_color(self, x, y):
        """
        Args:
            x: box's x coordinate
            y: box's y coordinate
        Returns:
            The shape and color of the icon in this box.
        """
        return self._board[x][y]

    def is_revealed(self, x, y):
        """
        Args:
            x: box's x coordinate
            y: box's y coordinate
        Returns:
            True if the box is revealed, else False.
        """
        return self._revealed[x][y]

    def reveal(self, x, y):
        """
        Reveal the box at the coordinates
        Args:
            x: box's x coordinate
            y: box's y coordinate
        """
        self._revealed[x][y] = True

    def cover(self, x, y):
        """
        Hide the box at the coordinates
        Args:
            x: box's x coordinate
            y: box's y coordinate
        """
        self._revealed[x][y] = False

    def toggle_reveal(self, x, y):
        """
        Toggle the reveal state of the box at the coordinates
        Args:
            x: box's x coordinate
            y: box's y coordinate
        """
        self._revealed[x][y] = not self.is_revealed(x, y)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
