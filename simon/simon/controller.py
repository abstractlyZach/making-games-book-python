import pygame

from . import constants
from . import events


class Controller(object):
    """Handles input by posting events to the event manager when input
    happens."""
    def __init__(self, main_event_manager, input_event_manager, model):
        main_event_manager.register_listener(self)
        self._input_event_manager = input_event_manager
        self._model = model
        self._boxes = dict()

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            for input_event in pygame.event.get():
                self._handle_input_event(input_event)
        elif isinstance(event, events.SetRectEvent):
            self._handle_set_rect_event(event)

    def _handle_input_event(self, event):
        if event.type == pygame.QUIT:
            self._input_event_manager.post(events.QuitEvent())
        elif event.type == pygame.KEYUP:
            self._handle_keypress_event(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            self._handle_click_event(x, y)

    def _handle_keypress_event(self, key):
        if key == pygame.K_ESCAPE:
            self._input_event_manager.post(events.QuitEvent())
        elif key == pygame.K_q:
            self._input_event_manager.post(
                events.ButtonPressEvent(constants.YELLOW)
            )
        elif key == pygame.K_w:
            self._input_event_manager.post(
                events.ButtonPressEvent(constants.BLUE)
            )
        elif key == pygame.K_a:
            self._input_event_manager.post(
                events.ButtonPressEvent(constants.RED)
            )
        elif key == pygame.K_s:
            self._input_event_manager.post(
                events.ButtonPressEvent(constants.GREEN)
            )

    def _handle_set_rect_event(self, event):
        self._boxes[event.color] = event.rect

    def _handle_click_event(self, x, y):
        for color in constants.BASIC_COLORS:
            if self._click_in_box(x, y, color):
                self._input_event_manager.post(events.ButtonPressEvent(color))

    def _click_in_box(self, click_x, click_y, color):
        target_rect = self._boxes[color]
        return target_rect.collidepoint((click_x, click_y))



