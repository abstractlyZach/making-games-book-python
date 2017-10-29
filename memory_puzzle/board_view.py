import math
import random

import pygame

import board
import misc

BOXES_TO_REVEAL_IN_HINT = 6

class AnimationStatus(object):
    def __init__(self, starting_coverage=0):
        self._coverage = starting_coverage
        self._animation_rate = 0
        self._being_animated = False
        self._will_reverse = False

    @property
    def coverage(self):
        return self._coverage

    @coverage.setter
    def coverage(self, new_coverage):
        self._coverage = new_coverage

    @property
    def animation_rate(self):
        return self._animation_rate

    @property
    def being_animated(self):
        return self._being_animated

    def start_animation(self, animation_rate, will_reverse=False):
        self._animation_rate = animation_rate
        self._being_animated = True
        self._will_reverse = will_reverse


    def end_animation(self):
        if self._will_reverse:
            self._animation_rate = -self._animation_rate
            self._will_reverse = False
        else:
            self._being_animated = False
            self._animation_rate = 0

    def tick_animation(self):
        self._coverage += self._animation_rate


class BoardView(object):
    """Class for handling graphical aspects of a board"""
    def __init__(self, board, display_surface, box_size, gap_size,
                 x_margin, y_margin, background_color, box_cover_color):
        self._board = board
        self._box_size = box_size
        self._gap_size = gap_size
        self._display_surface = display_surface
        self._x_margin = x_margin
        self._y_margin = y_margin
        self._background_color = background_color
        self._box_cover_color = box_cover_color
        self._quarter = math.floor(self._box_size / 4)
        self._half = math.floor(self._box_size / 2)
        self._animation_statuses = [[AnimationStatus(starting_coverage=box_size)
                                     for y in range(self._board.height)]
                                    for x in range(self._board.width)]

    def draw_board(self):
        self._display_surface.fill(self._background_color)
        self._progress_all_animations()
        for x, y in self._board.boxes():
            self._draw_box(x, y)

    def _draw_box(self, x, y):
        if self._is_being_animated(x, y):
            current_coverage = self._get_current_coverage(x, y)
            self._draw_icon(x, y)
            self._draw_box_cover(x, y, current_coverage)
        elif self._board.is_revealed(x, y):
            self._draw_icon(x, y)
        else:
            self._draw_box_cover(x, y, self._box_size)

    def _get_current_coverage(self, x, y):
        current_coverage = self._animation_statuses[x][y].coverage
        if current_coverage > 0:
            current_coverage = min(current_coverage, self._box_size)
        else:
            current_coverage = max(current_coverage, 0)
        return current_coverage

    def _progress_all_animations(self):
        for x, rows in enumerate(self._animation_statuses):
            for y, _ in enumerate(rows):
                animation_status = self._animation_statuses[x][y]
                self._progress_animation(animation_status)

    def _progress_animation(self, animation_status):
        if animation_status.being_animated:
            animation_status.tick_animation()
            coverage = animation_status.coverage
            if coverage <= 0 or coverage >= self._box_size:
                animation_status.end_animation()

    def are_animations_active(self):
        for box_x, box_y in self._board.boxes():
            if self._is_being_animated(box_x, box_y):
                return True
        return False

    def _is_being_animated(self, x, y):
        return self._animation_statuses[x][y].being_animated

    def animate_box_open_then_close(self, x, y):
        self._animation_statuses[x][y].start_animation(-5, will_reverse=True)

    def animate_box_close_then_open(self, x, y):
        self._animation_statuses[x][y].start_animation(5, will_reverse=True)

    def animate_box_open(self, x, y):
        self._animation_statuses[x][y].start_animation(-5)

    def animate_box_close(self, x, y):
        self._animation_statuses[x][y].start_animation(5)

    def get_hint_groups(self):
        unrevealed_box_coords = self._get_unrevealed_boxes()
        random.shuffle(unrevealed_box_coords)
        for i in range(0, len(unrevealed_box_coords), BOXES_TO_REVEAL_IN_HINT):
            boxes_to_peek = unrevealed_box_coords[i:i+BOXES_TO_REVEAL_IN_HINT]
            yield boxes_to_peek

    def _get_unrevealed_boxes(self):
        unrevealed_boxes = []
        for box_x, box_y in self._board.boxes():
            if not self._board.is_revealed(box_x, box_y):
                unrevealed_boxes.append((box_x, box_y))
        return unrevealed_boxes

    def peek_group_of_boxes(self, boxes):
        for box_x, box_y in boxes:
            self.animate_box_open_then_close(box_x, box_y)

    def get_box_at_pixel(self, pixel_coordinates):
        """
        Args:
            pixel_coordinates: the pixel's coordinates

        Returns:
            The board coordinates of the box at the pixel coordinates. Otherwise, None.
        """
        for x, y in self._board.boxes():
            left_top_pixel_coords = self.left_top_box_coords(x, y)
            box_rectangle = pygame.Rect(left_top_pixel_coords.x, left_top_pixel_coords.y,
                                        self._box_size, self._box_size)
            if box_rectangle.collidepoint(pixel_coordinates.x, pixel_coordinates.y):
                return x, y
        return None

    def _draw_box_cover(self, x, y, coverage):
        """
        Draw the box cover.
        Args:
            x: box's x coordinate
            y: box's y coordinate
            coverage: how many pixels of width should be covering the box
        """
        assert coverage <= self._box_size
        left_x, top_y, _  = self.left_top_box_coords(x, y)
        if coverage > 0:
            pygame.draw.rect(self._display_surface, self._box_cover_color,
                             (left_x, top_y, coverage, self._box_size))

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
        # todo: change these to variables instead of strings so that it throws errors on typos instead of allowing for
        #       weird bugs later
        if shape == 'donut':
            self._draw_donut(color, left, top)
        elif shape == 'square':
            self._draw_square(color, left, top)
        elif shape == 'diamond':
            self._draw_diamond(color, left, top)
        elif shape == 'lines':
            self._draw_lines(color, left, top)
        elif shape == 'oval':
            self._draw_oval(color, left, top)

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
        pygame.draw.rect(self._display_surface, color,
                         (left_x + self._quarter, top_y + self._quarter, self._half, self._half)
        )

    def _draw_diamond(self, color, left_x, top_y):
        """Draw a colored diamond at the pixel coordinates"""
        pygame.draw.polygon(self._display_surface, color,
                            [(left_x + self._half, top_y), (left_x + self._box_size, top_y + self._half),
                             (left_x + self._half, top_y + self._box_size), (left_x, top_y + self._half)]
        )

    def _draw_lines(self, color, left_x, top_y):
        """Draw colored lines at the pixel coordinates"""
        for i in range(0, self._box_size, 4):
            pygame.draw.line(self._display_surface, color, (left_x, top_y + i), (left_x + i, top_y))
            pygame.draw.line(self._display_surface, color,
                             (left_x + i, top_y + self._box_size),
                             (left_x + self._box_size, top_y + i)
            )

    def _draw_oval(self, color, left_x, top_y):
        """Draw a colored oval at the pixel coordinates"""
        pygame.draw.ellipse(self._display_surface, color,
                            (left_x, top_y + self._quarter, self._box_size, self._half)
        )

