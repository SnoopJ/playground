from dataclasses import dataclass
import multiprocessing
import random
import time
from pprint import pprint

@dataclass
class WorkerState:
    phase: int = 0

def poolworker(did, dt):
    global state
    print(f"In datum #{did}, going to sleep for {dt:.2f} sec")
    print(f"{state=}")
    time.sleep(dt)
    state.phase += 1
    return [did*n for n in range(5)]

def cb_factory(*args):
    def result(res):
        print(f"for args={args}, result: {res}")
    return result

def _init():
    # only called when each worker Process starts up, NOT when submitting a datum
    global state
    state = WorkerState()
    print(state.phase)

if __name__ == "__main__":
    data = {k:v for k,v in [(num, random.random()*0.5) for num in range(10)]}

    with multiprocessing.Pool(5, initializer=_init) as pool:
        res = [pool.apply_async(poolworker, (did, dt), callback=cb_factory(did, dt)) for did, dt in data.items()]

        print("pool's closed")
        pool.close()  

        print("waiting for everyone to get out of the pool")
        pool.join()  # wait for everything

        print("everyone's out")
        pprint([r.get() for r in res])
