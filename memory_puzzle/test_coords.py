import coords


def test_box_coords():
    click = coords.BoxCoords(1, 2)
    assert click.box_x == 1
    assert click.box_y == 2

def test_pixel_coords_in_corner():
    click = coords.PixelCoords(0, 0)
    assert click.pixel_x == 0
    assert click.pixel_y == (0)
    assert click.box_x == None
    assert click.box_y == None

def test_pixel_coords_in_first_cell():
    click = coords.PixelCoords(76, 71)
    assert click.box_x == 0
    assert click.box_y == 0

def test_pixel_coords_in_between_first_and_second_cells():
    click = coords.PixelCoords(120, 115)
    assert click.box_x == None
    assert click.box_y == None
