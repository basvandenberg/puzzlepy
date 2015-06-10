
class Partition:

    def __init__(self, name, partition, grid):

        self.name = name
        self.partition = partition
        self.grid = grid
        self.rule = None

        self.subsets = self._create_subsets(name, partition)

    def _create_subsets(self, name, partition):

        max_index = 0

        for i in range(self.grid.m):
            for j in range(self.grid.n):

                self.grid.cells[i][j].add_to_partition_subset(name,
                        partition[i][j])

                max_index = max(max_index, partition[i][j])

        subsets = []

        for i in range(max_index):
            subsets[i].push([])

        for i in range(self.grid.m):
            for j in range(self.grid.n):

                subsets[partition[i][j]].append(self.grid.cells[i][j])
        
        return subsets

    def set_rule(self, rule):

        self.rule = rule


    def is_valid(self):

        for i in range(len(self.subsets)):

            if not(self.rule(self.subsets[i])):
                return False

        return True

