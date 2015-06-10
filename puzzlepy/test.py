from sudoku import Sudoku

def main():

    with open('sudoku.txt', 'r') as fin:

        s = Sudoku.from_file(fin)

if __name__ == "__main__":
    main()
