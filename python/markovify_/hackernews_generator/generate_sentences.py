import json
import textwrap

import click
import markovify


@click.command()
@click.argument("modelfile")
@click.option("-n", "--num", type=int, default=5)
@click.option("--width", type=int, default=80)
def main(modelfile, num, width):
    """Generate sentences using Markov chains built from HackerNews scrapings"""
    with open(modelfile, "r") as f:
        model = markovify.Chain.from_json(f.read())

    for n in range(num):
        msg = " ".join(model.gen())
        lines = textwrap.wrap(msg, width=width)
        print(*lines, '---', sep="\n")


if __name__ == '__main__':
    main()
