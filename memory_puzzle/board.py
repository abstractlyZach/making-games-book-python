import settings

class RevealedBoxes(object):
    def __init__(self, value):
        self._revealed_boxes = []
        for column in range(settings.BOARD_WIDTH):
            self._revealed_boxes.append([value] * settings.BOARD_HEIGHT)

    def reveal(self, coord):
        self._set_box(coord, True)

    def hide(self, coord):
        self._set_box(coord, False)

    def _set_box(self, coord, bool):
        self._revealed_boxes[coord.box_x][coord.box_y] = bool

    def is_revealed(self, coord):
        return self._revealed_boxes[coord.box_x][coord.box_y]

    def toggle(self, coord):
        old_value = self.is_revealed(coord)
        self._set_box(coord, not old_value)

