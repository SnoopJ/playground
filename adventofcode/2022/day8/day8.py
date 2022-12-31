from pprint import pprint

import click



Grid = list[list[int]]

def vizgrid(grid: Grid) -> Grid:
    """Map the input grid to a visibility grid"""
    H = len(grid)
    W = len(grid[0])

    # assume everything is not-visible to begin with
    viz = [[0]*W for _ in range(H)]

    for rowidx, row in enumerate(grid):
        for colidx, val in enumerate(row):

            # if we're on an edge, this entry is visible…
            if (rowidx in (0, W-1)) or (colidx in (0, H-1)):
                viz[rowidx][colidx] = 1
                continue

            # …otherwise, test visibility to each edge…
            # NOTE: this probably does more work than it needs to because these
            # 'rays' have a lot of overlap. 'marching' a ray front in from the
            # edges would likely duplicate less work
            lefts = [grid[rowidx][c] for c in range(colidx)]
            rights = [grid[rowidx][c] for c in range(colidx + 1, W)]
            ups = [grid[r][colidx] for r in range(rowidx)]
            downs = [grid[r][colidx] for r in range(rowidx + 1, H)]

            for testvals in [lefts, rights, ups, downs]:
                if all(tv < val for tv in testvals):
                    viz[rowidx][colidx] = 1

    return viz


def part1(viz: Grid) -> int:
    num_visible = sum(sum(row) for row in viz)
    return num_visible


def part2():
    pass


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        grid = [[int(c) for c in line.strip()] for line in f]

    viz = vizgrid(grid)

    ans1 = part1(viz)
    print(f"Part 1: {ans1}")

    # ans2 = part2()
    # print(f"Part 2: {ans2}")

if __name__ == '__main__':
    main()
