from __future__ import annotations
import logging
import math
import sys
from dataclasses import dataclass
from itertools import cycle
from typing import Literal

import click


Node = str
Instruction = Literal["L", "R"]

@dataclass
class NodeMap:
    instructions: list[Instruction]
    nodes: dict[Node, tuple[Node, Node]]

    def _advance(self, node: Node, instr: Instruction) -> Node:
        dir = "LR".index(instr)
        nxt = self.nodes[node][dir]

        return nxt

    def naive_walk(self) -> int:
        cur = "AAA"
        instr = cycle(self.instructions)
        num_steps = 0
        while True:
            if cur == "ZZZ":
                break
            nxt = self._advance(cur, next(instr))
            num_steps += 1
            LOGGER.debug("Step #%d: %r → %r", num_steps, cur, nxt)
            cur = nxt

        return num_steps

    def cycle_length(self, node) -> int:
        seen = {node}
        cur = node
        instr = cycle(self.instructions)
        num_steps = 0
        while cur := self._advance(cur, next(instr)):
            num_steps += 1
            if cur in seen:
                break
            seen.add(cur)

        return num_steps

    def _starting_nodes(self) -> list[Node]:
        return [n for n in self.nodes if n.endswith('A')]

    def multiwalk(self) -> int:
        # Assume EACH starting node corresponds to a cycle in the map,
        # then the cycles will sync up after we take a number of steps
        # equal to the least common multiple of path lengths.
        #
        # This assumption does NOT have to hold for the problem as worded,
        # because the longest path(s) may not have a cycle, but can still sync
        # up with all the other paths that do. However, my input does contain
        # a cycle on every path. I'm filing this one under "advent of code is
        # communicating obtusely on purpose again".
        #
        # thanks to r/adventofcode for tipping me off to this solution
        lens = [self.cycle_length(n) for n in self._starting_nodes()]
        return math.lcm(*lens)


LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
@click.option('--no-part1', is_flag=True, default=False, help="Solve part 1")
@click.option('--no-part2', is_flag=True, default=False, help="Solve part 2")
def main(input, debug, no_part1, no_part2):
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

    if not no_part1:
        ans1 = mp.naive_walk()
        print(f"Part 1: {ans1}")

    if not no_part2:
        ans2 = mp.multiwalk()
        print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
