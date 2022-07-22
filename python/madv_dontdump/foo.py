import ctypes
from pathlib import Path

from repro import dump, fork_and_abort, _madv_dontdump

import numpy as np

# libfoo = ctypes.CDLL(Path('libfoo.so').resolve())
# libfoo.randvec.argtypes = (ctypes.c_int,)
# libfoo.randvec.restypes = (ctypes.c_void_p,)

if __name__ == "__main__":
    from resource import setrlimit, RLIMIT_CORE, RLIM_INFINITY
    # set nonzero core limit so a core dump is produced on abort
    setrlimit(RLIMIT_CORE, (RLIM_INFINITY, RLIM_INFINITY))

#     result = libfoo.randvec(1_000_000)
#     print(hex(result))
    result = np.arange(1_000_000)

    dump("foo1", outdir="foo/")

#     result = libfoo.randvec(10_000_000)
#     print(hex(result))
    result = np.arange(10_000_000)

    dump("foo2", outdir="foo/")

    _madv_dontdump(["libfoo"])

    dump("foo3", outdir="foo/")

    del result
    import gc; gc.collect()

    dump("foo4", outdir="foo/")
