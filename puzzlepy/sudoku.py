from grid import Grid

all_values = set(range(1, 10))

def valid_rule(values):

    print(values)
    return len(set(values)) == len(values)

def finished_rule(values):

    print(values)
    return len(all_values.difference(set(values))) == 0

class Sudoku:

    def __init__(self):
        
        self.grid = Grid(9, 9)

        self.grid.add_row_partition()
        self.grid.add_column_partition()
        self.grid.add_block_partition(3, 3)

        self.grid.partitions['row'].set_valid_rule(valid_rule)
        self.grid.partitions['column'].set_valid_rule(valid_rule)
        self.grid.partitions['block'].set_valid_rule(valid_rule)

        self.grid.partitions['row'].set_finished_rule(finished_rule)
        self.grid.partitions['column'].set_finished_rule(finished_rule)
        self.grid.partitions['block'].set_finished_rule(finished_rule)

    def is_valid(self):
        return self.grid.is_valid()

    def is_finished(self):
        return self.grid.is_finished()

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
        sudoku.grid.set_initial_values(init_values)

        return sudoku

    def __str__(self):
        return str(self.grid)
