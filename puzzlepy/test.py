import sys

from sudoku import Sudoku, SudokuSolver, SudokuGenerator, SudokuPatternGenerator

def main(task, puzzle):

    # Solve and evaluate.
    if(task == 'solve'):

        file = '../data/sudoku_%04d.txt' % (puzzle)
        sudoku = Sudoku.load(file)
        solver = SudokuSolver(sudoku)
        level = solver.evaluate_difficulty()

        print('level: %i' % (level))

    # Generate.
    if(task == 'generate'):
        outdir = '/mnt/MP1/Develop/'

        for i in range(500):

            grid = SudokuPatternGenerator.random_grid()
            pattern = SudokuPatternGenerator.to_string(grid)
            print(pattern)

            SudokuGenerator.generate_from_pattern(pattern, 100, outdir, backtrack=False)

if __name__ == "__main__":

    task = sys.argv[1]

    puzzle = 0
    if(task == 'solve'):
        puzzle = int(sys.argv[2])

    main(task, puzzle)
