from . import constants


FPS = 15
BG_COLOR = constants.BLACK
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = WINDOW_WIDTH / CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT / CELL_SIZE
