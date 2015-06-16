import sys

from sudoku import Sudoku, SudokuSolver, SudokuGenerator, SudokuPatternGenerator

def main(num):

    solve = False

    # Solve and evaluate.
    if(solve):
        file = '../data/sudoku_%04d.txt' % (num)
        sudoku = Sudoku.load(file)
        solver = SudokuSolver(sudoku)
        level = solver.evaluate_difficulty()

        print('level: %i' % (level))

    # Generate.

    #sudoku, solution, level = SudokuGenerator.generate()

    #print('\n%i\n' % (level))
    #print(solution)
    #print(sudoku)

    # Generate from pattern.

    #block_pattern = SudokuPatternGenerator.random_block_pattern(3)
    #print(SudokuPatternGenerator.to_string(block_pattern))

    #rotated = SudokuPatternGenerator.rotated_block(block_pattern)
    #print(SudokuPatternGenerator.to_string(rotated))

    #row = SudokuPatternGenerator.random_block_row_pattern(4, 3)
    #print(SudokuPatternGenerator.to_string(row))

    outdir = '/home/bastiaan/Desktop'

    for i in range(500):

        grid = SudokuPatternGenerator.random_grid()
        pattern = SudokuPatternGenerator.to_string(grid)
        print(pattern)

        SudokuGenerator.generate_from_pattern(pattern, 25, outdir, backtrack=False)

if __name__ == "__main__":
    main(int(sys.argv[1]))
