import copy
import itertools
import random

from grid import Grid
from timeout import timeout
from timeout import TimeoutException

class Sudoku(Grid):

    def __init__(self):
        
        super().__init__(9, 9)

        self.add_row_partition()
        self.add_column_partition()
        self.add_block_partition(3, 3)

        self.partitions['row'].valid_rule = Sudoku.valid_rule
        self.partitions['column'].valid_rule = Sudoku.valid_rule
        self.partitions['block'].valid_rule = Sudoku.valid_rule

        self.partitions['row'].finished_rule = Sudoku.finished_rule
        self.partitions['column'].finished_rule = Sudoku.finished_rule
        self.partitions['block'].finished_rule = Sudoku.finished_rule

        self.allowed_values = Sudoku.allowed_values()

    def set_initial_values(self, values):

        super().set_initial_values(values)
        self.set_valid_values()

    def set_valid_values(self):

        self.set_valid_values_cell()
        
        num_discarded = 1
        while(num_discarded > 0):
            num_discarded = self.set_valid_values_block()

    def set_valid_values_cell(self):
        '''

        '''

        # Iterate over the empty grid cells.
        for cell in [c for c in self if c.value is None]:

            # Start of with all allowed values.
            valid_values = self.allowed_values

            # Iterate over grid partitions.
            for name, partition in self.partitions.items():

                # Get the partition subset where this cell is in.
                subset = partition.subsets[cell.partition_subsets[name]]

                # Get the values of its (non-empty) cells.
                values = [c.value for c in subset if not c.value is None]

                # Remove these values from the set of valid values.
                valid_values = valid_values - set(values)

            cell.valid_values = valid_values

    def set_valid_values_block(self):

        count = 0
        
        for block_index, block in enumerate(self.partitions['block']):

            for value in self.allowed_values:

                #print('Block %i, value %i:' % (block_index, value))

                row_indices = self.get_valid_value_containing_block_rows(block, value)
                #print('Row indices: %s' % (str(row_indices)))
                if(len(row_indices) == 1):

                    row_index = list(row_indices)[0]

                    for cell in [c for c in self if c.value is None]:

                        if(cell.partition_subsets['row'] == row_index and not 
                           cell.partition_subsets['block'] == block_index):
                            
                            set_size = len(cell.valid_values)
                            cell.valid_values.discard(value)
                            count += set_size - len(cell.valid_values)
                            #print('(%i, %i) %i row' % (cell.coord.i, cell.coord.j, value))

                column_indices = self.get_valid_value_containing_block_columns(block, value)
                #print('Column indices: %s' % (str(column_indices)))
                if(len(column_indices) == 1):

                    col_index = list(column_indices)[0]

                    for cell in [c for c in self if c.value is None]:

                        if(cell.partition_subsets['column'] == col_index and not 
                           cell.partition_subsets['block'] == block_index):
                            
                            set_size = len(cell.valid_values)
                            cell.valid_values.discard(value)
                            count += set_size - len(cell.valid_values)
                            #print('(%i, %i) %i column' % (cell.coord.i, cell.coord.j, value))
                            
        return count

    def get_valid_value_containing_block_rows(self, block, value):
        return self.get_valid_value_containing_subsets(block, 'row', value)

    def get_valid_value_containing_block_columns(self, block, value):
        return self.get_valid_value_containing_subsets(block, 'column', value)

    def get_valid_value_containing_subsets(self, block, subset, value):

        # Set of rows/cols in which this value is part of valid values.
        block_subsets = set()

        # Iterate over the empty cells in block.
        for cell in [c for c in block if c.value is None]:

            # Add row index to rows if value is valid for this cell.
            if(value in cell.valid_values):
                block_subsets.add(cell.partition_subsets[subset])

        # Return true if the value is valid in only one row.
        return block_subsets

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

                                moves.add((cell, value))

        #print('Number of block moves: %i' % (len(moves)))
        #for cell, value in moves:
        #    print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        return moves

    def get_position_moves(self):
        
        moves = set()

        for cell in [c for c in self if c.value is None]:
            if(len(cell.valid_values) == 1):
                moves.add((cell, list(cell.valid_values)[0]))

        #print('Number of position moves: %i' % (len(moves)))
        #for cell, value in moves:
        #    print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        return moves

    def to_json_string(self):

        rows = []
        for row in self.cells:
            s = [str(c.value) if not c.value is None else 'null' for c in row]
            print(s)
            rows.append('    [%s]' % (', '.join(s)))

        return '[\n%s\n]' % (',\n'.join(rows))

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
    def empty_sudoku(cls):

        sudoku = cls()
        sudoku.set_initial_values([[None for i in range(9)] for j in range(9)])
        sudoku.set_valid_values()

        return sudoku

    @classmethod
    def from_string(cls, s):

        init_values = []

        # Parse sudoku string.
        for line in [l for l in s.split('\n') if not l.strip() == '']:
            init_values.append(Sudoku.row_from_string(line))

        # Initialize sudoku and set initial values.
        sudoku = cls()
        sudoku.set_initial_values(init_values)
        sudoku.set_valid_values()

        return sudoku

    @staticmethod
    def row_from_string(s):

        row = []

        for num in s.split(' '):
            if(num.strip() == '.'):
                row.append(None)
            else:
                row.append(int(num))

        return row

    @classmethod
    def load(cls, file_name):

        sudokus = []

        with open(file_name, 'r') as fin:
            rows = []

            for line in [l.strip() for l in fin]:

                # Start reading new grid.
                if(line == ''):

                    # Create sudo if we have enough lines.
                    if(len(rows) == 9):

                        # Initialize sudoku and set initial values.
                        sudoku = cls()
                        sudoku.set_initial_values(rows)
                        sudokus.append(sudoku)

                    rows = []

                # Append this line to rows.
                else:
                    rows.append(Sudoku.row_from_string(line))

            if(len(rows) == 9):

                # Initialize sudoku and set initial values.
                sudoku = cls()
                sudoku.set_initial_values(rows)
                sudokus.append(sudoku)

        return sudokus

    @staticmethod
    def save(file_name, sudokus):

        with open(file_name, 'w') as fout:

            for sudoku in sudokus:
                fout.write('%s\n\n' % (str(sudoku)))


