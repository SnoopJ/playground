"""
An ad-hoc tool to test which Unicode Standard Annex (UAX) #31 identifier category¹ each
codepoint in the UCS falls into

sample output (with optional dependency tqdm installed):
    $ python3.14 valid_identifiers.py --validate-against DerivedCoreProperties.txt
    3.14.0 (main, Oct  7 2025, 13:34:48) [GCC 12.3.0]
    unicodedata.unidata_version = '16.0.0'
    Scanning UCD: 100%|█████████████████████████████| 1114111/1114111 [00:14<00:00, 76547.31it/s]
    INVALID: 969589
    XID_START: 141246
    XID_CONTINUE: 3276

---
¹ https://unicode.org/reports/tr31/#Default_Identifier_Syntax
"""
import argparse
import logging
import sys
import unicodedata
from collections import defaultdict
from enum import StrEnum
from pathlib import Path
from typing import Iterator, List, Optional, Set, Tuple

LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Infer Python identifier rules")
parser.add_argument("--validate-against", type=Path, help="Path to DerivedCoreProperties.txt against which to validate the inferred rules. Any discrepances will be logged")
parser.add_argument("--verbose", action="store_true", help="Emit (lots of!) diagnostic information if set")


try:
    from tqdm import tqdm
except ImportError:
    LOGGER.warning("tqdm is not available, no progress bar will be available")
    def tqdm(it, *args, **kwargs):
        desc = kwargs.get("desc", None)
        if desc:
            print(desc)
        yield from it


class IdentifierType(StrEnum):
    INVALID = "INVALID"
    XID_START = "XID_Start"
    XID_CONTINUE = "XID_Continue"

    @classmethod
    def of(cls, value: str):
        if value.isspace() or value in ".,;#":
            # Special syntactical meaning, we already know these cannot be in identifiers
            return cls.INVALID

        if value == '_':
            # NOTE:to my knowledge, the one thing Python tweaks from the default ruleset is to
            # allow U+5F LOW LINE to start an identifier (it is XID_Continue by default)
            return cls.XID_CONTINUE

        XIDStart_src = f"{value} = 42  # if this compiles, c is a valid identifier (XID_Start)"
        XIDContinue_src = f"_{value} = -1  # if this compiles, c is a valid identifier (XID_Continue)"

        try:
            compile(XIDStart_src, "", "single")
            return cls.XID_START
        except (UnicodeEncodeError, SyntaxError):
            pass

        try:
            compile(XIDContinue_src, "", "single")
            return cls.XID_CONTINUE
        except (UnicodeEncodeError, SyntaxError):
            pass

        return cls.INVALID


# NOTE:2026-01-31:SnoopJ:adapted from CPython's `makeunicodedata.py`
class UcdFile:
    '''
    A file in the standard format of the UCD.

    See: https://www.unicode.org/reports/tr44/#Format_Conventions

    Note that, as described there, the Unihan data files have their
    own separate format.
    '''

    def __init__(self, fn) -> None:
        self.fn = fn

    def records(self) -> Iterator[List[str]]:
        LOGGER.info("Loading records from UCD file: %s", self.fn)
        with open(self.fn, 'r') as file:
            for line in file:
                line = line.split('#', 1)[0].strip()
                if not line:
                    continue
                yield [field.strip() for field in line.split(';')]

    def __iter__(self) -> Iterator[List[str]]:
        return self.records()

    def expanded(self) -> Iterator[Tuple[int, List[str]]]:
        for record in self.records():
            char_range, rest = record[0], record[1:]
            for char in self.expand_range(char_range):
                yield char, rest

    @staticmethod
    def expand_range(char_range: str) -> Iterator[int]:
        '''
        Parses ranges of code points, as described in UAX #44:
          https://www.unicode.org/reports/tr44/#Code_Point_Ranges
        '''
        if '..' in char_range:
            first, last = [int(c, 16) for c in char_range.split('..')]
        else:
            first = last = int(char_range, 16)
        for char in range(first, last+1):
            yield char


def uax31_classes(core_props_file: Path) -> list[IdentifierType]:
    core_props = UcdFile(core_props_file)
    result = [IdentifierType.INVALID] * (sys.maxunicode+1)

    for num, *props in core_props.expanded():
        uid = f"U+{hex(num)[2:]}"

        if not props:
            raise ValueError(f"Codepoint with no properties, invalid data? {uid}")

        typ = props[0][0]
        if not typ.startswith("XID_"):
            continue

        if result[num] == IdentifierType.XID_START:
            # XID_Continue is a superset of XID_Start, so don't downgrade such a codepoint
            LOGGER.debug("Codepoint already marked as XID_START, moving on: %s", uid)
            continue

        result[num] = IdentifierType[typ.upper()]

    return result


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        loglvl = logging.DEBUG
    else:
        loglvl = logging.WARNING

    logging.basicConfig(level=loglvl)

    print(sys.version)
    print(f"{unicodedata.unidata_version = }")

    if args.validate_against:
        typs = uax31_classes(args.validate_against)

    results = []
    for n in tqdm(range(1, sys.maxunicode+1), desc="Scanning UCD"):
        c = chr(n)
        uid = f"U+{hex(n)[2:]}"

        typ = IdentifierType.of(c)
        results.append(typ)

        if args.validate_against:
            expected_typ = typs[n]
            LOGGER.debug("%s (%r) %s %s", uid, c, typ, expected_typ)
            if expected_typ is not None and expected_typ != typ:
                LOGGER.warning(f"!! Type mismatch: %s %r has observed type %s and UCD type %s", uid, c, typ, expected_typ)

    for T in IdentifierType:
        cnt = sum(typ == T for typ in results)
        print(f"{T.name}: {cnt}")
