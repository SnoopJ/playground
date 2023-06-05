This sample shows off how many small allocations made with [`glibc`'s `malloc()`](https://sourceware.org/glibc/wiki/MallocInternals)
may result in "high water mark" behavior, i.e. the memory used for these allocations
may not be returned to the OS after calling `free()`. The sample also shows off
how to call [`malloc_trim()`](https://man7.org/linux/man-pages/man3/malloc_trim.3.html)
using the `ctypes` library, which can reclaim memory set aside for the heap if
called immediately after such a pattern of allocations (NOTE: this is only able
to recover unused memory **from the top of the heap**, so in practice you'd want
to call this as soon as possible).

NOTE: The direct usage of `malloc()` by this program simulates allocations made
on behalf of some 3rd-party library that do not use `pymalloc`. For an example
using `numpy`, see `main_numpy.py`

### Sample output

```
$ python3 main.py
Before allocation
VmRSS:    11468 KiB

Creating 4096000 allocations of size 64 …
After allocation
VmRSS:   493388 KiB

free()ing allocations
After free
VmRSS:   331648 KiB

Calling malloc_trim
After malloc_trim()
VmRSS:    11652 KiB

$ python3 main_numpy.py
Before allocation
VmRSS:    29824 KiB

Creating 2048000 int8 ndarrays of size 64 …
After allocation
VmRSS:   464556 KiB

ndarrays going out of scope
After free
VmRSS:   253820 KiB

Calling malloc_trim
After malloc_trim()
VmRSS:    29912 KiB

```

Running these samples with [`PYTHONMALLOC=malloc`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONMALLOC)
to forcibly disable CPython's allocator may yield slightly more understandable
results, as there is no memory freed to the OS by the `del` statement.

```
$ PYTHONMALLOC=malloc python3 main.py
Before allocation
VmRSS:    11656 KiB

Creating 4096000 allocations of size 64 …
After allocation
VmRSS:   555336 KiB

free()ing allocations
After free
VmRSS:   523472 KiB

Calling malloc_trim
After malloc_trim()
VmRSS:    11488 KiB

$ PYTHONMALLOC=malloc python3 main_numpy.py
Before allocation
VmRSS:    29772 KiB

Creating 2048000 int8 ndarrays of size 64 …
After allocation
VmRSS:   493372 KiB

ndarrays going out of scope
After free
VmRSS:   477576 KiB

Calling malloc_trim
After malloc_trim()
VmRSS:    29608 KiB

```
