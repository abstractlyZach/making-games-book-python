import pygame

from . import events
from . import settings
from . import coords
from . import constants


DIRECTIONAL_KEYS = [pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT]
class Controller(object):
    """Handles input by posting events to the event manager when input
    happens."""
    def __init__(self, event_manager, model):
        self._event_manager = event_manager
        self._event_manager.register_listener(self)
        self._model = model

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            for input_event in pygame.event.get():
                self._handle_event(input_event)
        elif isinstance(event, events.SetResetRect):
            self._reset_rect = event.rectangle
        elif isinstance(event, events.SetSolveRect):
            self._solve_rect = event.rectangle
        elif isinstance(event, events.SetNewGameRect):
            self._new_game_rect = event.rectangle

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._event_manager.post(events.QuitEvent())
        elif (event.type == pygame.KEYUP) and \
                (event.key == pygame.K_ESCAPE):
            self._event_manager.post(events.QuitEvent())
        elif (event.type == pygame.KEYUP):
            self._handle_keypress(event)
        elif (event.type == pygame.MOUSEBUTTONUP):
            self._handle_click_event(event)

    def _handle_keypress(self, event):
        self._event_manager.post(events.KeyPressEvent(event.key))
        if event.key in DIRECTIONAL_KEYS:
            move_direction = self._get_move_direction(event.key)
            self._event_manager.post(events.MoveEvent(move_direction))
        elif event.key == pygame.K_r:
            self._event_manager.post(events.ResetEvent())
        elif event.key == pygame.K_s:
            self._event_manager.post(events.SolveEvent())
        elif event.key == pygame.K_n:
            self._event_manager.post(events.NewGameEvent())

    def _get_move_direction(self, event_key):
        if event_key == pygame.K_UP:
            return constants.UP
        elif event_key == pygame.K_DOWN:
            return constants.DOWN
        elif event_key == pygame.K_LEFT:
            return constants.LEFT
        elif event_key == pygame.K_RIGHT:
            return constants.RIGHT

    def _handle_click_event(self, event):
        self._check_button_clicked(event)
        x, y = event.pos
        click_coords = coords.PixelCoords(x, y)
        tile_clicked = self.get_tile_clicked(click_coords)
        if tile_clicked is not None:
            self._event_manager.post(events.ClickEvent(tile_clicked))

    def _check_button_clicked(self, event):
        if self._reset_rect.collidepoint(event.pos):
            self._event_manager.post(events.ResetEvent())
        elif self._solve_rect.collidepoint(event.pos):
            self._event_manager.post(events.SolveEvent())
        elif self._new_game_rect.collidepoint(event.pos):
            self._event_manager.post(events.NewGameEvent())

    def get_tile_clicked(self, coord):
        for tile_coord in coords.get_all_tile_coords():
            top_left_of_tile = coords.top_left_coord_of_tile(tile_coord)
            within_x_bounds = coord.pixel_x > top_left_of_tile.pixel_x and \
                coord.pixel_x < top_left_of_tile.pixel_x + settings.TILE_SIZE
            within_y_bounds = coord.pixel_y > top_left_of_tile.pixel_y and \
                coord.pixel_y < top_left_of_tile.pixel_y + settings.TILE_SIZE
            if within_x_bounds and within_y_bounds:
                return tile_coord
        return None