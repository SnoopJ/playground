"""
A tiny program I wrote to find all the latin mathematical double-struck
codepoints in the UCS and produce XCompose rules for typing them

find_chars() could be repurposed to searching for other fragments
"""
import sys
import unicodedata
from itertools import chain


def find_chars(*parts):
    for n in range(sys.maxunicode+1):
        char = chr(n)
        try:
            name = unicodedata.name(char)
        except ValueError:
            continue

        if any(part.casefold() not in name.casefold() for part in parts):
            continue

        yield char


if __name__ == "__main__":
    for char in chain(find_chars("double-struck", "capital"), find_chars("double-struck", "small")):
        name = unicodedata.name(char)
        n = ord(char)
        normed = unicodedata.normalize('NFKC', char)
        hexcode = f"U{hex(n).upper()[2:]}"

        xcompose_rule = f"<Multi_key> <d> <s> <{normed}> : \"{char}\" {hexcode}  # {name}"
        print(xcompose_rule)
