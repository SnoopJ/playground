from pathlib import Path


def anchored_path_prefix(a: Path, b: Path) -> Path:
    """Given two Paths, find the part of one that is a non-overlapping prefix for the other"""
    if a == b:
        raise ValueError("Paths are equal")
    elif a.is_absolute() and b.is_absolute():
        raise ValueError("At least one of the input paths must be relative")
    lng, shrt = (b.parts, a.parts)
    if len(lng) < len(shrt):
        # oops, wrong order
        lng, shrt = shrt, lng

    # walk the "shorter" path
    for numstep, prt in enumerate(shrt[::-1], 1):
        if lng[-numstep] != prt:  # NOTE: this is a string comparison, I'm not thinking about stuff like a/b/../c or a/b/./c here
            raise ValueError(f"{shrt} is not a subsequence of {lng}")

    # whatever we left the loop with, omit that many parts of the longer path
    return Path(*lng[:-numstep])


if __name__ == "__main__":
    pth1 = Path("taco/cat")
    pth2 = Path("/foo/bar/baz/taco/cat")

    prefix = anchored_path_prefix(pth1, pth2)
    print(f"{pth1=}")
    print(f"{pth2=}")
    print(f"{prefix=}")
