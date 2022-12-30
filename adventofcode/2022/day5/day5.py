from copy import deepcopy
import re
from typing import Iterable

import click


Column = list[str]  # list order is bottom -> top
Count = From = To = int
Move = tuple[Count, From, To]


def print_drawing(drawing):
    for num, col in enumerate(drawing, 1):
        coltxt = ' '.join(f"[{c}]" for c in col)
        print(f"#{num}: {coltxt}")


def parse_drawing(drawing_lines: list[str]) -> list[Column]:
    # flip the drawing so we can build from the bottom-up
    drawing_lines.reverse()

#     print("Raw reversed drawing:")
#     print(*drawing_lines, end='', sep='')

    ncols = [int(val) for val in drawing_lines[0].split()][-1]

    # initialize an empty drawing
    drawing = [[] for _ in range(ncols)]

    # NOTE: original pattern was r"(\[[A-Z]\]|   )" which led to an interesting
    # off-by-one edge case whenever there were three-or-more adjacent empty spots
    COLS_PATT = r"(\[[A-Z]\](\s)|   \s)"
    for rowidx, line in enumerate(drawing_lines[1:]):
        for colidx, m in enumerate(re.finditer(COLS_PATT, line)):
            col = m[0].strip()
            if col:
                col = col[1]
#                 print(f"Pushing {col} to column #{idx+1}")
                drawing[colidx].append(col)


    return drawing


def parse_moves(move_lines: Iterable[str]) -> list[Move]:
    MOVE_PATT = r"move (?P<target>\d+) from (?P<from>\d+) to (?P<to>\d+)"

    moves = []

    for line in move_lines:
        m = re.match(MOVE_PATT, line)
        assert m
        count, from_, to = [int(val) for val in m.groups(["target", "from", "to"])]
        move = (count, from_, to)
        moves.append(move)

    return moves


def parse(lines: Iterable[str]) -> tuple[list[Column], list[Move]]:
    it = iter(lines)

    drawing_lines = []

    for line in it:
        if line.strip() == "":
            # empty line indicates the end of the drawing and beginning of the moves
            break
        drawing_lines.append(line)

    # remaining lines are moves
    move_lines = list(it)

    drawing = parse_drawing(drawing_lines)
    moves = parse_moves(move_lines)

    return drawing, moves


def part1(drawing, moves):
    # it's convenient to mutate the drawing in-place, so let's take a copy
    # (note: we need a 'deep' copy here since we have nested lists)
    drawing = deepcopy(drawing)

    for mov in moves:
        count, from_, to = mov
#         print(f"Moving {count} boxes from #{from_} to #{to}")
#         print("before:")
#         print_drawing(drawing)
        for _ in range(count):
            drawing[to - 1].append(drawing[from_ - 1].pop())

#         print("after:")
#         print_drawing(drawing)
#         print()

    return ''.join(col[-1] for col in drawing)


def part2(drawing, moves):
    # it's convenient to mutate the drawing in-place, so let's take a copy
    # (note: we need a 'deep' copy here since we have nested lists)
    drawing = deepcopy(drawing)

    for mov in moves:
        count, from_, to = mov
#         print(f"Moving {count} boxes from #{from_} to #{to}")
#         print("before:")
#         print_drawing(drawing)
        move_stack = []
        for _ in range(count):
            move_stack.append(drawing[from_ - 1].pop())

        # The CrateMover 9001 can preserve the original order
        move_stack.reverse()
        drawing[to - 1].extend(move_stack)

#         print("after:")
#         print_drawing(drawing)
#         print()

    return ''.join(col[-1] for col in drawing)


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        drawing, moves = parse(f)


#     print("initial drawing (rotated)")
#     print_drawing(drawing)
#     print()
#
#     print("moves:")
#     print(moves)
#     print()

    ans1 = part1(drawing, moves)
    print(f"Part 1: {ans1}")

    ans2 = part2(drawing, moves)
    print(f"Part 2: {ans2}")

if __name__ == '__main__':
    main()
