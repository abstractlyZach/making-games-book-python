import pygame
import logging
from collections import namedtuple

from . import coords
from . import settings
from . import constants
from . import events

# class MovingTile(object):
#     def __init__(self, coord, x_velocity, y_velocity):
#         self._x_delta = 0
#         self._y_delta = 0
#         self._coord = coord
#         self._x_velocity = x_velocity
#         self._y_velocity = y_velocity
#
#     def move_single_frame(self):
#         self._x_delta += self._x_velocity
#         self._y_delta += self._y_velocity
#
#     @property
#     def coord(self):
#         return self._coord
#
#     @property
#     def x_delta(self):
#         return self._x_delta
#
#     @property
#     def y_delta(self):
#         return self._y_delta


class BoardView(object):
    def __init__(self, display_surface, model, font):
        self._display_surface = display_surface
        self._model = model
        self._font = font
        self._moving_tile = None

    def notify(self, event):
        # if isinstance(event, events.AnimationRequest):
        #     self._begin_animation(event.coord, event.direction)
        if isinstance(event, events.TickEvent):
            self.render()

    def render(self):
        self._draw_border()
        self._draw_all_tiles()

    def _draw_border(self):
        border_size = 5
        top = settings.Y_MARGIN
        left = settings.X_MARGIN
        inner_width = settings.BOARD_WIDTH * settings.TILE_SIZE
        width = inner_width + (2 * border_size)
        inner_height = settings.BOARD_HEIGHT * settings.TILE_SIZE
        height = inner_height + (2 * border_size)
        border_rectangle = (
            left - border_size,
            top - border_size,
            width,
            height
        )
        pygame.draw.rect(self._display_surface,
                         settings.BORDER_COLOR,
                         border_rectangle,
                         border_size)

    def _draw_all_tiles(self):
        # tiles_that_dont_move = coords.get_all_tile_coords()
        # if self._moving_tile is not None:
        #     tiles_that_dont_move.remove(self._moving_tile.coord)
        #     # self._progress_animation()
        #     self._draw_tile_at_coord(self._moving_tile.coord,
        #                              x_delta=self._moving_tile.x_delta,
        #                              y_delta=self._moving_tile.y_delta)
        #     # self._check_animation_complete()
        # for coord in tiles_that_dont_move:
        #     self._draw_tile_at_coord(coord)
        for coord in coords.get_all_tile_coords():
            self._draw_tile_at_coord(coord)

    # def _begin_animation(self, coord, direction):
    #     x_velocity = 0
    #     y_velocity = 0
    #     if direction == constants.UP:
    #         y_velocity = -settings.ANIMATION_SPEED
    #     elif direction == constants.DOWN:
    #         y_velocity = settings.ANIMATION_SPEED
    #     elif direction == constants.LEFT:
    #         x_velocity = -settings.ANIMATION_SPEED
    #     elif direction == constants.RIGHT:
    #         x_velocity = settings.ANIMATION_SPEED
    #     self._animation_in_progress = direction
    #     self._moving_tile = MovingTile(coord, x_velocity, y_velocity)
    #
    # def _check_animation_complete(self):
    #     x_movement_complete = \
    #         abs(self._moving_tile.x_delta) >= settings.TILE_SIZE
    #     y_movement_complete = \
    #         abs(self._moving_tile.y_delta) >= settings.TILE_SIZE
    #     if x_movement_complete or y_movement_complete:
    #         self._animation_event_manager.post(
    #             events.AnimationComplete(self._animation_in_progress)
    #         )
    #         self._moving_tile = None
    #
    # def _progress_animation(self):
    #     if self._moving_tile is not None:
    #         self._moving_tile.move_single_frame()

    def _draw_tile_at_coord(self, coord):
        tile = self._model.get_tile(coord)
        tile_text = str(tile.number)
        x_delta = tile.x_delta
        y_delta = tile.y_delta
        if tile_text != str(constants.BLANK):
            top_left_corner= coords.top_left_coord_of_tile(coord)
            top_left_corner_with_delta = coords.PixelCoords(
                top_left_corner.pixel_x + x_delta,
                top_left_corner.pixel_y + y_delta
            )
            tile_rectangle = (top_left_corner_with_delta.pixel_x,
                              top_left_corner_with_delta.pixel_y,
                              settings.TILE_SIZE,
                              settings.TILE_SIZE)
            pygame.draw.rect(self._display_surface,
                             settings.TILE_COLOR,
                             tile_rectangle)
            pygame.draw.rect(self._display_surface,
                             settings.BG_COLOR,
                             tile_rectangle,
                             2)
            text_surface = self._font.render(tile_text,
                                             True,
                                             settings.TEXT_COLOR)
            text_rectangle = text_surface.get_rect()
            text_rectangle.center = (
                top_left_corner_with_delta.pixel_x + settings.TILE_SIZE / 2,
                top_left_corner_with_delta.pixel_y + settings.TILE_SIZE / 2,
            )
            self._display_surface.blit(text_surface, text_rectangle)

