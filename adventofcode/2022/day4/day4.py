from itertools import count
import string

import click


Assignment = tuple[int, int]


def sections(line: str) -> tuple[Assignment, Assignment]:
    assmnts = line.split(',')
    return tuple(tuple(int(num) for num in assmnt.split('-')) for assmnt in assmnts)


def overlap(a: Assignment, b: Assignment, full: bool = False) -> bool:
    # NOTE: assuming that a,b are sorted here, i.e. a1 <= a2, b1 <= b2
    a1, a2 = a
    b1, b2 = b

    if full:
        if ((a1 <= b1 and a2 >= b2) or
            (b1 <= a1 and b2 >= a2)):
            return True
    else:
        if ((a1 <= b1 and a2 >= b1) or
            (b1 <= a1 and b2 >= a1)):
            return True

    return False


def part1(assmnts: list[Assignment]):
    overlaps = 0
    for a, b in assmnts:
        if overlap(a, b, full=True):
            overlaps += 1
#             print(f"Full overlap: {a}, {b}")

    return overlaps


def part2(assmnts: list[Assignment]):
    overlaps = 0
    for a, b in assmnts:
        if overlap(a, b, full=False):
            overlaps += 1
#             print(f"Partial overlap: {a}, {b}")

    return overlaps


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        assignments = [sections(line) for line in f]

    num_full_overlaps = part1(assignments)
    print(f"Part 1: {num_full_overlaps} full overlaps")

    num_overlaps = part2(assignments)
    print(f"Part 2: {num_overlaps} overlaps")

if __name__ == '__main__':
    main()
