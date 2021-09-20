"""
Implementation of ternary logic with click.
"""
import click

@click.command()
@click.option('--foo/--no-foo', default=None)
def main(foo):
    print(foo)

if __name__ == '__main__':
    main()
