from __future__ import annotations
import bisect
import logging
import sys
from dataclasses import dataclass
from functools import total_ordering
from typing import NamedTuple

import click


LOGGER = logging.getLogger(__name__)



@dataclass
@total_ordering
class Range:
    src_start: int
    dst_start: int
    length: int

    def __contains__(self, val: int):
        return self.src_start <= val <= self.src_start + self.length

    def __lt__(self, other: Range | int):
        if isinstance(other, Range):
            return self.src_start < other.src_start
        elif isinstance(other, int):
            return self.src_start < other
        else:
            return NotImplemented



@dataclass
class SubMap:
    SRC_START = int
    DST_START = int
    RANGE = tuple[SRC_START, DST_START, int]

    src: str
    dst: str
    ranges: list[RANGE]

    def __getitem__(self, num) -> int:
        if num < self.ranges[0].src_start:
            # fast path: all ranges start above this number, it cannot be a member of one
            return num

        rnge = next((r for r in self.ranges if num in r), None)
        if not rnge:
            LOGGER.debug("Num %r not in any %r range", num, self.dst)
            return num
        else:
            LOGGER.debug("Num %r is in %r range %r", num, self.dst, rnge)
            return rnge.dst_start + (num - rnge.src_start)


    @classmethod
    def from_lines(cls, lines: list[str]):
        header, *rest = lines
        # assume: header is formatted "SOURCE-to-DESTINATION map:"
        src, dst = header.split()[0].split("-to-")

        ranges = []
        for ln in rest:
            dst_start, src_start, length = [int(v) for v in ln.split()]
            r = Range(
                src_start=src_start,
                dst_start=dst_start,
                length=length,
            )
            bisect.insort(ranges, r)

        return cls(
            src=src,
            dst=dst,
            ranges=ranges,
        )


# assume: every type of source is connected to ONE type of destination
@dataclass
class Map:
    submaps: dict[_SOURCENAME, SubMap]

    _SOURCENAME = str
    _DESTNAME = str
    _STOP = object()

    @staticmethod
    def _get_submaps(lines: list[str]) -> list[SubMap]:
        result = []
        acc = []
        for ln in (l.strip() for l in lines):
            if not ln and acc:
                result.append(SubMap.from_lines(acc))
                acc.clear()
            elif ln:
                acc.append(ln)
        if acc:
            result.append(SubMap.from_lines(acc))

        return result

    @classmethod
    def from_lines(cls, lines: list[str]):
        submaps = {sm.src: sm for sm in cls._get_submaps(lines)}
        return cls(submaps=submaps)

    def location(self, seed: int) -> int:
        num = seed
        key = "seed"
        while key != self._STOP:
            sm = self.submaps[key]
            oldnum, num = num, sm[num]
            LOGGER.debug("%r\t%r\t->\t%r\t%r", key, oldnum, sm.dst, num)
            if sm.dst == "location":
                key = self._STOP
            else:
                key = sm.dst

        return num


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
        seed_line, *rest = f
        seeds = [int(snum) for snum in seed_line.split()[1:]]
        LOGGER.debug("seeds: %s\n", seeds)

        map = Map.from_lines(rest)

    ans1 = min(map.location(seednum) for seednum in seeds)
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
