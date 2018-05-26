import pygame

from . import events

class SoundBoard(object):
    def __init__(self, main_event_manager):
        main_event_manager.register_listener(self)

    def notify(self, event):
        if isinstance(event, events.InitializeEvent):
            self.initialize()
        elif isinstance(event, events.SoundEvent):
            self.play(event.id)

    def initialize(self):
        pygame.init()
        self._sounds = [
            pygame.mixer.Sound(f'simon/sounds/beep{number}.ogg')
            for number in range(1, 5)
        ]

    def play(self, number):
        self._sounds[number].play()
