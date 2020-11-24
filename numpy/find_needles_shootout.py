import numpy as np

np.random.seed(0)  # for the sake of fair comparison, every test uses the same data

N = 10_000_000
num_needles = 10
arr = np.random.random(N)  # haystack is [0, 1)
arr[np.random.randint(0, N, size=num_needles)] = -1  # needles

def numpy_loop():
    """Rely entirely on numpy vectorization"""
    yield from arr[arr < 0]

def python_loop():
    """Rely entirely on python looping"""
    yield from (elem for elem in arr if elem < 0)

def python_chunked_loop(scantwice=False):
    """
    Chunk the search space

    With the numpy optimization enabled, this *might* outperform numpy_loop() 
    in lazy contexts where we don't immediately need the location of any needle
    farther along than the current one. It seems to vary quite a bit, and 
    overall I think it's more fuss than it's worth. If I really cared, I'd be
    writing this in Cython.
    """
    chunksize = N//10
    for idx in range(0, chunksize):
        chunk = arr[chunksize*idx:chunksize*(idx+1)]
        gen = (elem for elem in chunk if elem < 0)  # basically the same as python_loop, but smaller search space
        if scantwice:  # optimization: let numpy check for the needle first
            if (chunk < 0).any():
                yield from gen
        else:
            # performance in this branch should be nearly identical to python_loop()
            yield from gen
