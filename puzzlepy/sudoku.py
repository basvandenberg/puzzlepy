# -*- coding: utf-8 -*-
'''

This module contains three main classes:

- Sudoku
- SudokuSolver
- SudokuGenerator

And a helper class used for 'shuffling' sudokus to generate new sudokus from
existing ones:

- SudokuTransform

The helper class works with sudoku values only (array of arrays) and not
with Sudoku objects, because that is faster and easier.
'''

import sys
import copy
import random
import json

from puzzlepy.grid import Grid
from puzzlepy.coord import Coord


class Sudoku(Grid):

    def __init__(self):
        '''
        '''
        
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

                row_indices =\
                    self.get_valid_value_containing_block_rows(block, value)

                if(len(row_indices) == 1):

                    row_index = list(row_indices)[0]

                    for cell in [c for c in self if c.value is None]:
                        if(cell.partition_subsets['row'] == row_index and not
                           cell.partition_subsets['block'] == block_index):
                            
                            set_size = len(cell.valid_values)
                            cell.valid_values.discard(value)
                            count += set_size - len(cell.valid_values)

                column_indices =\
                    self.get_valid_value_containing_block_columns(block, value)

                if(len(column_indices) == 1):

                    col_index = list(column_indices)[0]

                    for cell in [c for c in self if c.value is None]:

                        if(cell.partition_subsets['column'] == col_index and not 
                           cell.partition_subsets['block'] == block_index):
                            
                            set_size = len(cell.valid_values)
                            cell.valid_values.discard(value)
                            count += set_size - len(cell.valid_values)
                            
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

        moves = {}

        for name, partition in self.partitions.items():

            moves[name] = set()

            for index, subset in enumerate(partition):

                # Get valid values in this partition subset.
                valid_values = []
                for cell in [c for c in subset if c.value is None]:
                    valid_values.extend(list(cell.valid_values))

                # Get values that still need to be added in partition subset.
                values = [c.value for c in subset if not c.value is None]
                values_to_add = self.allowed_values - set(values)

                for value in values_to_add:

                    num_positions = valid_values.count(value)

                    if(num_positions == 1):
                        for cell in [c for c in subset if c.value is None]:
                            if(value in cell.valid_values):

                                moves[name].add((cell, value))

        return moves

    def get_position_moves(self):
        
        moves = set()

        for cell in [c for c in self if c.value is None]:
            if(len(cell.valid_values) == 1):

                moves.add((cell, list(cell.valid_values)[0]))

        return moves

    def to_json_string(self):

        rows = []
        for row in self.cells:
            s = [str(c.value) if not c.value is None else 'null' for c in row]
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
    def full_sudoku(cls):

        sudoku = cls()
        sudoku.set_initial_values(Sudoku.BASIC_SUDOKU_VALUES)
        sudoku.set_valid_values()

        return sudoku

    @classmethod
    def from_string(cls, s):

        init_values = []

        # Parse sudoku string.
        for line in [l for l in s.split('\n') if not l.strip() == '']:
            init_values.append(Sudoku._row_from_string(line))

        # Initialize sudoku and set initial values.
        sudoku = cls()
        sudoku.set_initial_values(init_values)
        sudoku.set_valid_values()

        return sudoku
    
    @staticmethod
    def _row_from_string(s):

        row = []

        for num in s.split(' '):
            if(num.strip() == '.'):
                row.append(None)
            else:
                row.append(int(num))

        return row

    @classmethod
    def load_txt(cls, fin):

        sudokus = []

        #with open(file_name, 'r') as fin:
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
                rows.append(Sudoku._row_from_string(line))

        if(len(rows) == 9):

            # Initialize sudoku and set initial values.
            sudoku = cls()
            sudoku.set_initial_values(rows)
            sudokus.append(sudoku)

        return sudokus

    @staticmethod
    def save_txt(file, sudokus):

        for sudoku in sudokus:
            file.write('%s\n\n' % (str(sudoku)))

    @classmethod
    def from_json(cls, json):

        sudoku = cls()
        sudoku.set_initial_values(json)
        sudoku.set_valid_values()

        return sudoku

    @classmethod
    def load_json(cls, file):

        sudokus = []
       
        # Parse json from file.
        data = json.load(file)

        # Iterate over difficulty levels (discard level, just reading sudos).
        for _, level_sudokus in data.items():
            for sudoku_values in level_sudokus:
                sudokus.append(Sudoku.from_json(sudoku))

        return sudokus

    @staticmethod
    def save_json(file, sudokus, level):
        
        sudokus_string = ','.join([s.to_json_string() for s in sudokus])
        file.write('{"%s":[%s]}' % (level, sudokus_string))


