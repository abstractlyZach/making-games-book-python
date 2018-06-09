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

    def notify(self, event):
        if isinstance(event, events.TickEvent):
            for input_event in pygame.event.get():
                self._handle_event(input_event)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self._input_event_manager.post(events.QuitEvent())
        elif (event.type == pygame.KEYUP) and \
                (event.key == pygame.K_ESCAPE):
            self._input_event_manager.post(events.QuitEvent())
        elif (event.type == pygame.KEYUP):
            self._handle_keypress(event.key)

    def _handle_keypress(self, key):
        if key == pygame.K_UP:
            self._input_event_manager.post(
                events.DirectionChangeEvent(constants.UP)
            )
        elif key == pygame.K_DOWN:
            self._input_event_manager.post(
                events.DirectionChangeEvent(constants.DOWN)
            )
        elif key == pygame.K_RIGHT:
            self._input_event_manager.post(
                events.DirectionChangeEvent(constants.RIGHT)
            )
        elif key == pygame.K_LEFT:
            self._input_event_manager.post(
                events.DirectionChangeEvent(constants.LEFT)
            )


