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
Y_MARGIN = int((WINDOW_HEIGHT- (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

assert(BOARD_HEIGHT * BOARD_WIDTH % 2 == 0,
       'Board needs to have an even number of boxes for pairs of matches.')

BG_COLOR = constants.NAVYBLUE
LIGHT_BG_COLOR = constants.GRAY
BOX_COLOR = constants.WHITE
HIGHLIGHT_COLOR = constants.BLUE