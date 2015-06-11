from grid import Grid

all_values = set(range(1, 10))

class Sudoku(Grid):

    def __init__(self):
        
        super().__init__(9, 9)

        self.add_row_partition()
        self.add_column_partition()
        self.add_block_partition(3, 3)

        self.partitions['row'].set_valid_rule(Sudoku.valid_rule)
        self.partitions['column'].set_valid_rule(Sudoku.valid_rule)
        self.partitions['block'].set_valid_rule(Sudoku.valid_rule)

        self.partitions['row'].set_finished_rule(Sudoku.finished_rule)
        self.partitions['column'].set_finished_rule(Sudoku.finished_rule)
        self.partitions['block'].set_finished_rule(Sudoku.finished_rule)

        self.set_allowed_values(Sudoku.allowed_values())

    @staticmethod
    def valid_rule(values):
        return len(set(values)) == len(values)

    @staticmethod
    def finished_rule(values):
        return len(Sudoku.allowed_values().difference(set(values))) == 0

    @staticmethod
    def allowed_values():
        return set(range(1, 10))

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

        return sudoku
