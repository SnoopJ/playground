import argparse
import logging
import sys
import unicodedata
from collections import defaultdict
from enum import StrEnum

LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Infer Python identifier rules")
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

# sample output:
# $ python3.13 valid_identifiers.py
# 3.13.0 (main, Oct  7 2024, 18:29:55) [GCC 11.4.0]
# unicodedata.unidata_version = '15.1.0'
# Scanning UCD: 100%|███████████████████| 1114111/1114111 [00:32<00:00, 34265.67it/s]
# INVALID: 974017
# XID_START: 136945
# XID_CONTINUE: 3149


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


if __name__ == "__main__":
    args = parser.parse_args()
    if args.verbose:
        loglvl = logging.DEBUG
    else:
        loglvl = logging.WARNING

    logging.basicConfig(level=loglvl)

    print(sys.version)
    print(f"{unicodedata.unidata_version = }")
    results = []
    for n in tqdm(range(1, sys.maxunicode+1), desc="Scanning UCD"):
        c = chr(n)

        typ = IdentifierType.of(c)
        results.append(typ)

    for T in IdentifierType:
        cnt = sum(typ == T for typ in results)
        print(f"{T.name}: {cnt}")
