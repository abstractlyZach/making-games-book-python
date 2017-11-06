import random
import sys

import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE, MOUSEBUTTONUP, MOUSEMOTION

import coords

# todo: move all these things to a config file
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
    mouse_coords = coords.PixelCoords(0, 0)

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_coords = misc.Coords(event.pos[0], event.pos[1], 'pixel')
                box_coords = main_board_view.get_box_at_pixel(mouse_coords)
                if box_coords:
                    box_coords = misc.Coords(box_coords[0], box_coords[1], 'board')
                    # main_board.toggle_reveal(box_coords.x, box_coords.y)
                    # main_board_view.animate_box_open_then_close(box_coords.x, box_coords.y)
                    # main_board_view.animate_box_open(box_coords.x, box_coords.y)
                    main_board_view.select(box_coords.x, box_coords.y)
                    print('({}, {})'.format(box_coords.x, box_coords.y))
                else:
                    print(None)
            elif event.type == MOUSEMOTION:
                mouse_coords = misc.Coords(event.pos[0], event.pos[1], 'pixel')
                box_coords = main_board_view.get_box_at_pixel(mouse_coords)

        main_board_view.draw_board()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def get_randomized_board():
    available_icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            available_icons.append((shape, color))
    random.shuffle(available_icons)
    num_icons_to_use = BOARD_WIDTH * BOARD_HEIGHT / 2
    icons_to_use = available_icons[:num_icons_to_use] * 2
    random.shuffle(icons_to_use)
    # create board
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            current_icon = icons_to_use.pop()
            column.append(current_icon)
        board.append(column)
    return board




if __name__ == '__main__':
    main()
