import ctypes
from pathlib import Path

from repro import dump, fork_and_abort

libfoo = ctypes.CDLL(Path('libfoo.so').resolve())
libfoo.randvec.argtypes = (ctypes.c_int,)
libfoo.randvec.restypes = (ctypes.c_void_p,)

if __name__ == "__main__":
    result = libfoo.randvec(1_000_000)
    print(hex(result))

    fork_and_abort()

    result = libfoo.randvec(10_000_000)
    print(hex(result))

    fork_and_abort()
