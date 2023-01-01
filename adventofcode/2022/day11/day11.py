import logging
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
            acc.append(line)

    if acc:
        yield "\n".join(acc)


def part1(monkeys):
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
        txt = f.read()
        descs = list(monkey_descs(txt.splitlines()))
        monkeys = [Monkey.from_desc(desc) for desc in descs]

    ans1 = part1(monkeys)
    print(f"Part 1: {ans1}")

    # ans2 = part2(debug=debug)
    # print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
