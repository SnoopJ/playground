"""
A little script I screwed around with when teaching myself multiprocessing
"""
import multiprocessing
import random
import time
from pprint import pprint

def poolworker(did, dt):
    print(f"In datum #{did}, going to sleep for {dt:.2f} sec")
    time.sleep(dt)
    return [did*n for n in range(5)]

def cb_factory(*args):
    def result(res):
        print(f"for args={args}, result: {res}")
    return result

def _init():
    # only called when each worker Process starts up, NOT when submitting a datum
    print("Hey, this is an initializer!")

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
