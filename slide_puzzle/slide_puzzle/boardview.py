import pygame

from . import coords
from . import settings
from . import constants
from . import events


class BoardView(object):
    def __init__(self, display_surface, model, font):
        self._display_surface = display_surface
        self._model = model
        self._font = font
        self._moving_tile = None

    def notify(self, event):
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
        for coord in coords.get_all_tile_coords():
            self._draw_tile_at_coord(coord)

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

