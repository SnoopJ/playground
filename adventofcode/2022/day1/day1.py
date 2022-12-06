import click


def elves(lines):
    accum = []
    for line in lines:
        if not line.strip():
            yield accum
            accum = []
        else:
            cals = int(line)
            accum.append(cals)

    if accum:
        yield accum


@click.command()
@click.option('--input', required=True, help="Input file for this day")
def main(input):
    with open(input, "r") as f:
        food_by_elf = list(elves(f))

    cals_by_elf = sorted((sum(elf_food) for elf_food in food_by_elf), reverse=True)

    part1 = cals_by_elf[0]
    print(f"Part 1: {part1}")

    part2 = sum(cals_by_elf[:3])
    print(f"Part 2: {part2}")


if __name__ == '__main__':
    main()
