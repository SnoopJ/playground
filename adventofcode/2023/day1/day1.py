from __future__ import annotations
import logging
import sys

import click


LOGGER = logging.getLogger(__name__)


DIGITS_EN = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def translate_digits(line: str) -> str:
    result = line

    for word, val in DIGITS_EN.items():
        # The problem description contains an ambiguity. I HOPE it's an
        # oversight, because it's rude inclusion of the author if it isn't
        # "eightwo" should be mapped to "82", so here we duplicate the word
        # on either side of the replacement. Idea from r/adventofcode when I
        # went to see if the problem was ambiguously written.
        #
        # this replaces e.g. "two" with "two2two" so that "eightwo" will turn
        # into 82 when we're all done with this line
        repl = f"{word}{val}{word}"
        result = result.replace(word, repl)

    LOGGER.debug("[translation]: line=%r -> %r", line, result)

    return result


def first_last_digits(line: str, translate: bool = False) -> int:
    if translate:
        line = translate_digits(line)

    digit_chars = [c for c in line if c.isdigit()]
    if not digit_chars:
        LOGGER.error(f"No digit chars in {line=}, returning 0")
        return 0
    result = int(digit_chars[0] + digit_chars[-1])

    LOGGER.debug("[digits]: line=%r -> %r\n", line, result)

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
        lines = [line.strip() for line in f]

    ans1 = sum(first_last_digits(ln) for ln in lines)
    print(f"Part 1: {ans1}")

    ans2 = sum(first_last_digits(ln, translate=True) for ln in lines)
    print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
