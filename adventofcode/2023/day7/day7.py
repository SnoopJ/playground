from __future__ import annotations
import logging
import sys
from collections import Counter
from enum import IntEnum
from functools import partial

import click


LOGGER = logging.getLogger(__name__)

# lowest to highest card rank
CARD_RANK = "23456789TJQKA"

class HandType(IntEnum):
    # lowest to highest type rank
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


def hand_type(hand: str, wildcards: bool = False) -> HandType:
    assert len(hand) == 5, "A Camel Cards hand must be exactly 5 cards"
    cnt = Counter(hand)
    counts = sorted(cnt.values(), reverse=True)
    base_type = TYPE_BY_COUNTS[tuple(counts)]
    num_wildcards = hand.count("J")
    if wildcards and num_wildcards:
        counts.remove(num_wildcards)
        if not counts:
            # edge case: five wildcards, we already have the best hand type possible
            result = HandType.FIVE_OF_A_KIND
        else:
            # take the wildcards out of the hand and add their count to the
            # next-largest count to promote this hand to the best possible hand
            counts[0] += num_wildcards
            result = TYPE_BY_COUNTS[tuple(counts)]
    else:
        result = base_type

    return result


def _hand_sort_key(hand_bid_pair, wildcards: bool = False):
    hand, bid = hand_bid_pair
    if wildcards:
        # wildcards have the lowest possible card rank
        index_key = [CARD_RANK.index(c) if c != "J" else -1 for c in hand]
    else:
        index_key = [CARD_RANK.index(c) for c in hand]
    type_key = hand_type(hand, wildcards=wildcards)

    return type_key, index_key


def winnings(plays, wildcards: bool = False) -> int:
    winnings = 0
    rank_key = partial(_hand_sort_key, wildcards=wildcards)
    for rank, (hand, bid) in enumerate(sorted(plays, key=rank_key), 1):
        hnd_t = hand_type(hand, wildcards=wildcards)
        LOGGER.debug(f"{hand = } with {bid = } is of type = {hnd_t!r} has {rank = }")
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

    ans2 = winnings(plays, wildcards=True)
    print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
