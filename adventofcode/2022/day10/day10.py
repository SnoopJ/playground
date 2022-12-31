import click

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
                print(f"Cycle #{cpu.cycles}, {cpu.X=} {cpu.signal_strength=}")
                values.append(cpu.signal_strength)
        except ExecutionHalted:
            break

    return sum(values)


def part2(debug: bool = False):
    pass


@click.command()
@click.option('--input', required=True, help="Input file for this day")
@click.option('--debug', is_flag=True, default=False, help="Enable debug output")
def main(input, debug):
    with open(input, "r") as f:
        instructions = parse_instructions(f)

    ans1 = part1(instructions, debug=debug)
    print(f"Part 1: {ans1}")

    # ans2 = part2(debug=debug)
    # print(f"Part 2: {ans2}")


if __name__ == '__main__':
    main()
