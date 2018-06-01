from PIL import Image
import pygame

from . import boardview
from . import constants
from . import coords
from . import settings


class PhotoBoardView(boardview.BoardView):
    def __init__(self, *args):
        super().__init__(*args)
        photo = Image.open('photos/dad_and_me.png')
        board_dimensions = (settings.BOARD_WIDTH * settings.TILE_SIZE,
                            settings.BOARD_HEIGHT * settings.TILE_SIZE)
        photo = photo.resize(board_dimensions)
        self._image_parts = []
        for row_index in range(settings.BOARD_HEIGHT):
            for column_index in range(settings.BOARD_WIDTH):
                left_pixel = settings.TILE_SIZE * column_index
                top_pixel = settings.TILE_SIZE * row_index
                crop_rectangle = (
                    left_pixel,
                    top_pixel,
                    left_pixel + settings.TILE_SIZE,
                    top_pixel + settings.TILE_SIZE
                )
                pil_cropped_image = photo.crop(crop_rectangle)
                data = pil_cropped_image.tobytes()
                mode = pil_cropped_image.mode
                size = pil_cropped_image.size
                pygame_cropped_image = pygame.image.fromstring(data,
                                                               size,
                                                               mode)
                self._image_parts.append(pygame_cropped_image)



    def _draw_tile_at_coord(self, coord):
        tile = self._model.get_tile(coord)
        x_delta = tile.x_delta
        y_delta = tile.y_delta
        if tile.number != constants.BLANK:
            top_left_corner= coords.top_left_coord_of_tile(coord)
            top_left_corner_with_delta = coords.PixelCoords(
                top_left_corner.pixel_x + x_delta,
                top_left_corner.pixel_y + y_delta
            )
            topleft = (top_left_corner_with_delta.pixel_x,
                       top_left_corner_with_delta.pixel_y)
            self._display_surface.blit(self._image_parts[tile.number - 1],
                                       topleft)
