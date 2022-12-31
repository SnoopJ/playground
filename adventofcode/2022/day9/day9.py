import click

# NOTE: I assume with these imports that we are running day9.py from the same dir as pair.py
from grid import Grid
from pair import Pair
from rope import Rope


def parse_moves(lines):
    moves = []
    for line in lines:
        dir, dist = line.strip().split()
        dist = int(dist)
        moves.append((dir, dist))

    return moves


def part1(moves, debug: bool = False) -> int:
    rope = Rope(N_knots=2)

    grid = Grid.from_moves(moves)

    if debug:
        print("=== Initial State ===\n")
        grid.print(rope)
        print()


    visited = set()
    for (dir,dist) in moves:
        if debug:
            print(f"=== {dir} {dist} ===\n")

        dx, dy = Grid.DELTAS[dir]
        for _ in range(dist):
            rope.move_head((dx, dy))

            if debug:
                grid.print(rope)
                print()

            visited.add(tuple(rope.tail))

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
