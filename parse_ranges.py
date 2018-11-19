"""

"""
import itertools
import re
from pprint import pprint

# pat = "192.168.[0-2].[0-3]:*"
pat = "192.*.2.[0-5]"


def _parsegroup(part):
    """ turn a re.Group """
    print(part, part.groups())
    if part.group(1) == "*":
        res = range(0, 255)
    elif part.group(1) is not None:
        lower = int(part.group(1))
        upper = int(part.group(2)) + 1
        res = range(lower, upper)
    else:
        res = [part.group()]

    return res


RANGE_PATTERN = r"\*|\[(\d+)-(\d+)\]|[^[*]+"

prod_args = [_parsegroup(part) for part in re.finditer(RANGE_PATTERN, pat)]

addrs = ["".join(map(str, out)) for out in itertools.product(*prod_args)]

pprint(addrs)
