import sys

from sudoku import Sudoku, SudokuSolver, SudokuGenerator

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

    SudokuGenerator.generate_from_pattern(pattern)   

if __name__ == "__main__":
    main(int(sys.argv[1]))
