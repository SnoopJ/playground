from __future__ import annotations
import logging
import sys
from collections import Counter
from enum import IntEnum

import click


LOGGER = logging.getLogger(__name__)

# lowest to highest rank
CARD_RANK = "23456789TJQKA"

class HandType(IntEnum):
    # lowest to highest rank
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

TYPE_BY_COUNTS = {
    (5,): HandType.FIVE_OF_A_KIND,
    (4, 1): HandType.FOUR_OF_A_KIND,
    (3, 2): HandType.FULL_HOUSE,
    (3, 1, 1): HandType.THREE_OF_A_KIND,
    (2, 2, 1): HandType.TWO_PAIR,
    (2, 1, 1, 1): HandType.ONE_PAIR,
    (1, 1, 1, 1, 1): HandType.HIGH_CARD,
}


def hand_type(hand: str) -> HandType:
    assert len(hand) == 5, "A Camel Cards hand must be exactly 5 cards"
    cnt = Counter(hand)
    counts = sorted(cnt.values(), reverse=True)
    return TYPE_BY_COUNTS[tuple(counts)]


def _rank_key(hand_bid_pair):
    hand, bid = hand_bid_pair
    return hand_type(hand), [CARD_RANK.index(c) for c in hand]


def winnings(plays) -> int:
    winnings = 0
    for rank, (hand, bid) in enumerate(sorted(plays, key=_rank_key), 1):
        LOGGER.debug(f"{hand = } with {bid = } has {rank = }")
        winnings += rank * int(bid)

    return winnings


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
        plays = [line.strip().split() for line in f]

    ans1 = winnings(plays)
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
