import logging
import sys

import click


LOGGER = logging.getLogger(__name__)


def part1():
    pass


def part2():
    pass


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        stream=sys.stdout,
    )

    with open(input, "r") as f:
        lines = [line.strip() for line in f]

#     ans1 = part1()
#     print(f"Part 1: {ans1}")

#     ans2 = part2()
#     print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
