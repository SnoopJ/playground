from __future__ import annotations
import random
from pathlib import Path


random.seed(42)


HERE = Path(__file__).parent
TREE_ROOT = HERE.joinpath("tree")
TREE_ROOT.mkdir()

FILE_EXT = ".txt"
PROB_CHILD_DIR = 0.5


def make_path_tree():
    pending: list[Path] = [TREE_ROOT]

    while pending:
        nxt = pending.pop()
        nchildren = 1 + random.randint(0, 3)

        for n in range(nchildren):
            depth = len(nxt.relative_to(TREE_ROOT).parts)
            name = f"d{depth}c{n}"
            child = nxt.joinpath(name)

            if random.random() < PROB_CHILD_DIR:
                print(f"Creating dir:  {child!s}")
                child.mkdir()
                pending.append(child)
            else:
                print(f"Creating file: {child!s}{FILE_EXT}")
                child.with_name(child.name + FILE_EXT).touch()


if __name__ == "__main__":
    make_path_tree()
