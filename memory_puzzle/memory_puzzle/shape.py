import math

import pygame

import constants
import settings


class Shape(object):
    def __init__(self, color, coords, display_surface):
        self._color = color
        self._coords = coords
        self._display_surface = display_surface

class Square(Shape):
    def draw(self):
        quarter = math.floor(settings.BOX_SIZE / 4)
        half = math.floor(settings.BOX_SIZE / 2)
        container_size = settings.BOX_SIZE + settings.GAP_SIZE
        top_of_container = settings.Y_MARGIN + \
                           (self._coords.box_y * container_size)
        left_of_container = settings.X_MARGIN + \
                            (self._coords.box_x * container_size)
        square_top = top_of_container + quarter
        square_left = left_of_container + quarter
        rectangle_tuple = (square_top, square_left, half, half)
        pygame.draw.rect(self._display_surface, self._color, rectangle_tuple)
