import click

# NOTE: I assume with these imports that we are running day10.py from the same dir as cpu.py
from cpu import CPU, INSTRUCTIONS, ExecutionHalted


def parse_instructions(lines):
    instructions = []
    for line in lines:
        instr_name, *args = line.split()
        args = [int(a) for a in args]
        instr = INSTRUCTIONS[instr_name](*args)
        instructions.append(instr)

    return instructions


def part1(instructions, debug: bool = False) -> int:
    cpu = CPU(debug=debug)
    cpu.load(instructions)

    values = []
    while True:
        try:
            cpu.step()
            if (20 + cpu.cycles) % 40 == 0:
                if debug:
                    print(f"Cycle #{cpu.cycles}, {cpu.X=} {cpu.signal_strength=}")
                values.append(cpu.signal_strength)
        except ExecutionHalted:
            break

    return sum(values)


def part2(instructions, debug: bool = False) -> None:
    cpu = CPU(debug=debug)
    cpu.load(instructions)

    values = []
    while True:
        try:
            if debug:
                cpu.draw_sprite()
                cpu.draw_display()

            cpu.step()
            if (20 + cpu.cycles) % 40 == 0:
                values.append(cpu.signal_strength)

        except ExecutionHalted:
            break

    return cpu


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    with open(input, "r") as f:
        instructions = parse_instructions(f)

    ans1 = part1(instructions, debug=debug)
    print(f"Part 1: {ans1}")

    print("Part 2:")
    cpu = part2(instructions, debug=debug)
    cpu.draw_display()
    # NOTE: I believe my output has an 'extra' draw in it, the top-left pixel
    # is darkened but probably shouldn't be. Good enough to get the star, though!
    #
    #  .###.#..#...##.####.###....##.####.####.
    #  ...#.#.#.....#.#....#..#....#.#.......#.
    #  ..#..##......#.###..###.....#.###....#..
    #  .#...#.#.....#.#....#..#....#.#.....#...
    #  #....#.#..#..#.#....#..#.#..#.#....#....
    #  ####.#..#..##..#....###...##..#....####.


if __name__ == '__main__':
    main()