class SudokuCollection():

    def __init__(self):        
        self._sudokus = {}

    @property
    def sudokus(self):
        return self._sudokus;

    def set_sudokus(self, sudokus, level):
        self._sudokus[level] = sudokus

    def solve(self):

        for level, sudokus in self._sudokus.items():
            print('\n%s\n' % (level))

            for sudoku in sudokus:
                ss = SudokuSolver(sudoku)
                iterations, backtracked = ss.solve()
                print('- %s (%s)' % (iterations, backtracked))
        print()

    def test(self):

        for level, sudokus in self._sudokus.items():
            print('\n%s\n' % (level))

            for sudoku in sudokus:
                ss = SudokuSolver(sudoku)
                solutions = ss.backtrack('sorted', multiple_solutions=True)
                print('- %i' % (len(solutions)))
        print()

    def save_json(self, file):

        level_strings = []

        for level, sudokus in self._sudokus.items():

            jsons = [s.to_json_string() for s in sudokus]
            s = '    "%s": [\n%s\n    ]' % (level, ',\n'.join(jsons))
            level_strings.append(s)

        file.write('{\n%s\n}' % (',\n'.join(level_strings)))

    @classmethod
    def load_json(cls, file):

        collection = cls()

        # Parse json from file.
        data = json.load(file)

        # Iterate over difficulty levels (discard level, just reading sudos).
        for level, sudokus in data.items():
            sudokus = [Sudoku.from_json(s) for s in sudokus]
            collection.set_sudokus(sudokus, level)

        return collection

    def save_nodejs(self, file):

        pre = '(function(){\n\n    module.exports = {\n\n'
        post = '\n    };\n}());'

        level_strings = []

        for level, sudokus in self._sudokus.items():

            jsons = [s.to_json_string() for s in sudokus]
            s = '        %s: [\n%s\n        ]' % (level, ',\n'.join(jsons))
            level_strings.append(s)

        file.write('%s%s%s' % (pre, ',\n'.join(level_strings), post))


class SudokuSolver():

    # Difficulty levels.
    LEVELS = ['mild', 'difficult', 'fiendish', 'super_fiendish']

    # High weight for easy moves. 
    BLOCK_MOVE_EASE = 3
    ROW_MOVE_EASE = 1
    COLUMN_MOVE_EASE = 1
    POSITION_MOVE_EASE = 1

    def __init__(self, sudoku):

        self.sudoku = copy.deepcopy(sudoku)

    def solve(self, backtrack=False, multiple_solutions=False):

        iterations = []
        backtraced = False
        
        ease = 1

        while(ease > 0 and not self.sudoku.is_finished()):

            _, ease = self.apply_move_iteration()

            if(ease > 0):
                iterations.append(ease)

        if not(self.sudoku.is_finished()):

            backtraced = True

            if(backtrack):
                self.backtrack('sorted', multiple_solutions)

        return (iterations, backtraced)

    @staticmethod
    def ease_level(iterations, backtracked):

        if(backtracked):
            return 'impossible'

        num_iter = len(iterations)
        first = iterations[0]

        if(num_iter in [3, 4, 5] and first in range(30, 55)):
            return 'mild'

        elif((num_iter in [4, 5] and first in range(20, 30)) or
             (num_iter == 6 and first in range(30, 55))):
            return 'difficult'

        elif((num_iter == 6 and first in range(15, 30)) or
             (num_iter in [7, 8] and first in range(30, 55))):
            return 'fiendish'

        elif(num_iter >= 8 and first < 30):
            return 'super-fiendish'
        
        else:
            return 'too-easy'

    @staticmethod
    def unique_moves(partition_moves, position_moves):

        partition_union = set.union(partition_moves['row'],
                                    partition_moves['column'],
                                    partition_moves['block'])

        block_moves = partition_moves['block']
        row_moves = partition_moves['row'] - block_moves
        column_moves = (partition_moves['column'] - block_moves) - row_moves

        position_moves = position_moves - partition_union

        moves_per_type = {
            'block': block_moves,
            'row': row_moves,
            'column': column_moves,
            'position': position_moves
        }

        moves = set().union(partition_union, position_moves)

        return (moves_per_type, moves)

    @staticmethod
    def move_iteration_ease(moves):

        return\
            len(moves['row']) * SudokuSolver.ROW_MOVE_EASE +\
            len(moves['column']) * SudokuSolver.COLUMN_MOVE_EASE +\
            len(moves['block']) * SudokuSolver.BLOCK_MOVE_EASE +\
            len(moves['position']) * SudokuSolver.POSITION_MOVE_EASE

    def apply_move_iteration(self):

        partition_moves = self.sudoku.get_block_moves()
        position_moves = self.sudoku.get_position_moves()

        moves_per_type, moves =\
                SudokuSolver.unique_moves(partition_moves, position_moves)

        for cell, value in moves:
            cell.value = value

        self.sudoku.set_valid_values()

        ease = SudokuSolver.move_iteration_ease(moves_per_type)

        return (moves_per_type, ease)

    def backtrack(self, type, multiple_solutions=False):

        self._solutions = []
        self.multiple_solutions = multiple_solutions

        if(type == 'random'):
            nodes = self.sudoku.get_shuffled_valid_values()

        elif(type == 'sorted'):
            nodes = self.sudoku.get_sorted_valid_values()

        else:
            nodes = self.sudoku.get_valid_values()
    
        self._backtrack(nodes, 0)
        
        return self._solutions
    
    def _backtrack(self, nodes, tree_depth):

        # No solution?
        if(tree_depth >= len(nodes)):
            print('Done backtracing.')
            return False

        cell, values = nodes[tree_depth]

        for value in values:

            cell.value = value

            # Solution found.
            if(self.sudoku.is_finished()):

                self._solutions.append(copy.deepcopy(self.sudoku))

                if(self.multiple_solutions):
                    cell.value = None
                    return False
                else:
                    return True

            # Valid grid, but not finshed yet, proceed with next tree level.
            if(self.sudoku.is_valid() and self._backtrack(nodes, tree_depth + 1)):
                if(self.multiple_solutions):
                    cell.value = None
                return True

            # Invalid grid, skip this value
            else:
                pass

        # No more values left to explore, done with this branch, level up.
        cell.value = None
        return False


