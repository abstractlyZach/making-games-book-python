
class Button(object):
    def __init__(self, original_color, flash_color):
        self._original_color = original_color
        self._flash_color = flash_color
        self._brightening = False

    def update(self):
        if self._brightening: