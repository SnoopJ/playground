"""
A little script I screwed around with when teaching myself multiprocessing
"""
import multiprocessing
import random
import time
from pprint import pprint

data = {k:v for k,v in [(num, random.random()*0.5) for num in range(5)]}

def poolworker(wid, dt):
    print(f"In worker #{wid}, going to sleep for {dt:.2f} sec")
    time.sleep(dt)
    return [wid*n for n in range(5)]

def cb_factory(*args):
    def result(res):
        print(f"for args={args}, result: {res}")
    return result

if __name__ == "__main__":
    with multiprocessing.Pool(5) as pool:
        res = [pool.apply_async(poolworker, (wid, dt), callback=cb_factory(wid, dt)) for wid, dt in data.items()]

        print("pool's closed")
        pool.close()  

        print("waiting for everyone to get out of the pool")
        pool.join()  # wait for everything

        print("everyone's out")
        pprint([r.get() for r in res])
