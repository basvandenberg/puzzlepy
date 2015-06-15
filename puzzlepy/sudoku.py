import copy
import random

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

    @staticmethod
    def valid_rule(values):
        return len(set(values)) == len(values)

    @staticmethod
    def finished_rule(values):
        return len(Sudoku.allowed_values().difference(set(values))) == 0

    @staticmethod
    def allowed_values():
        return set(range(1, 10))

    @staticmethod
    def shuffled_coordinates():

        coords = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(coords)

        return coords

    @classmethod
    def load(cls, file):

        # Read sudoku initial values from file
        init_values = []

        # TODO read string and call from_string if possible.

        with open(file, 'r') as fin:

            for line in fin:
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

        # Store file name (used for saving).
        sudoku.file_in = file
        sudoku.file_out = file[:-4] + '_solution.txt'

        return sudoku

    @classmethod
    def from_string(cls, str):

        # Read sudoku initial values from file
        init_values = []

        for line in str.split('\n'):
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

    @classmethod
    def empty_sudoku(cls):

        sudoku = cls()
        sudoku.set_initial_values([[None for i in range(9)] for j in range(9)])
        sudoku.set_valid_values()

        return sudoku

    def save(self):

        with open(self.file_out, 'w') as fout:
            fout.write(str(self))


class SudokuSolver():

    def __init__(self, sudoku):

        self.sudoku = sudoku

    def solve(self, multiple_solutions=False):

        num_iterations = 0
        backtraced = False
        
        num_moves = 1

        while(num_moves > 0 and not self.sudoku.is_finished()):

            num_moves = self.apply_move_iteration()

            if(num_moves > 0):
                num_iterations += 1

            #print(self.sudoku)

        #self.sudoku.print_sorted_valid_values()

        if not(self.sudoku.is_finished()):

            #print('Running backtracking algorithm...')
            backtraced = True
            self.backtrack('sorted', multiple_solutions)

        return (num_iterations, backtraced)

    def evaluate_difficulty(self):

        tmp = {
            -1: 'To easy',
            0: 'Mild',
            1: 'Difficult',
            2: 'Fiendish',
            3: 'Super Fiendish'    
        }

        num_iter, backtraced = self.solve()

        #print(num_iter)
        #print(backtraced)

        if(backtraced):
            level = 3
        elif(num_iter > 12):
            level = 2
        elif(num_iter > 5):
            level = 1
        elif(num_iter > 4):
            level = 0
        else:
            level = -1

        #print(tmp[level])

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
        shuffled_coords = Sudoku.shuffled_coordinates()
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

        sudoku = copy.deepcopy(solution)

        return (last, solution, level)

    @staticmethod
    def generate_from_pattern(pattern):
        
        found = False
        num_tries = 0
        max_tries = 100

        pattern_sudoku = Sudoku.from_string(pattern)

        while(not found and num_tries < max_tries):

            solution = SudokuGenerator.random_solution()

            for cell in pattern_sudoku:
                if(cell.value == 0):
                    solution.cells[cell.coord.i][cell.coord.j].clear_value()

            solution.set_valid_values()

            solver = SudokuSolver(copy.deepcopy(solution))
            level = solver.evaluate_difficulty()

            print('\n%i:' % (level))
            print(solution)

            num_tries += 1

    @staticmethod
    def random_solution():

        sudoku = Sudoku.empty_sudoku()
        #sudoku.file_in = '../data/random.txt'
        sudoku.file_out = '../data/random_solution.txt'

        solver = SudokuSolver(sudoku)
        solution = solver.backtrack('random')[0]

        #print(str(solution))
        
        return solution
