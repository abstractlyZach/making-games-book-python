from memory_puzzle import constants
from memory_puzzle import coords
from memory_puzzle import icon


def test_identical_icons_match():
    for shape in constants.ALL_SHAPES:
        for color in constants.ALL_COLORS:
            random_coords = coords.BoxCoords(1, 2)
            current_icon = icon.create_icon(shape, color, random_coords)
            assert current_icon == current_icon

def test_different_icons_dont_match():
    random_coords = coords.BoxCoords(5, 7)
    all_icons =  [icon.create_icon(shape, color, random_coords)
                  for shape in constants.ALL_SHAPES
                  for color in constants.ALL_COLORS]
    for current_index, current_icon in enumerate(all_icons):
        for other_index, other_icon in enumerate(all_icons):
            if current_index != other_index:
                assert current_icon != other_icon

