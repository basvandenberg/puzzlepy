import sys

from sudoku import Sudoku

def main(num):

    with open('../data/sudoku_%04d.txt' % (num), 'r') as fin:

        s = Sudoku.from_file(fin)

        print(s)

        num_moves = 1
        
        while(num_moves > 0 and not s.is_finished()):

            num_moves = s.apply_move_iteration()
            print(s)

        s.print_sorted_valid_values()

        if not(s.is_finished()):

            print('Running backtracking algorithm...')
            s.backtrack('../data/sudoku_%04d_solution.txt' % (num))

if __name__ == "__main__":
    main(int(sys.argv[1]))
