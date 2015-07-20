
class SubSet:

    def __init__(self, cells, partition, index):

        self._cells = cells
        self._partition = partition
        self._index = index

    @property
    def cells(self):
        return self._cells

    @property
    def partition(self):
        return self._partition

    @property
    def index(self):
        return self._index

    def is_valid(self):
        values = [c.value for c in self if not c.value is None]
        return self.partition.valid_rule(values)

    def is_finished(self):
        values = [c.value for c in self if not c.value is None]
        return self.partition.finished_rule(values)
 
    def is_empty(self):
        return len([c.value for c in self if not c.value is None]) == 0

    def __iter__(self):
        return iter(self.cells)