class SudokuSolver():

    def __init__(self, sudoku):

        self.sudoku = sudoku

    def solve(self, backtrack=True, multiple_solutions=False):

        iterations = []
        backtraced = False
        
        num_moves = 1

        while(num_moves > 0 and not self.sudoku.is_finished()):

            num_moves = self.apply_move_iteration()

            if(num_moves > 0):
                iterations.append(num_moves)

            #print(self.sudoku)

        #self.sudoku.print_sorted_valid_values()

        if not(self.sudoku.is_finished()):

            backtraced = True
            if(backtrack):
                #print('Running backtracking algorithm...')
                self.backtrack('sorted', multiple_solutions)

        return (iterations, backtraced)

    @timeout(1)
    def evaluate_difficulty(self, backtrack=True):

        iterations, backtraced = self.solve(backtrack=backtrack)

        print(iterations)
        print(backtraced)

        # level 3: extra fiendish, backtracking
        if(backtraced):
            level = 3

        # level 2: fiendish, 15+
        elif(len(iterations) > 8 and iterations[0] < 5):
            level = 2

        # level 1: difficult, 7-14 iteraties
        elif(len(iterations) > 6 and iterations[0] < 7):
            level = 1

        # level 0: mild, 5-6 iteraties
        elif(len(iterations) > 4 and iterations[0] < 9):
            level = 0
        else:
            level = -1

        return level

    def apply_move_iteration(self):

        block_moves = self.sudoku.get_block_moves()
        position_moves = self.sudoku.get_position_moves()

        moves = block_moves.union(position_moves)

        #print('Number of moves: %i' % (len(moves)))
        #for cell, value in moves:
        #    print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

        for cell, value in moves:
            cell.set_value(value)

        self.sudoku.set_valid_values()

        return len(moves)

    def backtrack(self, type, multiple_solutions=False):

        #self.fout = open(self.sudoku.file_out, 'w')
        #self.counter = 0

        self._solutions = []
        self.multiple_solutions = multiple_solutions

        if(type == 'random'):
            nodes = self.sudoku.get_shuffled_valid_values()

        elif(type == 'sorted'):
            nodes = self.sudoku.get_sorted_valid_values()

        else:
            nodes = self.sudoku.get_valid_values()
    
        self._backtrack(nodes, 0)
        
        #print(self.counter)
        #self.fout.close()
        return self._solutions
    
    def _backtrack(self, nodes, tree_depth):

        #print('Backtrack tree depth: %i' % (tree_depth))

        # No solution?
        if(tree_depth >= len(nodes)):
            print('Done backtracing.')
            return False

        cell, values = nodes[tree_depth]

        for value in values:

            #print('(%i, %i): %i' % (cell.coord.i, cell.coord.j, value))

            cell.set_value(value)

            # Solution found.
            if(self.sudoku.is_finished()):
                #print('Solution found!')
                #self.counter += 1
                #print(self.counter)
                #print(self.sudoku)
                #self.fout.write('\n# %010d\n' % (self.counter))
                #self.fout.write('%s' % (str(self.sudoku)))
                #self.fout.flush()

                self._solutions.append(copy.deepcopy(self.sudoku))

                if(self.multiple_solutions):
                    cell.set_value(None)
                    return False
                else:
                    return True

            # Valid grid, but not finshed yet, proceed with next tree level.
            if(self.sudoku.is_valid() and self._backtrack(nodes, tree_depth + 1)):
                if(self.multiple_solutions):
                    cell.set_value(None)
                return True

            # Invalid grid, skip this value
            else:
                pass

        # No more values left to explore, done with this branch, level up.
        cell.set_value(None)
        return False

