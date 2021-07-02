from functools import partial
import multiprocessing
import random
import time
from queue import Empty as QueueEmpty


class QueueWriteHelper:
    def __init__(self, q: multiprocessing.Queue):
        self._q = q

    def write(self, msg):
        self._q.put(msg, block=False)


def worker(q):
    q = QueueWriteHelper(q)
    print = partial(__builtins__.print, file=q)
    N = random.randint(3, 8)

    for n in range(N):
        dt = 2*random.random()
        print(f"message {n} (sleeping for {dt:.3e} sec)")
        time.sleep(dt)


def main():
    q = multiprocessing.Queue()
    proc = multiprocessing.Process(target=worker, args=(q,))
    proc.start()
    breakpoint()

    start = time.time()
    while proc.is_alive():
        try:
            line = q.get(block=False).strip()
            if line:
                end = time.time()
                dt = end-start
                print(f"Got message after {dt:.3e} sec:")
                print(f"\t{line}")
                start = end
        except QueueEmpty as exc:
            pass


if __name__ == "__main__":
    main()
