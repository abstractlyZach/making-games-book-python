import pygame

from . import constants
from . import settings


class StartScreen(object):
    def __init__(self, screen):
        self._screen = screen
        # degrees of rotation for titles
        self._title_1_degrees = 0
        self._title_2_degrees = 0
        self._title_font = pygame.font.Font('freesansbold.ttf', 100)
        self._title_surface_1 = self._title_font.render(
            'Wormy!', True, constants.WHITE, constants.DARK_GREEN
        )
        self._title_surface_2 = self._title_font.render(
            'Wormy!', True, constants.GREEN
        )

    def draw(self):
        """Draw the titles to the screen and rotate them a little more each
        time.
        """
        self._screen.fill(settings.BG_COLOR)
        self._draw_rotated_title(self._title_surface_1, self._title_1_degrees)
        self._draw_rotated_title(self._title_surface_2, self._title_2_degrees)
        # rotate titles every time it's asked to draw
        self._title_1_degrees += 3
        self._title_2_degrees += 7

    def _draw_rotated_title(self, original_surface, degrees):
        """Rotate a title and blit it to the screen.
        """
        rotated_surface = pygame.transform.rotate(original_surface,
                                                    degrees)
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = (settings.WINDOW_WIDTH / 2,
                               settings.WINDOW_HEIGHT / 2)
        self._screen.blit(rotated_surface, rotated_rect)



