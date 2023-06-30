"""
This program shows how to generate a list of exclusions for `auditwheel repair`
so that only specifically included libraries are vendored into the resulting
wheel.

This is necessary because an `--include` option was explicitly rejected
upstream: https://github.com/pypa/auditwheel/pull/310#issuecomment-849773358
"""
from __future__ import annotations

import sys
from fnmatch import fnmatch
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from auditwheel.lddtree import lddtree


INCLUDED_LIBS = {
    "libgfortran*.so*",
}
print("included libs:")
print(INCLUDED_LIBS)

def _is_included(libname: str) -> bool:
    return any(fnmatch(libname, patt) for patt in INCLUDED_LIBS)


def _excluded_libs(wheel: Path) -> set[str]:
    """
    Get a list of libraries that should be excluded from `auditwheel repair` vendoring

    This looks at first-level dependencies of all `.so` files in the given wheel file,
    and removes any library that should be explicitly included (via `INCLUDED_LIBS`)
    """
    _tmpdir = TemporaryDirectory()
    tmpdir = Path(_tmpdir.name)

    needed_libs = set()

    with ZipFile(wheel, 'r') as zf:
        zf.extractall(tmpdir)
    for soname in tmpdir.glob("**/*.so"):
        needed_libs.update(lddtree(soname).get("needed", ()))

    print("all libs:")
    print(needed_libs)

    return {lib for lib in needed_libs if not _is_included(lib)}


if __name__ == "__main__":
    excludes = _excluded_libs(Path(sys.argv[1]))
    print("excluded libs:")
    print(excludes)


# --- EXAMPLE OUTPUT ---
# $ python3 auditwheel_exclude.py numpy-1.24.4-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# included libs:
# {'libgfortran*.so*'}
# all libs:
# {'libpthread.so.0', 'libc.so.6', 'ld-linux-x86-64.so.2', 'libm.so.6', 'libgfortran-040039e1.so.5.0.0', 'libopenblas64_p-r0-15028c96.3.21.so'}
# excluded libs:
# {'libpthread.so.0', 'libc.so.6', 'libm.so.6', 'ld-linux-x86-64.so.2', 'libopenblas64_p-r0-15028c96.3.21.so'}
