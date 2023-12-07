from __future__ import annotations
import logging
import operator
import sys
from functools import reduce

import click


LOGGER = logging.getLogger(__name__)


CHARGE_RATE = 1  # mm/msec/msec

def dist(T, tc):
    return tc * CHARGE_RATE * (T - tc)


# NOTE: this approach is very naive, we could do some calculus instead and maybe we'll need to in part 2
def num_wins(times, dists):
    nums = []
    for num, (T, record_dist) in enumerate(zip(times, dists), 1):
        LOGGER.debug("Considering race #%r of max time %r, record distance is %r", num, T, record_dist)
        n = 0
        for tc in range(0, T+1):
            d = dist(T, tc)
            if d > record_dist:
                n += 1
                LOGGER.debug("Charging for tc=%r msec wins with distance %r", tc, d)
        LOGGER.debug("%r ways to win", n)
        nums.append(n)
        LOGGER.debug("---\n")

    return nums


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
        times = [int(v) for v in next(f).split()[1:]]
        dists = [int(v) for v in next(f).split()[1:]]

    ans1 = reduce(operator.mul, num_wins(times, dists))
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
