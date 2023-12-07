from __future__ import annotations
import logging
import math
import operator
import sys
from functools import reduce

import click


LOGGER = logging.getLogger(__name__)


CHARGE_RATE = 1  # mm/msec/msec
def thresholds(T: int, D: int) -> tuple[int, int]:
    """
    values of t_c for which the boat will travel farther than the record

    Δ = D - (tc * CR * (T - tc))
      = CR * tc² - T*CR * tc + D
    Δ = 0 →  tc = T*CR ± sqrt(T²*CR² - 4*CR*D) / (2 * CR)

    """
    CR = CHARGE_RATE
    negb = T*CR
    sqrtb2fourac = math.sqrt(T**2 * CR**2 - 4 * CR * D)
    twoa = (2 * CR)

    lo = (negb - sqrtb2fourac) / twoa
    hi = (negb + sqrtb2fourac) / twoa

    return math.ceil(lo), math.floor(hi + 0.5)


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

    num_wins = []
    for T, D in zip(times, dists):
        lo, hi = thresholds(T, D)
        num_wins.append(hi - lo)
    ans1 = reduce(operator.mul, num_wins)
    print(f"Part 1: {ans1}")

    # this is a fairly lazy way to concatenate all the digits
    T = int("".join(str(v) for v in times))
    D = int("".join(str(v) for v in dists))

    lo, hi = thresholds(T, D)
    ans2 = hi - lo
    print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
