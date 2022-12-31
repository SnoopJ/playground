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


def vizscore(grid: Grid, row: int, col: int) -> int:
    H = len(grid)
    W = len(grid[0])

    # edges score 0 by definition
    if row in (0, W-1) or col in (0, H-1):
        return 0

    val = grid[row][col]
    leftscore = rightscore = upscore = downscore = 0

    for r in range(row-1, -1, -1):
        leftscore += 1
        if grid[r][col] >= val:
            break

    for r in range(row+1, W):
        rightscore += 1
        if grid[r][col] >= val:
            break

    for c in range(col-1, -1, -1):
        upscore += 1
        if grid[row][c] >= val:
            break

    for c in range(col+1, H):
        downscore += 1
        if grid[row][c] >= val:
            break

    score = leftscore * rightscore * upscore * downscore

    return score


def part1(viz: Grid) -> int:
    num_visible = sum(sum(row) for row in viz)
    return num_visible


def part2(grid: Grid) -> int:
    H = len(grid)
    W = len(grid[0])

    maxscore = 0
    winner = None

    for rowidx, row in enumerate(grid):
        for colidx, val in enumerate(row):
            score = vizscore(grid, rowidx, colidx)
#             print(f"({rowidx}, {colidx}), {val}: {score=}")

            if score > maxscore:
                winner = (rowidx, colidx)
                maxscore = score

    return maxscore


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        grid = [[int(c) for c in line.strip()] for line in f]

    viz = vizgrid(grid)

    ans1 = part1(viz)
    print(f"Part 1: {ans1}")

    ans2 = part2(grid)
    print(f"Part 2: {ans2}")

if __name__ == '__main__':
    main()
