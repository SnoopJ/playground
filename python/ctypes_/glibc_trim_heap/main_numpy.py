import ctypes
import ctypes.util
import os

import numpy as np


PID = os.getpid()

libc = ctypes.CDLL(ctypes.util.find_library('c'))


MiB = 1024 * 1024
TARGET_RAM = 500 * MiB
ALLOC_SIZE = 64
# NOTE: the factor of 4 here is an eyeball guess that roughly accounts for the
# memory consumed by the rest of this program (i.e. the ndarray list)
N_ALLOC = int(TARGET_RAM / ALLOC_SIZE / 4)


def report_mem(msg):
    with open(f"/proc/{PID}/status", "r") as f:
        mem_line = next(line for line in f if line.startswith("VmRSS:"))
        mem_line = mem_line[len("VmRSS:"):-3]
        mem_KiB = int(mem_line)

    if msg:
        print(msg)
    print(f"VmRSS: {mem_KiB:>8} KiB\n")


###

report_mem("Before allocation")
print(f"Creating {N_ALLOC} int8 ndarrays of size {ALLOC_SIZE} …")
arrs = [np.array(list(range(64)), dtype=np.int8) for _ in range(N_ALLOC)]
report_mem("After allocation")

print("ndarrays going out of scope")
del arrs
report_mem("After free")

print("Calling malloc_trim")
libc.malloc_trim(0)
report_mem("After malloc_trim()")
