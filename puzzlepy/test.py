import sys

from sudoku import Sudoku, SudokuSolver, SudokuGenerator, SudokuPatternGenerator

def main(num):

    # Solve and evaluate.

    #file = '../data/sudoku_%04d.txt' % (num)
    #sudoku = Sudoku.load(file)
    #solver = SudokuSolver(sudoku)
    #solver.evaluate_difficulty()

    # Generate.

    #sudoku, solution, level = SudokuGenerator.generate()

    #print('\n%i\n' % (level))
    #print(solution)
    #print(sudoku)

    # Generate from pattern.

    pattern =\
'''
. 0 . 0 . 0 . 0 .
0 . . . 0 . . . 0
0 . . . 0 . . . 0
. . 0 . . 0 0 . .
. 0 . . 0 . . 0 .
. 0 . 0 . . . 0 .
0 . 0 . 0 . 0 . 0
0 . . . 0 . . . 0
. 0 . 0 . 0 . 0 .
'''
    pattern2 =\
'''
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
'''

    #block_pattern = SudokuPatternGenerator.random_block_pattern(3)
    #print(SudokuPatternGenerator.to_string(block_pattern))

    #rotated = SudokuPatternGenerator.rotated_block(block_pattern)
    #print(SudokuPatternGenerator.to_string(rotated))

    #row = SudokuPatternGenerator.random_block_row_pattern(4, 3)
    #print(SudokuPatternGenerator.to_string(row))

    grid = SudokuPatternGenerator.random_grid(5, 2, 3, 3)
    pattern = SudokuPatternGenerator.to_string(grid)
    print(pattern)

    SudokuGenerator.generate_from_pattern(pattern)

if __name__ == "__main__":
    main(int(sys.argv[1]))
