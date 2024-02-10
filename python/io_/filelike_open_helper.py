from __future__ import annotations

import random
from contextlib import contextmanager
from io import StringIO, IOBase
from pathlib import Path


@contextmanager
def ensure_filelike(obj: str | IOBase, mode):
    """A helper like open() that supports StringIO and BytesIO"""
    if isinstance(obj, IOBase):
        # TODO: this should probably at least check that the mode makes sense
        # we already have a file-like object, no-op
        yield obj
        # no need to close
    else:
        with open(obj, mode) as f:
            yield f
        # file is closed


if __name__ == "__main__":
    bufs = [StringIO() for _ in range(5)]
    fns = [f"{n}.txt" for n in range(5)]
    targets = [*bufs, *fns]
    random.shuffle(targets)

    for idx, obj in enumerate(targets):
        with ensure_filelike(obj, "w") as f:
            f.write(f"test string {idx}")

    print("buffers: ", [b.getvalue() for b in bufs])
    print("files: ", [Path(fn).read_text() for fn in fns])
