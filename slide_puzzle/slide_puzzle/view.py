import pygame

from . import settings
from . import coords
from . import boardview

from slide_puzzle import events


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, event_manager, model):
        event_manager.register_listener(self)
        self._model = model
        self._is_initialized = False
        self._display_surface = None
        self._starting_new_word = False

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._is_initialized = False
            # ends the pygame graphical display
            pygame.quit()
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.TickEvent):
            self.render_all()


    def render_all(self):
        if not self._is_initialized:
            return
        # clear display
        self._display_surface.fill((0, 0, 0))
        self._display_surface.blit(self._reset_surf, self._reset_rect)
        self._display_surface.blit(self._solve_surf, self._solve_rect)
        self._display_surface.blit(self._new_surf, self._new_rect)
        self._board_view.render()
        pygame.display.update()

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.display.set_caption('Slide Puzzle')
        self._display_surface = pygame.display.set_mode((
            settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self._is_initialized = True
        self._BASIC_FONT = pygame.font.Font('freesansbold.ttf',
                                      settings.BASIC_FONT_SIZE)
        self._board_view = boardview.BoardView(
            self._display_surface,
            self._model,
            self._BASIC_FONT
        )
        reset_button_coords = coords.PixelCoords(
            settings.WINDOW_WIDTH - 120,
            settings.WINDOW_HEIGHT - 90)
        new_game_button_coords = coords.PixelCoords(
            settings.WINDOW_WIDTH - 120,
            settings.WINDOW_HEIGHT - 60)
        solve_button_coords = coords.PixelCoords(
            settings.WINDOW_WIDTH - 120,
            settings.WINDOW_HEIGHT - 30)
        self._reset_surf, self._reset_rect = self.makeText(
            'Reset',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            reset_button_coords)
        self._new_surf, self._new_rect = self.makeText(
            'New Game',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            new_game_button_coords)
        self._solve_surf, self._solve_rect = self.makeText(
            'Solve',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            solve_button_coords)

    def makeText(self, text, color, bgcolor, top_left_coords):
        # create the Surface and Rect objects for some text.
        textSurf = self._BASIC_FONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.top = top_left_coords.pixel_y
        textRect.left = top_left_coords.pixel_x
        return (textSurf, textRect)
