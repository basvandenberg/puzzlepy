from grid import Grid

class Sudoku:

    def __init__(self):
        
        self.grid = Grid(9, 9)


    @classmethod
    def from_file(cls, file):

        # Read sudoku initial values from file
        init_values = []

        for line in file:
            row = []

            for num in line.split(' '):

                if(num.strip() == '.'):
                    row.append(None)

                else:
                    row.append(int(num))

            init_values.append(row)

        # Initialize sudoku and set initial values.
        sudoku = cls()
        sudoku.set_initial_values(init_values)

        sudoku.add_row_partition()
        sudoku.add_column_partition()
        sudoku.add_block_partition()

