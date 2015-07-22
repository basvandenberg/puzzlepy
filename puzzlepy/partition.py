from puzzlepy.subset import SubSet

class Partition:

    def __init__(self, name, partition, grid):
        '''Initializes partition and its subsets.'''

        self._name = name
        self._grid = grid

        # Partition specific value (int, list, dict, or ...)
        self._value = None
        self._valid_rule = None
        self._finished_rule = None

        self._partition = partition
        self._init_subsets(name, partition)

    @property
    def name(self):
        '''Return the partition name.'''
        return self._name

    @property
    def grid(self):
        '''Return the grid which is subdivided by this partition.'''
        return self._grid

    @property
    def value(self):
        '''Return the partition's value, which can be anything.'''
        return self._value

    @value.setter
    def value(self, value):
        '''Set the partition's value.'''
        self._value = value

    @property
    def valid_rule(self):
        '''Return the rule that checks if a partition subset is valid.'''
        return self._valid_rule

    @valid_rule.setter
    def valid_rule(self, rule):
        '''Set the rule that checks if a partition subset is valid.'''
        self._valid_rule = rule

    @property
    def finished_rule(self):
        '''Return the rule that checks if a partition subset is finished.'''
        return self._finished_rule

    @finished_rule.setter
    def finished_rule(self, rule):
        '''Set the rule that checks if a partition subset is finished.'''
        self._finished_rule = rule

    def _init_subsets(self, name, partition):
        '''Initialize the partition subsets based on the provided partion.'''

        max_index = 0

        for i in range(self.grid.m):
            for j in range(self.grid.n):

                self.grid.cells[i][j].add_to_partition_subset(name,
                        partition[i][j])

                max_index = max(max_index, partition[i][j])

        subsets = []

        for i in range(max_index + 1):
            subsets.append([])

        for i in range(self.grid.m):
            for j in range(self.grid.n):

                subsets[partition[i][j]].append(self.grid.cells[i][j])
        
        self.subsets = []
        for index, subset in enumerate(subsets):
            self.subsets.append(SubSet(subset, self, index))

    def is_valid(self):
        '''Return if this partition is valid, which means that all of its
        subsets are valid according to the valid_rule.'''

        for subset in self.subsets:
            if not(subset.is_valid()):
                return False

        return True

    def is_finished(self):
        '''Return if this partition is finished, which means that all of its
        subsets are finished according to the finished_rule.'''

        for subset in self.subsets:
            if not(subset.is_finished()):
                return False

        return True

    def has_empty_subset(self):
        '''Returns if any of this partition's subsets is empty.'''

        for subset in self.subsets:
            if(subset.is_empty()):
                return True

        return False

    def __iter__(self):
        '''Iterate over the subsets in this partition.'''

        return iter(self.subsets)
