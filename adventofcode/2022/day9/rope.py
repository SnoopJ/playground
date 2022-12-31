from dataclasses import dataclass, field

from pair import Pair


@dataclass
class Rope:
    N_knots: int
    x0: int = 0
    y0: int = 0
    # head-to-tail order
    _nodes: list[Pair] = field(init=False)

    def __post_init__(self):
        assert self.N_knots >= 2
        self._nodes = [Pair(self.x0, self.y0) for _ in range(self.N_knots)]

    @property
    def head(self):
        return self._nodes[0]

    @head.setter
    def set_head(self, newhead):
        self._nodes[0] = newhead

    @property
    def tail(self):
        return self._nodes[-1]

    @tail.setter
    def set_tail(self, newtail):
        self._nodes[-1] = newtail

    def __iter__(self):
        return iter(self._nodes)

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, idx: int):
        return self._nodes[idx]

    def move_head(self, offset):
        self.head.move(offset)

        for dest, mover in zip(self._nodes, self._nodes[1:]):
            mover.move_towards(dest)

