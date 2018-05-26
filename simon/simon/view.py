import pygame

from . import constants
from . import events
from . import settings


class GraphicalView(object):
    """Draws the model's state to the screen."""
    def __init__(self, main_event_manager, model):
        main_event_manager.register_listener(self)
        self._main_event_manager = main_event_manager
        self._model = model
        self._is_initialized = False
        self._screen = None
        self._small_font = None

    def notify(self, event):
        if isinstance(event, events.QuitEvent):
            self._handle_quit()
        elif isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.TickEvent):
            self.render_all()

    def _handle_quit(self):
        self._is_initialized = False
        # ends the pygame graphical display
        pygame.quit()

    def render_all(self):
        if not self._is_initialized:
            return
        # clear display
        self._screen.fill(settings.BG_COLOR)
        self._draw_buttons()
        pygame.display.update()

    def initialize(self):
        """Set up the pygame graphical display and load graphical resources."""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Simon')
        self._screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        self._small_font = pygame.font.Font(None, 40)
        self._is_initialized = True
        self._yellow_rect = pygame.Rect(
            settings.X_MARGIN,
            settings.Y_MARGIN,
            settings.BUTTON_SIZE,
            settings.BUTTON_SIZE
        )
        self._blue_rect = pygame.Rect(
            settings.X_MARGIN+settings.BUTTON_SIZE+settings.BUTTON_GAP_SIZE,
            settings.Y_MARGIN,
            settings.BUTTON_SIZE,
            settings.BUTTON_SIZE
        )
        self._red_rect = pygame.Rect(
            settings.X_MARGIN,
            settings.Y_MARGIN+settings.BUTTON_SIZE+settings.BUTTON_GAP_SIZE,
            settings.BUTTON_SIZE,
            settings.BUTTON_SIZE
        )
        self._green_rect = pygame.Rect(
            settings.X_MARGIN+settings.BUTTON_SIZE+settings.BUTTON_GAP_SIZE,
            settings.Y_MARGIN+settings.BUTTON_SIZE+settings.BUTTON_GAP_SIZE,
            settings.BUTTON_SIZE,
            settings.BUTTON_SIZE
        )
        self._main_event_manager.post(
            events.SetRectEvent(constants.BLUE, self._blue_rect)
        )
        self._main_event_manager.post(
            events.SetRectEvent(constants.YELLOW, self._yellow_rect)
        )
        self._main_event_manager.post(
            events.SetRectEvent(constants.GREEN, self._green_rect)
        )
        self._main_event_manager.post(
            events.SetRectEvent(constants.RED, self._red_rect)
        )

    def _draw_buttons(self):
        pygame.draw.rect(self._screen, constants.YELLOW, self._yellow_rect)
        pygame.draw.rect(self._screen, constants.BLUE, self._blue_rect)
        pygame.draw.rect(self._screen, constants.RED, self._red_rect)
        pygame.draw.rect(self._screen, constants.GREEN, self._green_rect)
        for button in self._model.get_flashing_buttons():
            if button.original_color == constants.GREEN:
                target_rect = self._green_rect
            elif button.original_color == constants.YELLOW:
                target_rect = self._yellow_rect
            elif button.original_color == constants.RED:
                target_rect = self._red_rect
            elif button.original_color == constants.BLUE:
                target_rect = self._blue_rect
            flash_surf = pygame.Surface(
                (settings.BUTTON_SIZE, settings.BUTTON_SIZE)
            )
            flash_surf = flash_surf.convert_alpha()
            flash_surf.fill((*button.flash_color, button.brightness_alpha))
            self._screen.blit(flash_surf, target_rect.topleft)

