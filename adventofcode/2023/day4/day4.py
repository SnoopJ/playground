from __future__ import annotations
import logging
import sys
from dataclasses import dataclass

import click


LOGGER = logging.getLogger(__name__)

@dataclass
class Card:
    id: int
    wins: set[int]
    nums: tuple[int]

    @property
    def winning_numbers(self) -> set[int]:
        return self.wins.intersection(self.nums)

    @property
    def score(self) -> int:
        if self.winning_numbers:
            scr = 2**(len(self.winning_numbers) - 1)
        else:
            scr = 0

        LOGGER.debug("Card #%s has score %s", self.id, scr)

        return scr

    @classmethod
    def from_line(cls, line: str):
        card_id, nums = line.split(":")

        _, id_txt = card_id.split()
        id = int(id_txt)

        wins_txt, nums_txt = nums.split("|")
        wins = set(int(w) for w in wins_txt.split())
        nums = tuple(int(n) for n in nums_txt.split())

        return cls(
            id=id,
            wins=wins,
            nums=nums,
        )



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
        cards = [Card.from_line(line) for line in f]

    ans1 = sum(c.score for c in cards)
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
