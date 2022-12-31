import click

# NOTE: I assume with these imports that we are running day9.py from the same dir as pair.py
from grid import Grid
from pair import Pair


def parse_moves(lines):
    moves = []
    for line in lines:
        dir, dist = line.strip().split()
        dist = int(dist)
        moves.append((dir, dist))

    return moves


def part1(moves, debug: bool = False) -> int:
    head = Pair(0, 0)
    tail = Pair(0, 0)

    grid = Grid.from_moves(moves)

    if debug:
        print("=== Initial State ===\n")
        grid.print(head, tail)
        print()


    visited = set()
    for (dir,dist) in moves:
        if debug:
            print(f"=== {dir} {dist} ===\n")
        dx, dy = Grid.DELTAS[dir]
        for _ in range(dist):
            head += (dx, dy)
            tail = tail.move_towards(head)
            hx, hy = head
            tx, ty = tail
            ddx, ddy = head - tail
            ddx = abs(ddx)
            ddy = abs(ddy)

            if debug:
                grid.print(head, tail)
                print()

            assert ((ddx == 0 and ddy == 0) or
                    (ddx == 1 and ddy == 0) or
                    (ddx == 0 and ddy == 1) or
                    (ddx == 1 and ddy == 1)), f"Tail appears to be too far away from head ({ddx=}, {ddy=})"
            visited.add(tuple(tail))

    grid.print_visited(visited)
    print()

    return len(visited)


def part2():
    pass


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    with open(input, "r") as f:
        moves = parse_moves(f)


    ans1 = part1(moves, debug=debug)
    print(f"Part 1: {ans1} points visited")

    # ans2 = part2()
    # print(f"Part 2: {ans2}")

if __name__ == '__main__':
    main()
