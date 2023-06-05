import ctypes
import ctypes.util
import os


PID = os.getpid()

libc = ctypes.CDLL(ctypes.util.find_library('c'))
libc.malloc.restype = ctypes.c_void_p
libc.free.argtypes = [ctypes.c_void_p]


MiB = 1024 * 1024
TARGET_RAM = 500 * MiB
ALLOC_SIZE = 64
# NOTE: the factor of 2 here is an eyeball guess that roughly accounts for the
# memory consumed by the rest of this program (i.e. the pointer list)
N_ALLOC = int(TARGET_RAM / ALLOC_SIZE / 2)


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
print(f"Creating {N_ALLOC} allocations of size {ALLOC_SIZE} …")
ptrs = [libc.malloc(ALLOC_SIZE) for _ in range(N_ALLOC)]
report_mem("After allocation")

print("free()ing allocations")
for p in ptrs:
    libc.free(p)
del ptrs
report_mem("After free")

print("Calling malloc_trim")
libc.malloc_trim(0)
report_mem("After malloc_trim()")
