from functools import reduce
import logging
import operator
import sys

import click

from monkey import Monkey, MonkeyBusiness, MonkeyMatcher


LOGGER = logging.getLogger(__name__)


def monkey_descs(lines) -> list[str]:
    acc = []

    for line in lines:
        if not line.strip():
            yield "\n".join(acc)
            acc.clear()
        else:
            acc.append(line.rstrip())

    if acc:
        yield "\n".join(acc)


def part1(descs):
    monkeys = [Monkey.from_desc(desc) for desc in descs]
    biz = MonkeyBusiness(monkeys)

    for roundnum in range(1, 21):
        biz.handle_round()
        LOGGER.debug("After round #%s, monkey inventories are:", roundnum)
        for monk in monkeys:
            LOGGER.debug("  Monkey %s: %s", monk.id, monk.items)

    counts = {monk.id: monk.inspection_count for monk in monkeys}
    for id, count in counts.items():
        print(f"Monkey {id} inspected items {count} times.")

    a, b = sorted(counts.values(), reverse=True)[:2]

    return a*b


def part2(descs):
    monkeys = [Monkey.from_desc(desc, worry_control=False) for desc in descs]

    # AoC makes this problem harder by allowing the item worry values grow
    # unbounded, but since all of the tests hinge on modular arithmetic, we
    # can bound the worries above by the product of all the test divisors
    #
    # This requires O(N_items) work on each iteration but does bring the program
    # runtime back into reach of reality
    cap = reduce(operator.mul, [monk.test.divisor for monk in monkeys])

    biz = MonkeyBusiness(monkeys)

    for roundnum in range(1, 10_001):
        biz.handle_round()
        LOGGER.debug("After round #%s, monkey inventories are:", roundnum)
        for monk in monkeys:
            LOGGER.debug("  Monkey %s: %s", monk.id, monk.items)
            monk.items = [item % cap for item in monk.items]

    counts = {monk.id: monk.inspection_count for monk in monkeys}
    for id, count in counts.items():
        print(f"Monkey {id} inspected items {count} times.")

    a, b = sorted(counts.values(), reverse=True)[:2]

    return a*b


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        stream=sys.stdout,
    )

    with open(input, "r") as f:
        descs = list(monkey_descs(f))

    ans1 = part1(descs)
    print(f"Part 1: {ans1}")

    ans2 = part2(descs)
    print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
