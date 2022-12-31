"""
NOTE: This day's solution requires Python 3.10+

For whatever reason, I decided to deliberately avoid the 'natural' recursive
approach to this problem, so I ended up with a two-phase program that builds a
file tree and then sums over it. This approach is slower but handles
arbitrarily-deep hierarchies… which is a bit silly, because Python can handle
call stacks MUCH deeper than this problem is calling (heh) for :)
"""
from collections import Counter
from pathlib import PurePath
from pprint import pprint

import click


Command = str
Output = list[str]
Session = list[tuple[Command, Output]]

def parse_session(lines) -> Session:
    tree = {}

    session = []
    output = []
    cmd = None

    for line in lines:
        if line.startswith("$"):
            if cmd:
                session.append((cmd, output))
                output = []
            cmd = line[1:].strip()
        else:
            output.append(line)

    # edge case: catch the last command
    session.append((cmd, output))

    return session


def build_tree(session: Session) -> Counter:
    tree = {}

    cwd = PurePath()
    ROOT = PurePath("/")

    for cmd, output in session:
        match cmd.split():
            case ["cd", dr]:
                oldwd = cwd
                if dr.startswith("/"):
                    cwd = PurePath(dr)
                elif dr == "..":
                    if cwd != ROOT:
                        cwd = PurePath(*cwd.parts[:-1])
                else:
                    cwd = cwd.joinpath(dr)
            case ["ls"]:
                for entry in output:
                    sz, fn = entry.split()
                    if sz == "dir":
                        continue
                    else:
                        full_fn = cwd.joinpath(fn)
                        tree[full_fn] = int(sz)

    return tree


def dir_sizes(tree: dict) -> Counter:
    sizes = Counter()

    for pth, sz in tree.items():
        nparts = len(pth.parts)
        if nparts > 2:
            parents = [PurePath(*pth.parts[:n]) for n in range(1, nparts)]
        else:
            parents = [PurePath("/")]

        for p in parents:
            sizes[p] += sz

    return sizes


def part1(sizes: Counter) -> int:
    total = 0
    for pth, sz in sizes.items():
        if sz <= 100_000:
            total += sz

    return total


def part2(sizes: Counter, fs_size: int, target_size: int):
    free = fs_size - sizes[PurePath("/")]
    delta = target_size - free
    candidates = [(pth, sz) for pth, sz in sizes.items() if sz >= delta]
#     print(f"{delta=}")
#     print(candidates)

    return min(candidates, key=lambda pair: pair[1])


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        lines = [line.strip() for line in f]

    session = parse_session(lines)
    tree = build_tree(session)
    sizes = dir_sizes(tree)
#     print("tree")
#     pprint(tree)
#     print("\nsizes")
#     pprint(sizes)

    ans1 = part1(sizes)
    print(f"Part 1: {ans1}")

    fs_size = 70_000_000
    target_size = 30_000_000

    mindir, sz = part2(sizes, fs_size, target_size)

    print(f"Part 2: {mindir} = {sz}")

if __name__ == '__main__':
    main()
