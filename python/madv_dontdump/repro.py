import os
from pathlib import Path
import shutil
import subprocess
from resource import setrlimit, RLIMIT_CORE, RLIM_INFINITY
import typing as t

from _madvise import madvise, _madv_dontdump

def fork_and_abort():
    pid = os.fork()
    if pid == 0:
        # child process calls abort(), creating a core dump (if enabled)
        os.abort()
    else:
        # parent process
        os.waitpid(pid, 0)


def _mappings(corefn: str) -> str:
    return subprocess.check_output(['/usr/bin/gdb', '--batch', '-q', '--eval-command', 'info proc mappings', '--core', corefn], text=True)


def save_mappings(corefn: str, outdir: t.Optional[Path]=None):
    if outdir is None:
        outdir = Path()

    pid = os.getpid()
    corepth = Path(corefn)

    mapspth = Path(outdir, f"{corepth.stem}_mappings.txt")
    shutil.copy(f"/proc/{pid}/maps", mapspth)
    print(f"Memory maps for {corefn} saved to {mapspth}")

    smapspth = Path(outdir, f"{corepth.stem}_smaps.txt")
    shutil.copy(f"/proc/{pid}/smaps", smapspth)
    print(f"Memory map details (/proc/{pid}/smaps) saved to {smapspth}")


def dump(outfn: str, outdir: t.Optional[Path]=None):
    if outdir is None:
        outdir = Path()
    fork_and_abort()
    opth = Path(outdir, outfn)
    shutil.move("core", opth)
    szMB = os.stat(opth).st_size /1_000_000
    print(f"Dumped core to {opth} (size: {szMB:.1f} MB)")
    save_mappings(outfn, outdir=outdir)


if __name__ == "__main__":
    # set nonzero core limit so a core dump is produced on abort
    setrlimit(RLIMIT_CORE, (RLIM_INFINITY, RLIM_INFINITY))

    outpth = Path("output")
    if not outpth.exists():
        outpth.mkdir()

    print("--- First dump: baseline")
    dump("core1", outdir=outpth)
    print("---")

    print("calling libfoo")
    # allocate and populate a bunch of memory with libfoo
    import ctypes
    libfoo = ctypes.CDLL(Path('libfoo.so').resolve())
    libfoo.randvec.restypes = (ctypes.c_void_p,)
    result = libfoo.randvec(1_000_000)
    print(hex(result))

    print("--- Second dump: baseline with libfoo")
    dump("core2", outdir=outpth)
    print("---")
    # set MADV_DONTDUMP for memory mapped by the named libraries
    # scans /proc/<pid>/maps, identifies zero-offset maps with these prefixex, calls madvise()
    # this *should* exclude the relevant libraries from produced core dumps...
    _madv_dontdump(["libfoo"])

    # ... but it doesn't seem to
    print("--- Third dump: MADV_DONTDUMP")
    dump("core3", outdir=outpth)
    print("---")

    # nuclear option: tell the kernel to produce a core file NO LARGER than 100 MB...
    setrlimit(RLIMIT_CORE, (100_000_000, 100_000_000))

    # ...which does work, sorta.
    print("Fourth dump: MADV_DONTDUMP and RLIMIT_CORE=100 MB")
    dump("core4", outdir=outpth)
    print("---")