class SudokuGenerator():

    @staticmethod
    def generate():
        
        solution = SudokuGenerator.random_solution()
        shuffled_coords = solution.shuffled_coordinates()
        values = solution.get_values()

        num_solutions = 1
        index = 0

        while(num_solutions < 2):
            
            # Randomly remove value from solution.
            row, col = shuffled_coords[index]
            values[row][col] = None

            # Initialize sudoko with these values.
            s = Sudoku()
            s.set_initial_values(values)
            s.set_valid_values()

            solver = SudokuSolver(s)

            # Count number of solutions.
            solutions = solver.backtrack('sorted', multiple_solutions=True)

            num_solutions = len(solutions)

            # Initialize sudoko with these values.
            s = Sudoku()
            s.set_initial_values(values)
            s.set_valid_values()
            
            solver = SudokuSolver(s)

            if(len(solutions) == 1):

                # Evaluate solution
                level = solver.evaluate_difficulty()

                s = Sudoku()
                s.set_initial_values(values)
                s.set_valid_values()
                last = s

            index += 1

        # why did I do this??
        # sudoku = copy.deepcopy(solution)

        return (last, solution, level)

    def backtrack_generate(self):

        cells = SudokuGenerator.random_solution().cells
        nodes = [cells[i][j] for (i, j) in cells.shuffled_coordinates()]

        self._backtrack(nodes, 0)

    def _backtrack(self, nodes, tree_level):

        # TODO
        pass

    @staticmethod
    def generate_from_pattern(pattern, num_tries, outdir, backtrack=True):
        
        pattern_sudoku = Sudoku.from_string(pattern)

        for i in range(num_tries):

            solution = SudokuGenerator.random_solution()

            for cell in pattern_sudoku:
                if(cell.value is None):
                    solution.cells[cell.coord.i][cell.coord.j].clear_value()

            solution.set_valid_values()

            solver = SudokuSolver(copy.deepcopy(solution))

            try:
                #level = solver.evaluate_difficulty(backtrack=backtrack)
                iterations, backtrack = solver.solve(backtrack=False)

            except(TimeoutException):
                print('Timeout.')
                #level = 4

            #print('\n%i:' % (level))
            #print(solution)

            # TODO turn this into separate function.
            if not(backtrack):

                if(len(iterations) in set(range(3, 5)) and
                     iterations[0] in set(range(10, 16))):

                    with open('%s/mild_sudokus.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (solution))

                    with open('%s/mild_solve_tracks.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (str(iterations)))

                elif(len(iterations) in set(range(5, 7)) and 
                       iterations[0] in set(range(10, 16))):

                    with open('%s/difficult_sudokus.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (solution))

                    with open('%s/difficult_solve_tracks.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (str(iterations)))

                elif((len(iterations) > 6 and iterations[0] >= 10) or 
                        (len(iterations) in set(range(3, 7)) and iterations[0] < 10)):

                    with open('%s/fiendish_sudokus.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (solution))

                    with open('%s/fiendish_solve_tracks.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (str(iterations)))

                elif(len(iterations) > 6 and iterations[0] < 10):

                    with open('%s/super_fiendish_sudokus.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (solution))

                    with open('%s/super_fiendish_solve_tracks.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (str(iterations)))
                
                else:
                    with open('%s/no_level_sudokus.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (solution))

                    with open('%s/no_level_solve_tracks.txt' % (outdir), 'a+') as fout:
                        fout.write('%s\n' % (str(iterations)))

    @staticmethod
    def random_solution():

        sudoku = Sudoku.empty_sudoku()
        #sudoku.file_in = '../data/random.txt'
        sudoku.file_out = '../data/random_solution.txt'

        solver = SudokuSolver(sudoku)
        solution = solver.backtrack('random')[0]

        #print(str(solution))
        
        return solution





RANDOM_SYMETRIC_BLOCKS = [

    [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']],
    [['.', '.', '.'], ['.', '0', '.'], ['.', '.', '.']],
    [['.', '.', '.'], ['0', '.', '0'], ['.', '.', '.']],
    [['.', '0', '.'], ['.', '.', '.'], ['.', '0', '.']],
    [['0', '.', '.'], ['.', '.', '.'], ['.', '.', '0']],
    [['.', '.', '0'], ['.', '.', '.'], ['0', '.', '.']],
    [['.', '0', '.'], ['.', '0', '.'], ['.', '0', '.']],
    [['.', '.', '0'], ['.', '0', '.'], ['0', '.', '.']],
    [['.', '.', '.'], ['0', '0', '0'], ['.', '.', '.']],
    [['0', '.', '.'], ['.', '0', '.'], ['.', '.', '0']],
    [['0', '.', '0'], ['.', '.', '.'], ['0', '.', '0']],
    [['.', '0', '.'], ['0', '.', '0'], ['.', '0', '.']],
    [['0', '0', '.'], ['.', '.', '.'], ['.', '0', '0']],
    [['.', '.', '0'], ['0', '.', '0'], ['0', '.', '.']],
    [['.', '0', '0'], ['.', '.', '.'], ['0', '0', '.']],
    [['0', '.', '.'], ['0', '.', '0'], ['.', '.', '0']],
    [['0', '.', '0'], ['.', '0', '.'], ['0', '.', '0']],
    [['.', '0', '.'], ['0', '0', '0'], ['.', '0', '.']],
    [['0', '0', '.'], ['.', '0', '.'], ['.', '0', '0']],
    [['.', '.', '0'], ['0', '0', '0'], ['0', '.', '.']],
    [['.', '0', '0'], ['.', '0', '.'], ['0', '0', '.']],
    [['0', '.', '.'], ['0', '0', '0'], ['.', '.', '0']]
]


class SudokuPatternGenerator():

    @staticmethod
    def random_block_pattern(num_filled):

        fill_indices = random.sample(range(9), num_filled)
        pattern = []

        for rowi in range(3):
            row = []
            for coli in range(3):

                if((rowi * 3 + coli) in fill_indices):
                    row.append('0')
                else:
                    row.append('.')

            pattern.append(row)

        return pattern
    
    @staticmethod
    def rotated_block(block):

        rotated = copy.deepcopy(block)

        rotated.reverse()
        for row in rotated:
            row.reverse()

        return rotated

    @staticmethod
    def vmirrored_block(block):

        mirrored = copy.deepcopy(block)

        for row in mirrored:
            row.reverse()

        return mirrored

    @staticmethod
    def hconcat(blocks):

        concat = []

        for row_i in range(len(blocks[0])):

            rows = [block[row_i] for block in blocks]
            row = list(itertools.chain.from_iterable(rows))

            concat.append(row)
        
        return concat

    @staticmethod
    def vconcat(blocks):

        concat = []

        for block in blocks:
            for row in block:
                concat.append(copy.copy(row))
        
        return concat

    @staticmethod
    def random_block_row_pattern(num_filled_side, num_filled_center):
        
        left = SudokuPatternGenerator.random_block_pattern(num_filled_side)
        right = SudokuPatternGenerator.vmirrored_block(left)
        center = SudokuPatternGenerator.random_block_pattern(num_filled_center)

        row = SudokuPatternGenerator.hconcat([left, center, right])

        return row

    @staticmethod
    def random_grid():

        min_occupied = 25
        max_occupied = 34
        num_occupied = 0

        while(num_occupied < min_occupied or num_occupied > max_occupied):

            corner = random.randint(0, 5)
            hor_edge = random.randint(0, 5)
            ver_edge = random.randint(0, 5)
            center = random.randint(0, 5)

            num_occupied = 4 * corner + 2 * hor_edge + 2 * ver_edge + center

        print(num_occupied)

        top_left = SudokuPatternGenerator.random_block_pattern(corner)
        bottom_right = SudokuPatternGenerator.rotated_block(top_left)

        top_right = SudokuPatternGenerator.random_block_pattern(corner)
        bottom_left = SudokuPatternGenerator.rotated_block(top_right)

        top_center = SudokuPatternGenerator.random_block_pattern(ver_edge)
        bottom_center = SudokuPatternGenerator.rotated_block(top_center)

        left_center = SudokuPatternGenerator.random_block_pattern(hor_edge)
        right_center = SudokuPatternGenerator.rotated_block(left_center)

        center = RANDOM_SYMETRIC_BLOCKS[random.randint(0, len(RANDOM_SYMETRIC_BLOCKS) - 1)]

        top = SudokuPatternGenerator.hconcat([top_left, top_center, top_right])
        middle = SudokuPatternGenerator.hconcat([left_center, center, right_center])
        bottom = SudokuPatternGenerator.hconcat([bottom_left, bottom_center, bottom_right])

        grid = SudokuPatternGenerator.vconcat([top, middle, bottom])

        return grid

    @staticmethod
    def to_string(field):

        s = ''
        for row in field:
            s += '%s\n' % (' '.join(row))

        return s

