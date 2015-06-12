
class Cell:

    def __init__(self, coord):

        self.coord = coord
        self.neighbors = [None, None, None, None]

        self.init_value = None
        self.value = None

        self.valid_values = None
        self.marks = set()

        self.active = False
        self.valid = True

        self.partition_subsets = {}

    def set_initial_value(self, value):

        self.initial_value = value
        self.set_value(value)

    def set_value(self, value):

        self.valid_values = None
        self.value = value

    def clear_value(self):

        self.value = None

    def set_marks(self, marks):

        self.marks = marks

    def add_mark(self, mark):

        self.marks.add(mark)

    def clear_marks(self):

        self.marks = set()

    def add_to_partition_subset(self, partition_name, subset_index):

        self.partition_subsets[partition_name] = subset_index

    def __str__(self):

        if(self.value is None):
            return '.'
        else:
            return str(self.value)
