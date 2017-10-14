import math

import pygame

import board
import misc

class BoardView(object):
    """Class for handling graphical aspects of a board"""
    def __init__(self, board, display_surface, box_size, gap_size, x_margin, y_margin, background_color):
        self._board = board
        self._box_size = box_size
        self._gap_size = gap_size
        self._display_surface = display_surface
        self._x_margin = x_margin
        self._y_margin = y_margin
        self._background_color = background_color
        self._quarter = math.floor(self._box_size / 4)
        self._half = math.floor(self._box_size / 2)

    def draw_board(self):
        self._draw_all_icons()

    def _draw_all_icons(self):
        """Draws all the icons on the board"""
        for x, y in self._board.boxes():
            self._draw_icon(x, y)

    def _draw_icon(self, x, y):
        """
        Draws an icon in the given box onto the display surface
        Args:
            x: box's x coordinate
            y: box's y coordinate
        """
        left, top, _ = self.left_top_box_coords(x, y)
        shape, color = self._board.get_shape_and_color(x, y)
        if shape == 'donut':
            self._draw_donut(color, left, top)


    def left_top_box_coords(self, x, y):
        """
        Get the pixel coordinates of the box at given coordinates
        Args:
            x: box's x coordinate
            y: box's y coordinate
        Returns:
            misc.Coordinate (pixel)
        """
        left = x * (self._box_size + self._gap_size) + self._x_margin
        top = y * (self._box_size + self._gap_size) + self._y_margin
        return misc.Coords(left, top, 'pixel')

    def _draw_donut(self, color, left_x, top_y):
        """Draw a colored donut at the pixel coordinates"""
        pygame.draw.circle(self._display_surface, color,
                           (left_x + self._half, top_y + self._half),
                           self._half - 5)
        pygame.draw.circle(self._display_surface, self._background_color,
                           (left_x + self._half, top_y + self._half),
                           self._quarter - 5)

    def _draw_square(self, color, left_x, top_y):
        """Draw a colored square at the pixel coordinates"""
        pass

