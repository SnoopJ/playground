import sys
import unicodedata
from collections import defaultdict
from enum import IntEnum

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it, *args, **kwargs):
        yield from it

# sample output:
# $ python3.13 valid_identifiers.py
# 3.13.0 (main, Oct  7 2024, 18:29:55) [GCC 11.4.0]
# unicodedata.unidata_version = '15.1.0'
# Scanning UCD: 100%|███████████████████| 1114111/1114111 [00:32<00:00, 34265.67it/s]
# INVALID: 974017
# XID_START: 136945
# XID_CONTINUE: 3149


class IdentifierType(IntEnum):
    INVALID = 0
    XID_START = 1
    XID_CONTINUE = 2

    @classmethod
    def of(cls, value: str):
        if value.isspace() or value in ".,;#":
            return cls.INVALID

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
