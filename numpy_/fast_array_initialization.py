"""
This example was born of a discussion in freenode #python where someone
suggested `0*arr` as a good way to get an array of zeros the same shape as
`arr`. While this is correct, it's WAY slower, and we should absolutely prefer
`np.zeros()` (or `np.empty()` if we don't strictly need initialization)
instead. The difference may only be a factor of 2 or so for small matrices
(where overhead will dominate), but grows quickly to several orders of
magnitude for not-particularly-large matrices!
"""
import numpy as np
import timeit

num = 100
for N in (10, 20, 50, 100, 200, 500, 1000):
    arr = np.random.random(N ** 2).reshape((N, N))

    print(f"For {N}x{N} matrices...")

    setup = f"import numpy as np"

    mult_time = min(
        timeit.repeat(
            "np.zeros(shape=arr.shape)", setup=setup, number=num, globals={"arr": arr}
        )
    )
    print(f"`zeros()` took {mult_time:.2e} s (best of 3, {num} trials each)")

    mult_time = min(
        timeit.repeat(
            "np.empty(shape=arr.shape)", setup=setup, number=num, globals={"arr": arr}
        )
    )
    print(f"`empty()` took {mult_time:.2e} s (best of 3, {num} trials each)")

    mult_time = min(
        timeit.repeat("0*arr", setup=setup, number=num, globals={"arr": arr})
    )
    print(f"`0*arr` took {mult_time:.2e} s (best of 3, {num} trials each)\n")


# For 10x10 matrices...
# `zeros()` took 6.50e-05 s (best of 3, 100 trials each)
# `empty()` took 6.30e-05 s (best of 3, 100 trials each)
# `0*arr` took 1.29e-04 s (best of 3, 100 trials each)
#
# For 20x20 matrices...
# `zeros()` took 9.81e-05 s (best of 3, 100 trials each)
# `empty()` took 7.36e-05 s (best of 3, 100 trials each)
# `0*arr` took 1.58e-04 s (best of 3, 100 trials each)
#
# For 50x50 matrices...
# `zeros()` took 1.76e-04 s (best of 3, 100 trials each)
# `empty()` took 7.28e-05 s (best of 3, 100 trials each)
# `0*arr` took 2.99e-04 s (best of 3, 100 trials each)
#
# For 100x100 matrices...
# `zeros()` took 4.32e-04 s (best of 3, 100 trials each)
# `empty()` took 7.37e-05 s (best of 3, 100 trials each)
# `0*arr` took 6.64e-04 s (best of 3, 100 trials each)
#
# For 200x200 matrices...
# `zeros()` took 1.94e-03 s (best of 3, 100 trials each)
# `empty()` took 7.00e-05 s (best of 3, 100 trials each)
# `0*arr` took 3.24e-03 s (best of 3, 100 trials each)
#
# For 500x500 matrices...
# `zeros()` took 1.21e-02 s (best of 3, 100 trials each)
# `empty()` took 7.61e-05 s (best of 3, 100 trials each)
# `0*arr` took 1.96e-02 s (best of 3, 100 trials each)
#
# For 1000x1000 matrices...
# `zeros()` took 5.69e-02 s (best of 3, 100 trials each)
# `empty()` took 7.29e-05 s (best of 3, 100 trials each)
# `0*arr` took 1.19e-01 s (best of 3, 100 trials each)
