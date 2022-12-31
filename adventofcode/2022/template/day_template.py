import click


def part1(debug: bool = False):
    pass


def part2(debug: bool = False):
    pass


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    with open(input, "r") as f:
        lines = [line.strip() for line in f]

    # ans1 = part1(debug=debug)
    # print(f"Part 1: {ans1}")

    # ans2 = part2(debug=debug)
    # print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
