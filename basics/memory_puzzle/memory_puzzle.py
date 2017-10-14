import sys

import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE

import board
import misc

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10 # size of gap between boxes
BOARD_WIDTH = 10 # width in # of boxes
BOARD_HEIGHT = 7 # height in # of boxes
assert(BOARD_HEIGHT * BOARD_WIDTH % 2 == 0,
       'Board needs to have an even number of boxes for pairs of matches.')
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT- (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

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

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert(len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT,
       "Board is too big for the number of shapes/colors defined.")


def main():
    """Sets up the game and runs the main loop"""
    global DISPLAY_SURFACE
    global FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Memory Game')
    mouse_coords = misc.Coords(0, 0, 'pixels')

    main_board = board.Board()



    while True:
        DISPLAY_SURFACE.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main()
