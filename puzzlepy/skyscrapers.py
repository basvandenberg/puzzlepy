from puzzlepy.grid import Grid

class Skyscrapers(Grid):

    def __init__(self, size):
        
        super().__init__(size, size)

        self.add_row_partition()
        self.add_column_partition()

        self.allowed_values = set(range(1, size + 1))

        self.partitions['row'].valid_rule = valid_rule
        self.partitions['column'].valid_rule = valid_rule

        self.partitions['row'].finished_rule = finished_rule
        self.partitions['column'].finished_rule = finished_rule

    def set_initial_cell_values(values):
        pass

    def set_row_partition_values():
        pass

    def set_col_partition_values():
        pass

    def valid_rule(values):
        pass

    def finished_rule(values):
        return len(self.allowed_values.difference(set(values))) == 0
