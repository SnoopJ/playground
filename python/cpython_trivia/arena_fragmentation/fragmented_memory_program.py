"""
This sample shows off the memory consumption of CPython's internal memory
allocator in the "typical" case where the layout of objects in memory becomes
fragmented as objects pass into and out of existence.

The punchline: CPython can use more memory than your napkin math would suggest,
depending on the order of creation/destruction of the objects in your program

=== Background ===

CPython allocator crash course: the backing memory for most objects lives in
256 KB chunks ("arenas") requested from the OS (i.e. with malloc()), and
objects are internally allocated into this memory held by the runtime. [1]

This allocation strategy prevents repeated calls to ``malloc(), free()`` as
objects come into and out of existence throughout the program, but comes with
the quirk that an arena **will not be freed** unless it is entirely empty [2]

=== This program ===

This program first creates a bunch of lists that should each consume
approximately half of an arena, giving us memory utilization like what's shown
in the diagram below. [3]

                      (N)                                (N+1)
        +------------------------------+    +------------------------------+
        |                              |    |                              |
... --->|         256 KB arena         |--->|         256 KB arena         |---> ...
        |                              |    |                              |
        +------------------------------+    +------------------------------+
               |                |                  |                |
               |                |                  |                |
         +-----V-----+    +-----V-----+      +-----V-----+    +-----V-----+
         |           |    |           |      |           |    |           |
         | list[int] |    | list[int] |      | list[int] |    | list[int] |
         |           |    |           |      |           |    |           |
         +-----------+    +-----------+      +-----------+    +-----------+


THEN, the program randomly selects 25% of these lists and drops them, which
triggers garbage collection of those lists and frees up memory in the
underlying arenas. At the end of this process, *some* of the arenas will
be completely empty (and can be freed), but some will still contain living
objects. In the following diagram, arena ``N+1`` can be freed and those 256 KB
given back to the OS, but arena ``N`` has to hang around because it's still
providing storage for some objects.


                      (N)                                (N+1)
        +------------------------------+    +------------------------------+
        |                              |    |                              |
... --->|         256 KB arena         |--->|         256 KB arena         |---> ...
        |                              |    |                              |
        +------------------------------+    +------------------------------+
               |                |                  |                |
               |                |                  |                |
         +-----V-----+    +-----V-----+      +-----V-----+    +-----V-----+
         |           |    |           |      |           |    |           |
         | list[int] |    |           |      |           |    |           |
         |           |    |           |      |           |    |           |
         +-----------+    +-----------+      +-----------+    +-----------+


The output


=== Notes ===

[1] I am oversimplifying here, for more of the gory details, see the excellent
    talk that Larry Hastings gave at PyCon US 2012: https://youtu.be/XGF3Qu4dUqk?t=865

[2] Not counting arenas created by CPython for temporary purposes (i.e. when
    compiling code). The behavior of freeing an arena when it is entirely empty
    is documented here in the CPython source tree:
    https://github.com/python/cpython/blob/a1daf6e5ccd78e43ba1eb6fa8d0347e939ce8243/Objects/obmalloc.c#L2082-L2088

[3] Note that the ``list`` and ``int`` objects in this program have SEPARATE
    storage. The integer objects inside of a list and the list object itself
    may not even be stored in the same arena. This would be annoying to
    indicate on the diagrams, so I'm not doing that.
"""

import gc
import os
import random
import sys

from psutil import Process


KB = 1024
MB = 1024 * KB
ARENA_SIZE_BYTES = 256 * KB

# note: approximate, the size of an int varies based on the number of digits it has
INT_MINSIZE_BYTES = sys.getsizeof(100_000_000)
NUM_INT_ARENA = ARENA_SIZE_BYTES // INT_MINSIZE_BYTES

# approximation of the number of integers to consume about half of a CPython arena
NUM_INTS = NUM_INT_ARENA // 2
NUM_DUMMIES = 1000  # should be somewhere around 200 MB of memory

PROC = Process()
PID = PROC.pid


def _dummy_list(lo=1_000_000, hi=100_000_000):
    return [random.randint(lo, hi) for _ in range(NUM_INTS)]


def _dump_alloc_info(filename, do_print=True):
    with open(filename, "w") as f:
        oldstderr = os.dup(2)
        # replace stderr for a bit
        os.dup2(f.fileno(), 2)

        # NOTE: prints detailed allocation system info to stderr, now redirected to a file
        sys._debugmallocstats()

    # restore stderr
    os.dup2(oldstderr, 2)

    if do_print:
        with open(filename, "r") as f:
            for line in f:
                if "arenas" in line or "unused pools" in line:
                    print(line, end="")


if __name__ == "__main__":
    print(f"Running in pid {PID}")

    # make a bunch of lists that call CPython's arena allocator
    print("Building a bunch of dummy lists to create a lot of arenas and consume memory\n")
    lsts = [_dummy_list() for _ in range(NUM_DUMMIES)]
    peak_rss = PROC.memory_info().rss/1e6
    print(f"Resident set size: {peak_rss:.1f} MB\n")

    _dump_alloc_info("before.txt")

    num_del = len(lsts) // 4

    print("\n---\n")
    print(f"Removing {num_del}/{len(lsts)} lists (~25%) from the list-of-lists\n")
    indices = sorted(random.choices(range(len(lsts)), k=num_del))
    for num, idx in enumerate(indices):
        del lsts[idx-num]
        num += 1

    # NOTE: not really necessary for this simple program, but let's be REALLY
    # sure that the objects we just freed up were collected and the underlying
    # memory reclaimed
    gc.collect()

    _dump_alloc_info("after.txt")

    offpeak_rss = PROC.memory_info().rss/1e6
    print("\n---\n")
    print(f"Resident set size: {offpeak_rss:.1f} MB")
    print(f"---\nRatio of off-peak and peak RSS usage: {offpeak_rss/peak_rss:.3f}")
    print("Detailed allocator stats written to before.txt and after.txt")

