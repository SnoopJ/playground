from __future__ import annotations
import itertools
import logging
import re
import sys
from dataclasses import dataclass
from typing import Iterable

import click


LOGGER = logging.getLogger(__name__)


@dataclass
class Schematic:
    rows: list[str]

    UNSYMS = ".0123456789"
    neighbor_indices = list(itertools.product(range(-1, 2), repeat=2))

    @property
    def nrows(self) -> int:
        return len(self.rows)

    @property
    def ncols(self) -> int:
        assert len(len(r) == len(self.rows[0]) for r in self.rows[1:]), "Schematic columns are not even-width!"
        return len(self.rows[0])

    def part_numbers(self) -> Iterable[int]:
        for ridx, r in enumerate(self.rows):
            for m in re.finditer(r"\d+", r):
                cidx = m.start()
                num = int(m.group())
                if self.is_part_number(ridx, cidx):
                    LOGGER.debug("Found part number at (%s, %s): %s", ridx, cidx, num)
                    yield num
                else:
                    LOGGER.debug("Number %s at (%s, %s) is NOT a part number", num, ridx, cidx)

    def is_part_number(self, rowidx: int, colidx: int) -> bool:
        col_offset = 0
        while True:
            cidx = colidx + col_offset
            if cidx >= len(self.rows[0]) or not self.rows[rowidx][cidx].isdigit():
                break

            # if a character is not an "unsymbol" it is a symbol by definition
            # insofar as AoC 2023 is doing """definitions""" anyway :|
            if any(n not in self.UNSYMS for n in self.neighbors(rowidx, cidx)):
                return True

            col_offset += 1

        return False

    def neighbors(self, rowidx: int, colidx: int) -> Iterable[str]:
        assert rowidx >= 0 and colidx >= 0, "Negative row or column indices not supported"

        for (r_offset, c_offset) in self.neighbor_indices:
            r = rowidx + r_offset
            c = colidx + c_offset
            if r < 0 or c < 0 or r >= len(self.rows) or c >= len(self.rows[0]):
#                 LOGGER.debug("Skipping off-edge neighbor (%s, %s) of (%s, %s)", r, c, rowidx, colidx)
                continue

            yield self.rows[r][c]


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        stream=sys.stdout,
    )

    with open(input, "r") as f:
        schematic = Schematic([line.strip() for line in f])

    ans1 = sum(schematic.part_numbers())
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
