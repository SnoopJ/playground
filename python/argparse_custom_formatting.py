"""
Based on a question in freenode #python on Jan 14, 2019 about how to eliminate 
the [ ...] hinting for commandline options when using argparse. This is a 
really bad idea, but I was curious about how to go about it. Subclassing the
provided `HelpFormatter` and overriding `_format_args()` turns out to be 
sufficient.
"""

import argparse


class MyFormatter(argparse.HelpFormatter):
    def _format_args(self, action, default_metavar):
        return ""


parser = argparse.ArgumentParser(
    description="A useful description of this script (might want to set this to __doc__)",
    formatter_class=MyFormatter,
)
parser.add_argument(
    "-x",
    metavar="nameofx",
    nargs="+",
    type=float,
    default=32 * 32 * 32,
    help="Helpful message about this argument",
)

grp = parser.add_mutually_exclusive_group()
grp.add_argument(
    "--option1", dest="destination", action="store_const", const="option1_const"
)
grp.add_argument(
    "--option2", dest="destination", action="store_const", const="option2_const"
)

args = parser.parse_args()
