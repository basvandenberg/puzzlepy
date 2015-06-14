import sys

from sudoku import Sudoku, SudokuSolver, SudokuGenerator

def main(num):

    file = '../data/sudoku_%04d.txt' % (num)

    sudoku = Sudoku.load(file)
    solver = SudokuSolver(sudoku)
    solver.evaluate_difficulty()

    #SudokuGenerator.random_finished()

if __name__ == "__main__":
    main(int(sys.argv[1]))
