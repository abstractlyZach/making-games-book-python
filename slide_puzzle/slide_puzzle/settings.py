from . import constants


FPS = 30

BOARD_WIDTH = 4  # number of columns in the board
BOARD_HEIGHT = 4 # number of rows in the board
TILE_SIZE = 80
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BASIC_FONT_SIZE = 20

BUTTON_COLOR = constants.WHITE
BUTTON_TEXT_COLOR = constants.BLACK
MESSAGE_COLOR = constants.WHITE
BG_COLOR = constants.DARK_TURQUOISE
TILE_COLOR = constants.GREEN
TEXT_COLOR = constants.WHITE
BORDER_COLOR = constants.BRIGHT_BLUE


X_MARGIN = int((WINDOW_WIDTH -
               (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1)))
              / 2)
Y_MARGIN = int((WINDOW_HEIGHT -
               (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1)))
              / 2)

