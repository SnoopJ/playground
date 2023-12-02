from __future__ import annotations
import logging
import sys
from pprint import pprint

import click
from dataclasses import dataclass


LOGGER = logging.getLogger(__name__)


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __repr__(self):
        return f"<r:{self.red}, g:{self.green}, b:{self.blue}>"

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        """Determine if the draw is possible for a given bag"""
        if self.red > red or self.green > green or self.blue > blue:
            return False

        return True

    @classmethod
    def from_text(cls, txt: str):
        cubes = {}
        for d in txt.split(","):
            num_txt, col = d.split()
            num = int(num_txt)
            cubes[col] = num

        return cls(**cubes)


@dataclass
class Game:
    number: int
    draws: list[Draw]

    @classmethod
    def from_line(cls, line: str):
        gameid, draws = line.split(":")
        _, number_txt = gameid.split()
        number = int(number_txt)
        return cls(
            number=number,
            draws=[Draw.from_text(d) for d in draws.split(";")]
        )

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        """Determine if the game is possible for a given bag"""
        return all(drw.is_possible(red, green, blue) for drw in self.draws)

    @property
    def min_cube_power(self) -> tuple[int]:
        min_cubes = {}
        for col in ("red", "green", "blue"):
            min_cubes[col] = max(getattr(drw, col) for drw in self.draws)

        LOGGER.debug(f"Game #%s requires at minimum: %r", self.number, min_cubes)

        return min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        stream=sys.stdout,
    )

    with open(input, "r") as f:
        games = [Game.from_line(line) for line in f]

    BAG = (12, 13, 14)
    for gm in games:
        LOGGER.debug("Game #%s possible? %s", gm.number, gm.is_possible(*BAG))

    ans1 = sum(gm.number for gm in games if gm.is_possible(*BAG))
    print(f"Part 1: {ans1}")

    ans2 = sum(gm.min_cube_power for gm in games)
    print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
