import argparse

from . import main


parser = argparse.ArgumentParser(
    description="A useful description of this script", formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument("--delay", action="store_true")
args = parser.parse_args()


main(args.delay)
