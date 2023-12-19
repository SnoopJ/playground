from __future__ import annotations
import logging
import sys
from dataclasses import dataclass
from itertools import cycle
from typing import Literal

import click


Node = str

@dataclass
class NodeMap:
    instructions: list[Literal["L", "R"]]
    nodes: dict[Node, tuple[Node, Node]]

    def walk(self) -> int:
        cur = "AAA"
        instr = cycle(self.instructions)
        num_steps = 0
        while True:
            if cur == "ZZZ":
                break
            dir = "LR".index(next(instr))
            nxt = self.nodes[cur][dir]
            num_steps += 1
            LOGGER.debug("Step #%d: %r → %r", num_steps, cur, nxt)
            cur = nxt

        return num_steps



LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        stream=sys.stdout,
        format="%(levelname)s: %(message)s",
    )

    with open(input, "r") as f:
        instructions = next(f).strip()
        sep = next(f).strip()
        assert sep == "", f"Expected empty line, got {sep!r}"
        # remaining lines are node declarations
        nodes = {}
        for line in f:
            node_name, connections = [part.strip() for part in line.split('=')]
            L, R = [cn.strip('() ') for cn in connections.split(',')]
            nodes[node_name] = (L, R)

        mp = NodeMap(instructions=instructions, nodes=nodes)

    ans1 = mp.walk()
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