class SudokuGenerator():

    BASIC_SUDOKU_VALUES = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
    ]

    def generate(level, number):

        sudokus = []

        for i in range(number):
            s = SudokuGenerator.generate_backtrack(level)
            sudokus.append(s)

        return sudokus

    @staticmethod
    def generate_backtrack(level):

        sudoku = None

        while True:

            print('NEW')

            solution = SudokuGenerator.random_solution(method='backtrack')
            values = solution.get_values()
            coords = solution.top_triangle_coordinates()
            random.shuffle(coords)
            mask = [[False for i in range(9)] for j in range(9)]

            sudoku = SudokuGenerator._backtrack(level, values, mask, coords)

            if not (sudoku is None):
                break

        return sudoku

    @staticmethod
    def _backtrack(level, values, mask, coords):

        sys.stdout.write('.')
        sys.stdout.flush()

        # Create sudoku.
        sudoku = Sudoku()
        sudoku.set_initial_values(values)
        #print(sudoku)

        # Clear first coord in coords and rotated coord.
        coord = coords[0]
        rotated_coord = sudoku.rotated_coord(coord)
        other_coords = coords[1:]
        #print(coord)
        #print(other_coords)
        #print(rotated_coord)

        # Mask out current coordinate.
        local_mask = copy.deepcopy(mask)
        local_mask[coord[0]][coord[1]] = True
        local_mask[rotated_coord[0]][rotated_coord[1]] = True

        masked = [(i, j) for i in range(9) for j in range(9) if local_mask[i][j]]
        for c in masked:
            sudoku.get_cell(Coord.from_tuple(c)).clear_value()

        sudoku.set_valid_values()

        # Solve sudoke and determine ease level.
        solver = SudokuSolver(sudoku)
        iterations, backtraced = solver.solve()
        ease_level = SudokuSolver.ease_level(iterations, backtraced)

        #print(41 - len(other_coords))
        #print(coord)
        #print(ease_level)
        #print(sudoku)

        if(ease_level == level):
            #print('Found')
            #print(iterations)
            print()
            print(sudoku)
            return sudoku

        # Do not further explore this branch.
        if not(ease_level == 'impossible'):

            # Recursive call exploring all child-nodes.
            for index, c in enumerate(other_coords):

                rest_coords = other_coords[index:]
                result = SudokuGenerator._backtrack(level, values, local_mask, rest_coords)

                if not(result is None):
                    return result

            return None

        else:
            return None

    @staticmethod
    def generate_from_existing(sudoku):
        
        values = sudoku.get_values()
        SudokuTransform.random_transform(values)

        generated_sudoku = Sudoku()
        generated_sudoku.set_initial_values(values)

        return generated_sudoku

    ###
    # Creating random solutions.
    ###

    @staticmethod
    def random_solution(method='transform'):

        if(method == 'transform'):
            return SudokuGenerator.random_transform_solution()

        elif(method == 'backtrack'):
            return SudokuGenerator.random_backtrack_solution()

        else:
            return None

    @staticmethod
    def random_transform_solution():

        sudoku = Sudoku()
        sudoku.set_initial_values(SudokuGenerator.random_solution_values())
        sudoku.set_valid_values()

        return sudoku

    @staticmethod
    def random_solution_values():

        sudoku_values = SudokuGenerator.BASIC_SUDOKU_VALUES
        SudokuTransform.random_transform(sudoku_values)
        return sudoku_values

    @staticmethod
    def random_backtrack_solution():

        sudoku = Sudoku.empty_sudoku()
        solver = SudokuSolver(sudoku)
        solution = solver.backtrack('random')[0]

        return solution


