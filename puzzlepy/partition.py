
class Partition:

    def __init__(self, name, partition, grid):

        self.name = name
        self.partition = partition
        self.grid = grid

        self.valid_rule = None
        self.finished_rule = None

        self.subsets = self._create_subsets(name, partition)

    def _create_subsets(self, name, partition):

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
        
        return subsets

    def __iter__(self):
        return iter(self.subsets)

    def set_valid_rule(self, rule):

        self.valid_rule = rule

    def set_finished_rule(self, rule):

        self.finished_rule = rule

    def is_valid(self):

        for subset in self.subsets:
            if not(self.is_valid_subset(subset)):
                return False

        return True

    def is_valid_subset(self, subset):

        values = [c.value for c in subset if not c.value is None]
        return self.valid_rule(values)

    def is_finished(self):

        for subset in self.subsets:
            if not(self.is_finished_subset(subset)):
                return False

        return True

    def is_finished_subset(self, subset):

        values = [c.value for c in subset if not c.value is None]
        return self.finished_rule(values)
