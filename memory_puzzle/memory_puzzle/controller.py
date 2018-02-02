import pygame

from . import coords
from . import events


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

    def _handle_event(self, event):
        if self._is_quit_event(event):
            event_to_post = events.QuitEvent()
        elif (event.type == pygame.KEYUP):
            event_to_post = events.KeyPressEvent(event.key)
        elif (event.type == pygame.MOUSEBUTTONUP):
            mouse_coords = coords.PixelCoords(event.pos[0], event.pos[1])
            event_to_post = events.ClickEvent(mouse_coords)
        else:
            return
        self._event_manager.post(event_to_post)

    def _is_quit_event(self, event):
        if event.type == pygame.QUIT:
            return True
        elif (event.type == pygame.KEYUP) and \
                (event.key == pygame.K_ESCAPE):
            return True
        else:
            return False