class SudokuTransform():

    @staticmethod
    def random_transform(sudoku):

        actions = [
            SudokuTransform.random_permute,
            SudokuTransform.transpose,
            SudokuTransform.hmirror, # dubbel?
            SudokuTransform.vmirror, # dubbel?
            SudokuTransform.random_swap_rows,
            SudokuTransform.random_swap_cols,
            SudokuTransform.random_swap_block_rows,
            SudokuTransform.random_swap_block_cols
        ]

        for i in range(random.randint(100, 10000)):
            actions[random.randrange(len(actions))](sudoku)

    @staticmethod
    def random_permute(sudoku):

        # Generate random mapping from old to new value.
        value_map = dict(zip(range(1, 10), random.sample(range(1, 10), 9)))

        # Empty remains empty.
        value_map[None] = None

        # Permute sudoku with value map.
        SudokuTransform.permute(sudoku, value_map)

    @staticmethod
    def transpose(sudoku):
    
        for i in range(9):
            for j in range(9):
                if not(i == j):
                    SudokuTransform.swap_cells(sudoku, i, j, j, i)

    @staticmethod
    def hmirror(sudoku):
        
        for row_i in range(4):
            SudokuTransform.swap_rows(sudoku, row_i, 8 - row_i)

    @staticmethod
    def vmirror(sudoku):
        
        for col_i in range(4):
            SudokuTransform.swap_cols(sudoku, col_i, 8 - col_i)

    @staticmethod
    def random_swap_rows(sudoku):

        wheel = random.randrange(4)

        if(wheel == 0):
            SudokuTransform.swap_rows(sudoku, 3, 5)

        else:
            i0, i1 = random.sample(range(3), 2)
            i2 = 8 - i0;
            i3 = 8 - i1;
            SudokuTransform.swap_rows(sudoku, i0, i1)
            SudokuTransform.swap_rows(sudoku, i2, i3)

    @staticmethod
    def random_swap_cols(sudoku):

        wheel = random.randrange(4)

        if(wheel == 0):
            SudokuTransform.swap_cols(sudoku, 3, 5)

        else:
            i0, i1 = random.sample(range(3), 2)
            i2 = 8 - i0;
            i3 = 8 - i1;
            SudokuTransform.swap_cols(sudoku, i0, i1)
            SudokuTransform.swap_cols(sudoku, i2, i3)

    @staticmethod
    def random_swap_block_rows(sudoku):
        
        SudokuTransform.swap_block_rows(sudoku, 0, 2)

    @staticmethod
    def random_swap_block_cols(sudoku):

        SudokuTransform.swap_block_cols(sudoku, 0, 2)

    # helper functions

    @staticmethod
    def permute(sudoku, value_map):

        # Use mapping to replace old values with new values in sudoku.
        for i, row in enumerate(sudoku):
            for j, value in enumerate(row):
                sudoku[i][j] = value_map[value]

    @staticmethod
    def swap_cells(sudoku, i0, j0, i1, j1):

        tmp = sudoku[i0][j0]
        sudoku[i0][j0] = sudoku[i1][j1]
        sudoku[i1][j1] = tmp

    @staticmethod
    def swap_rows(sudoku, i0, i1):

        tmp = sudoku[i0]
        sudoku[i0] = sudoku[i1]
        sudoku[i1] = tmp

    @staticmethod
    def swap_cols(sudoku, j0, j1):

        for row in sudoku:       
            tmp = row[j0]
            row[j0] = row[j1]
            row[j1] = tmp

    @staticmethod
    def swap_block_rows(sudoku, i0, i1):
        
        for i in range(3):
            SudokuTransform.swap_rows(sudoku, i0 * 3 + i, i1 * 3 + i)

    @staticmethod
    def swap_block_cols(sudoku, j0, j1):
        
        for j in range(3):
            SudokuTransform.swap_cols(sudoku, j0 * 3 + j, j1 * 3 + j)
