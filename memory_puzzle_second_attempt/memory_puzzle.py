from collections import namedtuple
import math
import random
import sys

import pygame
from pygame.locals import QUIT, KEYUP, K_ESCAPE, MOUSEBUTTONUP, MOUSEMOTION

import board
import constants
import coords
from settings import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT
from constants import ALL_SHAPES, BG_COLOR, ALL_COLORS
import settings
import shape

GameState = namedtuple('GameState', ['board', 'reveal_data', 'display_surface'])

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
    revealed_boxes = board.RevealedBoxes(True)
    game_state = GameState(main_board, revealed_boxes, DISPLAY_SURFACE)

    first_selection = None

    DISPLAY_SURFACE.fill(BG_COLOR)
    # start_game_animation(main_board)

    while True:
        DISPLAY_SURFACE.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_coords = coords.PixelCoords(event.pos[0], event.pos[1])
                if mouse_coords.in_a_box:
                    # main_board.toggle_reveal(box_coords.x, box_coords.y)
                    # main_board_view.animate_box_open_then_close(box_coords.x, box_coords.y)
                    # main_board_view.animate_box_open(box_coords.x, box_coords.y)
                    # main_board_view.select(box_coords.x, box_coords.y)
                    # print('({}, {})'.format(mouse_coords.box_x, mouse_coords.box_y))
                    game_state.reveal_data.toggle(mouse_coords)
                else:
                    print(None)
            # elif event.type == MOUSEMOTION:
            #     mouse_coords = misc.Coords(event.pos[0], event.pos[1], 'pixel')
            #     box_coords = main_board_view.get_box_at_pixel(mouse_coords)

        # main_board_view.draw_board()
        draw_board(game_state)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def get_randomized_board():
    available_icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            available_icons.append((shape, color))
    random.shuffle(available_icons)
    num_icons_to_use = math.floor(BOARD_WIDTH * BOARD_HEIGHT / 2)
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

def start_game_animation(game_state):
    covered_boxes = board.RevealedBoxes(False)
    box_coords_to_animate = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            box_coords_to_animate.append(coords.BoxCoords(x, y))

def draw_board(game_state):
    for coord in coords.get_all_box_coords():
        if not game_state.reveal_data.is_revealed(coord):
            top_left_corner_coord = coords.top_left_coords_of_box(coord)
            pygame.draw.rect(game_state.display_surface, constants.BOX_COLOR,
                             (top_left_corner_coord.pixel_x,
                              top_left_corner_coord.pixel_y,
                              settings.BOX_SIZE,
                              settings.BOX_SIZE)
                             )
        else:
            icon = game_state.board[coord.box_x][coord.box_y]
            if icon[0] == constants.SQUARE:
                shape_drawer = shape.Square(icon[1], coord,
                                            game_state.display_surface)
                shape_drawer.draw()




if __name__ == '__main__':
    main()
