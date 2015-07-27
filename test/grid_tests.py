from nose.tools import *
from puzzlepy import grid

class TestGrid:

    def setup(self):
        self.small_grid = grid.Grid(3, 3)
        self.grid = grid.Grid(9, 9)

    def teardown(self):
        self.small_grid = None
        self.grid = None

    def test_top_triangle_coordinates(self):

        coords = self.small_grid.top_triangle_coordinates()

        assert len(coords) == 5
        assert coords[0] == (0, 0)
        assert coords[1] == (0, 1)
        assert coords[2] == (0, 2)
        assert coords[3] == (1, 1)
        assert coords[4] == (1, 2)

        coords = self.grid.top_triangle_coordinates()

        assert len(coords) == 41

    def test_rotated_coord(self):

        assert self.grid.rotated_coord((0, 0)) == (8, 8)
        assert self.grid.rotated_coord((0, 1)) == (8, 7)
        assert self.grid.rotated_coord((1, 0)) == (7, 8)

        assert self.grid.rotated_coord((3, 3)) == (5, 5)
        assert self.grid.rotated_coord((4, 4)) == (4, 4)
        assert self.grid.rotated_coord((5, 5)) == (3, 3)
        
        assert self.grid.rotated_coord((8, 8)) == (0, 0)
        assert self.grid.rotated_coord((8, 7)) == (0, 1)
        assert self.grid.rotated_coord((7, 8)) == (1, 0)

