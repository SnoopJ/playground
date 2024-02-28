from __future__ import annotations
import time
from textwrap import dedent


NUM_WORKERS = 0


def worker(N: int, numcalls: int) -> Callable:
    """
    Generate a worker that simulates some work by building a list of size N
    """
    global NUM_WORKERS

    # this is the easiest way I know of to define a function with a given name
    # in a way that will actually show up in the profiler
    #
    # You can change the __name__ and __qualname__ of a function object, but
    # the profiler reports the co_name stored in the underlying code object,
    # which is read-only
    workername = f"worker_{NUM_WORKERS}_N{N}_numcalls{numcalls}"
    src = dedent(f"""\
    def {workername}():
        list(range({N}))
    """)
    exec(src, globals(), globals())

    NUM_WORKERS +=1

    func = globals()[workername]

    return func


WORKERS = {worker(N=10**power, numcalls=numcalls): numcalls for power in range(5, 8) for numcalls in range(1, 5)}


def main():
    for (func, numcalls) in WORKERS.items():
        print(f"{func.__name__}()")
        for n in range(numcalls):
            func()


if __name__ == "__main__":
    main()
