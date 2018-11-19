from itertools import zip_longest
from enum import Enum


class Case(Enum):
    UPPER = 1
    LOWER = 2
    NONE = -1


def _case(c):
    """ Test the case of the char """
    if c.isupper():
        return Case.UPPER
    elif c.islower():
        return Case.LOWER
    else:
        return Case.NONE


def camelsplit(s):
    """
    Split a string s into its camelCase atoms.

    e.g. 'camelCaseString' -> ['camel', 'Case', 'String']
    """
    leftidx = 0
    for idx, (cur, prev) in enumerate(zip_longest(s[1:], s), 1):
        # cur will be None when we're done with the string, so we should just
        # yield whatever's left
        if cur is None or (_case(cur) is Case.UPPER and _case(cur) != _case(prev)):
            yield s[leftidx:idx]
            leftidx = idx


strings = [
    "camelCaseString",
    "notcasedstring",
    "UPPERSTRING",
    "MOSTLYUPPERString",
    "MOSTLYUPPERStringWithCamel",
    "PascalCaseString",
]

wpad = max(len(s) for s in strings)

for s in strings:
    print(f"{s:>{wpad}} → {list(camelsplit(s))}")
