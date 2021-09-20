import errno
import inspect
import logging
import mmap
import os
import sys
import typing as t

from ctypes import CDLL, c_void_p, c_int, get_errno
from ctypes.util import find_library
from enum import IntEnum
from pathlib import Path

import attr


logger = logging.getLogger(__name__)

_madv_vals = {name: val for name, val in inspect.getmembers(mmap) if name.startswith("MADV_")}
EMADVAdvice = IntEnum("EMADVAdvice", _madv_vals)  # type:ignore
EMADVAdvice.__doc__ = """Enumeration of `advice` parameters for `madvise()` (see `man 2 madvise`)"""

_libc = CDLL(find_library('c'), use_errno=True)
_libc.madvise.argtypes = c_void_p, c_int, c_int
_libc.madvise.restype = c_int

def madvise(start: int, size: int, advice: EMADVAdvice, comment: str="", allow_unmapped: bool=False):
    if size < 0:
        raise ValueError("Mapping cannot have negative size (got: {size}")

    end = start + size
    logger.debug("Calling madvise(..., MADV_DONTDUMP) for range %x-%x %s", start, end, comment)
    err = _libc.madvise(start, size, advice)
    if err != 0:
        errcode = get_errno()
        errname = errno.errorcode.get(errcode, "<unknown>")
        # for madvise(), ENOMEM indicates the range is unmapped or outside this process's address space
        if allow_unmapped and errcode == errno.ENOMEM:
            logger.debug("madvise(): range %x-%x is not mapped (swallowing error)", start, end)
        else:
            raise OSError(f"madvise() returned error {errname} ({errcode})")


def _dontdump(prefixes: t.Sequence[str]) -> None:
    for mp in _mmaps():
        deny = any(mp.objfile.startswith(pre) for pre in prefixes)
        if mp.offset != 0:
            continue
        if deny:
            try:
                madvise(mp.start, mp.nbytes, EMADVAdvice.MADV_DONTDUMP, comment=f"for {mp.objfile}", allow_unmapped=True)  # type: ignore
            except OSError as exc:
                logger.exception("madvise() failed")


def _hex2int(val: str) -> int:
    return int(val, base=16)


@attr.s(auto_attribs=True, kw_only=True)
class MemMapping:
    """
    A memory mapping, as found in `/proc/<PID>/maps` on POSIX systems
    """

    perms: str
    dev: str
    inode: int = attr.ib(converter=int)
    offset: int = attr.ib(converter=_hex2int)
    start: int = attr.ib(converter=_hex2int)
    stop: int = attr.ib(converter=_hex2int)
    pathname: t.Optional[str] = None
    src: t.Optional[str] = None

    @classmethod
    def parse(cls, src: str):
        fields = src.split()

        addr, perms, offset, dev, inode, *rest = fields
        if len(rest) == 0:
            # anonymous mapping (or *very* old Linux), no pathname
            pathname = None
        else:
            pathname = rest.pop(0)

        start, _, stop = addr.partition("-")
        return cls(start=start, stop=stop, perms=perms, offset=offset, dev=dev, inode=inode, pathname=pathname, src=src)

    @property
    def nbytes(self) -> int:
        return self.stop - self.start

    @property
    def objfile(self) -> str:
        if self.pathname is None:
            return "<anonymous>"
        return os.path.basename(self.pathname)


MAPPING_PREDICATE_T = t.Callable[[MemMapping], bool]

def _mmaps(
    pid: t.Optional[int] = None, predicate: t.Optional[MAPPING_PREDICATE_T] = None
) -> t.Generator[MemMapping, None, None]:
    """
    Get memory mappings for a process

    Parameters
    ----------
    pid : int, optional
        Process ID for which to retrieve mappings. If None, use current PID
        Note: the calling process must have `PTRACE_MODE_READ_FSCREDS`
        capability, see `man 5 proc` and `man 2 ptrace` for more information
    predicate: callable, optional
        Callable that accepts a `MemMapping` object and returns a bool
        indicating if that mapping should be included in the results

    Returns
    -------
    mappings : list[MemMapping]
        The memory mappings for the given process
    """
    if sys.platform != "linux":
        raise NotImplementedError("Only Linux is supported")

    if pid is None:
        pid = os.getpid()

    lines = Path(f"/proc/{pid}/maps").read_text().splitlines()
    for line in lines:
        mmap = MemMapping.parse(line)
        if predicate and not predicate(mmap):
            logger.debug("Excluding mapping %s (fails predicate)", mmap)
        else:  # (not predicate) or (not predicate(mmap))
            yield mmap
