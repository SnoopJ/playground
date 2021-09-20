import click
from click.testing import CliRunner

@click.command()
@click.argument('x', type=int)
def main(x):
    """ A program to put the lime in the coconut """
    res = x+1
    print(f"{res=}")
    return res

if __name__ == '__main__':
    runner = CliRunner()
    result = runner.invoke(main, ['42'])
    print(f"{result.return_value=}")
