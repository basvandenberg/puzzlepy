from subset import SubSet

class Partition:

    def __init__(self, name, partition, grid):

        self._name = name
        self._partition = partition
        self._grid = grid

        self._valid_rule = None
        self._finished_rule = None

        self._subsets = None
        self._init_subsets(name, partition)

    @property
    def name(self):
        return self._name

    @property
    def partition(self):
        return self._partition

    @property
    def grid(self):
        return self._grid

    @property
    def valid_rule(self):
        return self._valid_rule

    @valid_rule.setter
    def valid_rule(self, rule):
        self._valid_rule = rule

    @property
    def finished_rule(self):
        return self._finished_rule

    @finished_rule.setter
    def finished_rule(self, rule):
        self._finished_rule = rule

    def _init_subsets(self, name, partition):

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

        for subset in self.subsets:
            if not(subset.is_valid()):
                return False

        return True

    def is_finished(self):

        for subset in self.subsets:
            if not(subset.is_finished()):
                return False

        return True

    def has_empty_subset(self):

        for subset in self.subsets:
            if(subset.is_empty()):
                return True

        return False

    def __iter__(self):
        return iter(self.subsets)
