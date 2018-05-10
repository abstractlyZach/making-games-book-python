import pytest

from slide_puzzle import board
from slide_puzzle import constants
from slide_puzzle import coords
from slide_puzzle import settings

def match_board(expected_numbers, board):
    current_index = 0
    for y in range(settings.BOARD_HEIGHT):
        for x in range(settings.BOARD_WIDTH):
            expected_number = expected_numbers[current_index]
            coord = coords.TileCoords(x, y)
            assert expected_number == board.get_tile_number(coord)
            current_index += 1

def test_no_exceptions_on_init():
    board.Board()

@pytest.fixture
def basic_board():
    return board.Board()

def test_blank_tile_is_in_place(basic_board):
    assert basic_board.get_blank_tile_coord() == coords.TileCoords(3, 3)

#todo: patch in the settings
def test_all_number_tiles_are_in_place(basic_board):
    expected_numbers = list(range(1, 16))
    expected_numbers.append(constants.BLANK)
    match_board(expected_numbers, basic_board)

def test_move_left_from_start_throws_exception(basic_board):
    with pytest.raises(Exception):
        basic_board.make_move(constants.LEFT)

def test_move_up_from_start_throws_exception(basic_board):
    with pytest.raises(Exception):
        basic_board.make_move(constants.UP)

def test_move_right_from_start_works(basic_board):
    basic_board.make_move(constants.RIGHT)
    expected_numbers = list(range(1,15))
    expected_numbers.append(constants.BLANK)
    expected_numbers.append(15)
    match_board(expected_numbers, basic_board)

def test_move_down_from_start_works(basic_board):
    basic_board.make_move(constants.DOWN)
    expected_numbers = list(range(1,12))
    expected_numbers.append(constants.BLANK)
    expected_numbers += list(range(13, 16))
    expected_numbers.append(12)
    match_board(expected_numbers, basic_board)

