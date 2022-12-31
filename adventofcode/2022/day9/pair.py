from __future__ import annotations
import math


def sign(val: float) -> int:
    if val == 0:
        return 0
    elif val > 0:
        return +1
    elif val < 0:
        return -1
    else:
        raise ValueError(f"Invalid value: {val}")


class Pair:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def move(self, offset) -> None:
        dx, dy = offset
        self.x += dx
        self.y += dy

    # NOTE: the self-referencing annotation here requires the __future__ to work
    def move_towards(self, other: Pair) -> None:
        dx, dy = other - self
        adx = abs(dx)
        ady = abs(dy)
        dxn = sign(dx)
        dyn = sign(dy)

        if dxn == 0 and ady > 1:
#             print("move in same column")
            self.y += dyn
        elif dyn == 0 and adx > 1:
#             print("move in same row")
            self.x += dxn
        elif dxn != 0 and dyn != 0 and (adx + ady) > 2:
#             print("move diagonally")
            self.x += dxn
            self.y += dyn
        else:
#             print("no move")
            pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __iter__(self):
        return iter([self.x, self.y])

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.x == other.x and self.y == other.y
        else:
            ox, oy = other
            return self.x == ox and self.y == oy

    def __sub__(self, other):
        if isinstance(other, Pair):
            dx, dy = -other.x, -other.y
        else:
            dx, dy = -other[0], -other[1]

        return Pair(self.x + dx, self.y + dy)


