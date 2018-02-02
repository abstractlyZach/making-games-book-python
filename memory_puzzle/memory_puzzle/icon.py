import math

import pygame

from . import constants
from . import settings


class Icon(object):
    """Base class for icons."""
    quarter = math.floor(settings.BOX_SIZE / 4)
    half = math.floor(settings.BOX_SIZE / 2)

    def __init__(self, color, coords):
        self._color = color
        self._coords = coords
        self._calculate_box_left()
        self._calculate_box_top()

    def _calculate_box_top(self):
        container_size = settings.BOX_SIZE + settings.GAP_SIZE
        container_distance_from_margin = self._coords.box_y * container_size
        top_of_container = settings.Y_MARGIN + container_distance_from_margin
        self._box_top = top_of_container + math.floor(settings.GAP_SIZE / 2)

    def _calculate_box_left(self):
        container_size = settings.BOX_SIZE + settings.GAP_SIZE
        container_distance_from_margin = self._coords.box_x * container_size
        left_of_container = settings.X_MARGIN + container_distance_from_margin
        self._box_left = left_of_container + math.floor(settings.GAP_SIZE / 2)

    def draw(self, display_surface):
        raise NotImplementedError("You're using the base icon class!")


class Square(Icon):
    def draw(self, display_surface):
        rectangle_tuple = (self._box_left + self.quarter,
                           self._box_top + self.quarter,
                           self.half,
                           self.half)
        pygame.draw.rect(display_surface, self._color, rectangle_tuple)


class Donut(Icon):
    def draw(self, display_surface):
        center = (self._box_left + self.half,
                  self._box_top + self.half)
        pygame.draw.circle(display_surface, self._color,
                           center, self.half - 5)
        pygame.draw.circle(display_surface, settings.BG_COLOR,
                           center, self.quarter - 5)


class Diamond(Icon):
    def draw(self, display_surface):
        top_middle = (self._box_left + self.half, self._box_top)
        right_middle = (self._box_left + settings.BOX_SIZE,
                        self._box_top + self.half)
        bottom_middle = (self._box_left + self.half,
                         self._box_top + settings.BOX_SIZE)
        left_middle = (self._box_left, self._box_top + self.half)
        point_list = [top_middle, right_middle, bottom_middle, left_middle]
        pygame.draw.polygon(display_surface, self._color, point_list)


class Lines(Icon):
    def draw(self, display_surface):
        self._draw_diagonals_bottom_left_to_top_right(display_surface)
        self._draw_diagonals_top_left_to_bottom_right(display_surface)

    def _draw_diagonals_bottom_left_to_top_right(self, display_surface):
        for i in range(0, settings.BOX_SIZE, 4):
            bottom_left = (self._box_left, self._box_top + i)
            top_right = (self._box_left + i, self._box_top)
            pygame.draw.line(display_surface, self._color,
                             bottom_left, top_right)

    def _draw_diagonals_top_left_to_bottom_right(self, display_surface):
        for i in range(0, settings.BOX_SIZE, 4):
            box_bottom = self._box_top + settings.BOX_SIZE
            top_left = (self._box_left + i, box_bottom)
            box_right = self._box_left + settings.BOX_SIZE
            bottom_right = (box_right, self._box_top + i)
            pygame.draw.line(display_surface, self._color,
                             top_left, bottom_right)


class Oval(Icon):
    def draw(self, display_surface):
        bounding_rectangle = (self._box_left, self._box_top + self.quarter,
                              settings.BOX_SIZE, self.half)
        pygame.draw.ellipse(display_surface, self._color, bounding_rectangle)
