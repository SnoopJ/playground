"""
Based on a question in #python on Libera.chat on 8 April 2022,
about pattern-matching a string with patterns like "XYX" for "foobarfoo"
"""
import re
from pprint import pprint


def _build_regex(pattern: str):
    seen = []
    for c in pattern:
        if c in seen:
            idx = seen.index(c) + 1
            # yield a reference to the appropriate capture group
            yield rf"(?P={c})"
        else:
            seen.append(c)
            # yield a new capture group
            yield rf"(?P<{c}>.+)"


def pattern_to_regex(pattern: str) -> str:
    return "".join(_build_regex(pattern))


if __name__ == "__main__":
    patterns = ["XYX", "ABA", "XXX"]
    strings = ["abracadabra", "address", "hashembardemhashem", "hellohellohello", "it can work with (.*) even if the test string is quite complicated, showing it can work"]
    regexes = [pattern_to_regex(pattern) for pattern in patterns]
    for pattern, regex in zip(patterns, regexes):
        print(f"{pattern=!r} generated regex {regex!r}")

    for test_string in strings:
        print(f"{test_string=!r}")
        for pattern in patterns:
            regex = pattern_to_regex(pattern)
            m = re.search(regex, test_string)
            if m:
                print(f"Matched {pattern=!r}:")
                for k,v in m.groupdict().items():
                    print(f"\t{k}={v!r}")
            else:
                print(f"No match for {pattern=!r}")
        # empty line to separate each input string
        print()
