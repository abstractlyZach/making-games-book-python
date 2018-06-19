import pygame

from . import settings
from . import events
from . import coords
from . import boardview
from . import photo_boardview

from slide_puzzle import events


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, event_manager, model):
        event_manager.register_listener(self)
        self._event_manager = event_manager
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
        self._create_buttons()
        self._create_message_box()

    def _create_buttons(self):
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
            '(R)eset',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            reset_button_coords)
        self._new_surf, self._new_rect = self.makeText(
            '(N)ew Game',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            new_game_button_coords)
        self._solve_surf, self._solve_rect = self.makeText(
            '(S)olve',
            settings.TEXT_COLOR,
            settings.TILE_COLOR,
            solve_button_coords)
        self._event_manager.post(events.SetResetRect(self._reset_rect))
        self._event_manager.post(events.SetSolveRect(self._solve_rect))
        self._event_manager.post(events.SetNewGameRect(self._new_rect))

    def _create_message_box(self):
        self._message_box, self._message_rect = self.makeText(
            'Solved!',
            settings.MESSAGE_COLOR,
            settings.BG_COLOR,
            coords.PixelCoords(5, 5)
        )
    def render_all(self):
        if not self._is_initialized:
            return
        # clear display
        self._display_surface.fill(settings.BG_COLOR)
        self._display_surface.blit(self._reset_surf, self._reset_rect)
        self._display_surface.blit(self._solve_surf, self._solve_rect)
        self._display_surface.blit(self._new_surf, self._new_rect)
        if self._model.is_solved:
            self._display_surface.blit(self._message_box, self._message_rect)
        self._board_view.render()
        pygame.display.update()

    def makeText(self, text, color, bgcolor, top_left_coords):
        # create the Surface and Rect objects for some text.
        textSurf = self._BASIC_FONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.top = top_left_coords.pixel_y
        textRect.left = top_left_coords.pixel_x
        return (textSurf, textRect)
