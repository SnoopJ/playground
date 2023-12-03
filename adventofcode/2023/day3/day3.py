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
class SchematicPartNumber:
    num: int
    row: int
    col: int


@dataclass
class Schematic:
    rows: tuple[str]

    UNSYMS = ".0123456789"
    neighbor_indices = tuple(itertools.product(range(-1, 2), repeat=2))

    @property
    def nrows(self) -> int:
        return len(self.rows)

    @property
    def ncols(self) -> int:
        assert len(len(r) == len(self.rows[0]) for r in self.rows[1:]), "Schematic columns are not even-width!"
        return len(self.rows[0])

    def part_numbers(self) -> tuple[SchematicPartNumber]:
        result = []

        for num, ridx, cidx in self._schematic_numbers():
            if self.has_symbol_neighbor(ridx, cidx):
                LOGGER.debug("Found part number at (%s, %s): %s", ridx, cidx, num)
                pn = SchematicPartNumber(num=num, row=ridx, col=cidx)
                result.append(pn)
            else:
                LOGGER.debug("Number %s at (%s, %s) is NOT a part number", num, ridx, cidx)
            LOGGER.debug("-"*40)

        return tuple(result)

    def _schematic_numbers(self) -> Iterable[tuple[int, int, int]]:
        for ridx, row in enumerate(self.rows):
            for m in re.finditer(r"\d+", row):
                cidx = m.start()
                num = int(m.group())
                yield num, ridx, cidx

    def has_symbol_neighbor(self, rowidx: int, colidx: int) -> bool:
        col_offset = 0

        while True:
            cidx = colidx + col_offset
            if cidx < 0 or cidx >= len(self.rows[0]):
                break

            # if a character is not an "unsymbol" it is a symbol by definition
            # insofar as AoC 2023 is doing """definitions""" anyway :|
            for n in self.neighbors(rowidx, cidx):
                if n not in self.UNSYMS:
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
        format="%(levelname)s: %(message)s",
    )

    with open(input, "r") as f:
        schematic = Schematic(tuple(line.strip() for line in f))

    partnums = schematic.part_numbers()
    ans1 = sum(pn.num for pn in partnums)
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
