from dataclasses import dataclass

from pair import Pair
from rope import Rope


@dataclass
class Grid:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    DELTAS = {
        "U": (0, 1),
        "D": (0, -1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    @classmethod
    def from_moves(cls, moves):
        x = xmin = xmax = 0
        y = ymin = ymax = 0

        for (dir, dist) in moves:
            dx, dy = cls.DELTAS[dir]
            x += dist*dx
            y += dist*dy
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)

        return cls(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)


    @property
    def width(self):
        return self.xmax - self.xmin + 1

    @property
    def height(self):
        return self.ymax - self.ymin + 1

    def print(self, rope: Rope):
        grid = [['.'] * self.width for _ in range(self.height)]

        grid[0 - self.ymin][0 - self.xmin] = 's'

        labels = [*range(rope.N_knots - 1, 0, -1), 'H']
        for node, label in zip(reversed(rope), labels):
            nx, ny = node
            grid[ny - self.ymin][nx - self.xmin] = label

        # NOTE: it's convenient to represent the grid "upside-down" in memory and
        # then flip it when printing
        for row in reversed(grid):
            print(*row, sep='')

    def print_visited(self, visited: set[Pair]):
        grid = [['.'] * self.width for _ in range(self.height)]

        for pt in visited:
            x, y = pt
            grid[y - self.ymin][x - self.xmin] = '#'
        grid[0 - self.ymin][0 - self.xmin] = 's'

        print("Visited map:\n============")
        # NOTE: it's convenient to represent the grid "upside-down" in memory and
        # then flip it when printing
        for row in reversed(grid):
            print(*row, sep='')
