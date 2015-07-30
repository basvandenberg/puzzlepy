import copy
from nose.tools import *
from puzzlepy.sudoku import SudokuTransform

BASIC_SUDOKU_VALUES = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]

class TestSudokuTransform:

    def setup(self):
        self.sudoku = copy.deepcopy(SudokuTransform.BASIC_SUDOKU_VALUES)

    def teardown(self):
        self.sudoku = None

    def test_swap_cells(self):

        assert self.sudoku[0][0] == 1
        assert self.sudoku[0][1] == 2

        SudokuTransform.swap_cells(self.sudoku, 0, 0, 0, 1)

        assert self.sudoku[0][0] == 2
        assert self.sudoku[0][1] == 1

    def test_swap_rows(self):

        assert self.sudoku[0] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert self.sudoku[1] == [4, 5, 6, 7, 8, 9, 1, 2, 3]

        SudokuTransform.swap_rows(self.sudoku, 0, 1)

        assert self.sudoku[0] == [4, 5, 6, 7, 8, 9, 1, 2, 3]
        assert self.sudoku[1] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
