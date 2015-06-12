from sudoku import Sudoku

def main():

    with open('../data/sudoku_0001.txt', 'r') as fin:

        s = Sudoku.from_file(fin)

        print(s)

        num_moves = 1
        
        while(num_moves > 0 and not s.is_finished()):

            num_moves = s.apply_move_iteration()
            print(s)


if __name__ == "__main__":
    main()
