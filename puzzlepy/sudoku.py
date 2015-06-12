from grid import Grid

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

        self.allowed_values = Sudoku.allowed_values()

    def set_valid_values(self):

        for cell in [c for c in self if c.value is None]:

            valid_values = self.allowed_values

            for name, partition in self.partitions.items():

                subset = partition.subsets[cell.partition_subsets[name]]
                values = [c.value for c in subset if not c.value is None]

                valid_values = valid_values - set(values)

            #print('%s: %s' % (cell.coord, valid_values))
            cell.valid_values = valid_values

    def get_block_moves(self):

        moves = set()

        for name, partition in self.partitions.items():
            for index, subset in enumerate(partition):

                # Get valid values in this partition subset.
                valid_values = []
                for cell in [c for c in subset if c.value is None]:
                    valid_values.extend(list(cell.valid_values))
                #print(valid_values)

                # Get values that still need to be added in partition subset.
                values = [c.value for c in subset if not c.value is None]
                values_to_add = self.allowed_values - set(values)

                #print('%s - %i: %s' % (name, index, str(values_to_add)))
                
                for value in values_to_add:
                    num_positions = valid_values.count(value)
                    #print('value %i, positions: %i' % (value, num_positions))

                    if(num_positions == 1):
                        for cell in [c for c in subset if c.value is None]:
                            if(value in cell.valid_values):

                                #print('set cel (%i, %i): %i' % (cell.coord.i, cell.coord.j, value))
                                moves.add((cell, value))

        print('Number of block moves: %i' % (len(moves)))
        for cell, value in moves:
            print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        return moves

    def get_position_moves(self):
        
        moves = set()

        for cell in [c for c in self if c.value is None]:
            if(len(cell.valid_values) == 1):
                moves.add((cell, list(cell.valid_values)[0]))

        print('Number of position moves: %i' % (len(moves)))
        for cell, value in moves:
            print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        return moves

    def apply_move_iteration(self):

        block_moves = self.get_block_moves()
        position_moves = self.get_position_moves()

        moves = block_moves.union(position_moves)

        print('Number of moves: %i' % (len(moves)))
        for cell, value in moves:
            print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        for cell, value in moves:
            cell.set_value(value)

        self.set_valid_values()

        return len(moves)

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
        sudoku.set_valid_values()

        return sudoku


class SudokuSolver():

    def __init__(self, sudoku):

        self.sudoku = sudoku

    def solve(self):

        pass


