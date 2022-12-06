from itertools import count
import string

import click


def to_priority(char: str) -> int:
    # fun trivia: this would NOT be reliable in Python 2.7 because the order
    # of string.ascii_letters can change based on your locale
    # https://bugs.python.org/issue39084
    # (it's fine on Python 3 though)
    return string.ascii_letters.index(char) + 1


def part1(rucksacks: list[str]) -> int:
    common_value = 0
    for sak in rucksacks:
        container_size = len(sak) // 2
        first, second = sak[:container_size], sak[container_size:]
        common = set(first) & set(second)
        val = sum(to_priority(item) for item in common)
        common_value += val

    return common_value


def part2(rucksacks: list[str]) -> int:
    it = iter(rucksacks)
    accum = 0

    for groupnum in count(1):
        try:
            r1, r2, r3 = [next(it) for _ in range(3)]
        except StopIteration:
            break
        common = set(r1) & set(r2) & set(r3)
        assert len(common) == 1, "Found more than one common item"

        common_value = to_priority(*common)
        accum += common_value
#         print(f"Group #{groupnum} has common item {common=} (value {common_value})")

    return accum


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        rucksacks = [line.strip() for line in f]

    common_value = part1(rucksacks)
    print(f"Part 1 - sum of common values: {common_value}")

    assert len(rucksacks)/3 == len(rucksacks)//3, "Rucksacks do not divide into groups of 3"
    group_priorities = part2(rucksacks)
    print(f"Part 2 - sum of group priorities: {group_priorities}")


if __name__ == '__main__':
    main()
