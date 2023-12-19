from __future__ import annotations
import logging
import sys

import click


LOGGER = logging.getLogger(__name__)


def differences(history: list[int]) -> list[list[int]]:
    result = [history]
    cur = history
    while any(cur):
        cur = [b-a for a, b in zip(cur, cur[1:])]
        result.append(cur)
    return result


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
        histories = [[int(val) for val in line.split()] for line in f]

    ans1 = sum(sum(diff[-1] for diff in differences(hist)) for hist in histories)
    print(f"Part 1: {ans1}")

#     ans2 = another_miracle_occurs(lines)
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
