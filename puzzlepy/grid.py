import random

from puzzlepy import coord
from puzzlepy.coord import Coord
from puzzlepy.cell import Cell
from puzzlepy.partition import Partition

class Grid:

    def __init__(self, m, n):

        self._m = m
        self._n = n

        self._cells = []
        self._partitions = {}

        self._allowed_values = None

        self._init_cells()
        self._init_neighbors()

    @property
    def m(self):
        return self._m

    @property
    def n(self):
        return self._n

    @property
    def cells(self):
        return self._cells

    @property
    def partitions(self):
        return self._partitions

    @property
    def allowed_values(self):
        return self._allowed_values

    def _init_cells(self):

        for i in range(self.m):
            row = []

            for j in range(self.n):
                row.append(Cell(Coord(i, j)))

            self.cells.append(row)

    def _init_neighbors(self):

        for i in range(self.m):
            for j in range(self.n):
                for d in range(4):

                    cell = self.cells[i][j]
                    neighbor_coord = cell.coord.add(coord.RELATIVE_COORD[d])

                    cell.neighbors[d] = self.get_cell(neighbor_coord)

    def get_cell(self, coord):

        if(self.within_bounds(coord)):
            return self.cells[coord.i][coord.j]

        return None

    def within_bounds(self, coord):

        return (coord.i > -1 and coord.i < self.m and 
                coord.j > -1 and coord.j < self.n)

    def set_initial_values(self, values):

        for cell in self:
            cell.initial_value = values[cell.coord.i][cell.coord.j]

    def get_values(self):

        values = []

        for i in range(self.m):
            row = []

            for j in range(self.n):
                row.append(self.cells[i][j].value)

            values.append(row)

        return values

    def add_partition(self, name, partition):

        self.partitions[name] = Partition(name, partition, self)

    def is_valid(self):
        return all([p.is_valid() for p in self.partitions.values()])

    def is_finished(self):
        return all([p.is_finished() for p in self.partitions.values()])

    def has_empty_partition_subset(self):

        for key, partition in self.partitions.items():
            if(partition.has_empty_subset()):
                return True

        return False

    def empty_cells(self):
    
        for cell in [c for c in self if c.is_empty()]:
            yield cell

    def print_valid_values(self):

        for cell in self.empty_cells():
            i, j = cell.coord
            print('(%i, %i): %s' % (i, j, str(cell.valid_values)))

    def print_sorted_valid_values(self):

        for cell, values in self.get_sorted_valid_values():
            print('(%i, %i): %s' % (cell.coord.i, cell.coord.j, str(values)))

    def get_valid_values(self):

        return [(c, sorted(c.valid_values)) for c in self.empty_cells()]

    def get_sorted_valid_values(self):

        values = self.get_valid_values()
        values.sort(key=lambda v: len(v[1]))

        return values

    def get_shuffled_valid_values(self):

        values = self.get_valid_values()
        for _, v in values:
            random.shuffle(v)

        return values

    def shuffled_coordinates(self):

        coords = [(i, j) for i in range(self.m) for j in range(self.n)]
        random.shuffle(coords)

        return coords

    def top_triangle_coordinates(self):
        '''Returns the coordinates of the top trianglar grid part.
        
        The coordinates retured cover the top triangular part with the top
        half of the diagonal coordinates including the coordinate of the cell
        at the grid center.

        It is assumed that the grid is square with odd m and n.

        For a 5x5 grid this would return the following coordinates
        (* = returned coordinate, . = not returned).

        * * * * *
        . * * * *
        . . * * *
        . . . . *
        . . . . .

        For a 9x9 grid this function would return the following coordinates:

        * * * * * * * * *
        . * * * * * * * *
        . . * * * * * * *
        . . . * * * * * *
        . . . . * * * * *
        . . . . . . * * *
        . . . . . . . * *
        . . . . . . . . *
        . . . . . . . . .

        '''

        coords = []
        center = self.m // 2

        for i in range(self.m):
            start = i if i <= center else i + 1

            for j in range(start, self.n):
                coords.append((i, j))

        return coords

    def rotated_coord(self, coord):

        # Assumes odd m and n
        center_m = self.m // 2
        center_n = self.n // 2

        i, j = coord

        rotated_i = (center_m - i) + center_m
        rotated_j = (center_n - j) + center_n

        return (rotated_i, rotated_j)

    # Often used partitions

    def add_row_partition(self):

        partition = []

        for i in range(self.m):
            row = []

            for j in range(self.n):
                row.append(i);

            partition.append(row)

        self.partitions['row'] = Partition('row', partition, self)

    def add_column_partition(self):

        partition = []

        for i in range(self.m):
            row = []

            for j in range(self.n):
                row.append(j);

            partition.append(row)

        self.partitions['column'] = Partition('column', partition, self)

    def add_block_partition(self, num_row_blocks, num_col_blocks):

        partition = []

        for i in range(self.m):
            row = []

            for j in range(self.n):

                block_i = i // num_row_blocks
                block_j = j // num_col_blocks

                row.append(block_i * num_col_blocks + block_j);

            partition.append(row)

        self.partitions['block'] = Partition('block', partition, self)

    #
    #
    #

    def __str__(self):

        result = ''

        for i in range(self.m):
            for j in range(self.n):
                result += str(self.cells[i][j]) + ' '

            result += '\n'

        return result

    def __iter__(self):

        for i in range(self.m):
            for j in range(self.n):
                yield self.cells[i][j]

