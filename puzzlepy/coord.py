
class Coord:

    def __init__(self, i, j):
        self._i = i
        self._j = j

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    def add(self, coord):
        return Coord(self.i + coord.i, self.j + coord.j)

    @classmethod
    def from_tuple(cls, tuple):
        return cls(tuple[0], tuple[1])

    def __iter__(self):
        yield self.i
        yield self.j

    def __str__(self):
        return '(%i, %i)' % (self.i, self.j)

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

RELATIVE_COORD = [
    Coord(-1, 0),
    Coord(0, 1),
    Coord(1, 0),
    Coord(0, -1)
]

