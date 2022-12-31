from itertools import count
import string

import click


def find_header(data: str, width: int) -> int:
    window = zip(*[data[n:] for n in range(width)])
    for idx,chars in enumerate(window):
        if len(set(chars)) == width:
            print(f"{width} unique chars found at offset {idx=}: {chars}")
            return idx + width

    raise ValueError("not found")


def part1(data) -> int:
    return find_header(data, 4)


def part2(data):
    return find_header(data, 14)


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        data = f.read().strip()


    ans1 = part1(data)
    print(f"Part 1: {ans1}")

    ans2 = part2(data)
    print(f"Part 2: {ans2}")

if __name__ == '__main__':
    main()
