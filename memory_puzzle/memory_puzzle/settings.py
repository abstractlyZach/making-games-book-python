"""Memory puzzle settings"""
from . import constants

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10 # size of gap between boxes
BOARD_WIDTH = 10 # width in # of boxes
BOARD_HEIGHT = 7 # height in # of boxes
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)


# sanity checks
if BOARD_HEIGHT * BOARD_WIDTH % 2 != 0:
    error_message = 'Board needs to have an even number of boxes for pairs ' \
                    'of matches.'
    raise Exception(error_message)

if len(constants.ALL_COLORS) * len(constants.ALL_SHAPES) * 2 < \
       BOARD_WIDTH * BOARD_HEIGHT:
       error_message = 'Board is too big for the number of shapes/colors ' \
                        'defined.'
       raise Exception(error_message)


BG_COLOR = constants.NAVYBLUE
LIGHT_BG_COLOR = constants.GRAY
BOX_COLOR = constants.WHITE
HIGHLIGHT_COLOR = constants.BLUE
VISUAL_DEBUG_MODE = False