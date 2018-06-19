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
    assert not click.in_a_box

def test_pixel_coords_in_first_cell():
    click = coords.PixelCoords(76, 71)
    assert click.box_x == 0
    assert click.box_y == 0
    assert click.in_a_box
    click = coords.PixelCoords(114, 109)
    assert click.box_x == 0
    assert click.box_y == 0
    assert click.in_a_box

def test_pixel_coords_in_between_first_and_second_cells_horizontally():
    for i in range(115, 125):
        click = coords.PixelCoords(i, 120)
        assert click.box_x == None
        assert click.box_y == None
        assert not click.in_a_box

def test_pixel_coords_in_between_first_and_second_cells_vertically():
    for i in range(110, 120):
        click = coords.PixelCoords(120, i)
        assert click.box_x == None
        assert click.box_y == None
        assert not click.in_a_box
