from sudoku import Sudoku

def main():

    with open('sudoku.txt', 'r') as fin:

        s = Sudoku.from_file(fin)

        print(s)
        print(s.grid.partitions['row'].is_valid())
        print(s.grid.partitions['row'].is_finished())

if __name__ == "__main__":
    main()
