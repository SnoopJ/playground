from __future__ import annotations
import sys
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).parent
BUNDLE_ROOT = HERE.joinpath("tree")


def _gather_tree(root: Path, bundle_root: Path, depth: int = 0) -> Iterable[str]:
    EXCLUDED_FILENAMES = ("not relevant to this example",)
    INDENT = 4*" " * depth

    for pth in root.iterdir():
        if pth.is_dir():
            yield f'{INDENT}<Directory Name="{pth.name}">'
            # descend
            yield from _gather_tree(pth, bundle_root=bundle_root, depth=depth+1)
            yield f'{INDENT}</Directory>'
            continue

        if pth.name in EXCLUDED_FILENAMES:
            continue

        # okay, this is a leaf, we generate <FILE> instead

        relpth = pth.relative_to(bundle_root)
        relpth_str = str(relpth).replace("/", "\\")
        tag = f'{INDENT}<File Source="!(bindpath.bundle_root)\{relpth_str}" />'

        yield tag


if __name__ == "__main__":
    if not BUNDLE_ROOT.exists():
        print("Run make_path_tree.py first")
        sys.exit(1)

    print("Traversing tree/")


    print("<!-- BEGIN generated XML -->")
    for line in _gather_tree(root=BUNDLE_ROOT, bundle_root=BUNDLE_ROOT):
        print(line)
    print("<!-- END generated XML -->")
