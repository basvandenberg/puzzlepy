
class Coord:

    def __init__(self, i, j):

        self.i = i
        self.j = j

    def add(self, coord):

        return Coord(self.i + coord.i, self.j + coord.j)

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

