"""Constants to be used in the memory puzzle"""

import settings

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BG_COLOR = NAVYBLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)

assert(len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= settings.BOARD_WIDTH *
       settings.BOARD_HEIGHT,
       "Board is too big for the number of shapes/colors defined.")
