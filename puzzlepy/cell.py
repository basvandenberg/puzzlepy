
class Cell:

    def __init__(self, coord):

        self._coord = coord
        self._neighbors = [None, None, None, None]

        self._value = None
        self._initial_value = False

        self._valid_values = None
        self._marks = set()

        self._active = False
        self._valid = True

        self._partition_subsets = {}

    @property
    def coord(self):
        return self._coord

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def initial_value(self):
        return self._initial_value;

    @initial_value.setter
    def initial_value(self, value):
        self._initial_value = True
        self.value = value

    @property
    def value(self):
        return self._value;

    @value.setter
    def value(self, value):
        self._value = value
        self.valid_values = None

    def clear_value(self):
        self.value = None

    def is_empty(self):
        return self.value is None

    @property
    def valid_values(self):
        return self._valid_values

    @valid_values.setter
    def valid_values(self, values):
        self._valid_values = values

    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self, marks):
        self._marks = marks

    def add_mark(self, mark):
        self.marks.add(mark)

    def clear_marks(self):
        self.marks = set()

    @property
    def active(self):
        return self._active

    @property
    def valid(self):
        return self._valid

    @property
    def partition_subsets(self):
        return self._partition_subsets

    def add_to_partition_subset(self, partition_name, subset_index):
        self.partition_subsets[partition_name] = subset_index

    def __str__(self):

        if(self.value is None):
            return '.'
        else:
            return str(self.value)
