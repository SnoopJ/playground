"""
Based on a question in Freenode #python on 11 May 2021
"""
from typing import Iterable

import numpy as np


def common_rows(a: np.ndarray, b: np.ndarray, debug: bool=False) -> Iterable[tuple[int, int]]:
    """
    Yields the indices of combinations of equal rows in `a, b`

    Parameters
    ----------
    a, b: np.ndarray
        The arrays to compare, must be shape (N, C), (M, C)
    debug: bool
        If True, print every row comparison

    Yields
    -------
    idx_a : int
    idx_b : int

    Notes
    -----
    Uses the `nditer` interface [1] in `"external_loop"` mode [2] to iterate over all
    combinations of rows (i.e. entries along the first axis), performing comparisons
    as we go. This function is equivalent to

        ```
        (a[:, np.newaxis] == b).all(axis=-1).any(axis=0)
        ```

    **except** that this function does not create the intermediate values implied
    above. In particular, the broadcast and equality comparison above always requires
    O(N*M) space, where this function should (hopefully?) only use a constant amount
    of memory, regardless of the input sizes. It's still O(N*M) in time, and it is
    slower than a Cythonized counterpart [3] would be because of the Python loop embedded
    in it (I got ~50k iter/sec. on a single 2.2 GHz core)

    References
    ----------
    [1] https://numpy.org/devdocs/reference/arrays.nditer.html
    [2] https://numpy.org/devdocs/reference/arrays.nditer.html#using-an-external-loop
    [3] https://numpy.org/devdocs/reference/arrays.nditer.html#putting-the-inner-loop-in-cython
    """
    compatible = (a.ndim == b.ndim == 2 and
                  a.shape[1] == b.shape[1])
    if not compatible:
        raise ValueError(f"Expected arrays of shape (N, C), (M, C), got: {a.shape}, {b.shape}")

    # this mapping of axes advances fastest along `b`, see: https://numpy.org/devdocs/reference/arrays.nditer.html#outer-product-iteration
    axes_a = (0, -1, 1)
    axes_b = (-1, 0, 1)
    it = np.nditer(
            [a, b],
            flags=["external_loop"],  # the `external_loop` flag will give as much data at once as it can
            op_axes=[axes_a, axes_b])

    with it:
        for Ncmp, (row_a, row_b) in enumerate(it):
            if debug:
                print("data: ", row_a, row_b)
            if np.array_equal(row_a, row_b):
                idxa, idxb = divmod(Ncmp, b.shape[0])
                yield idxa, idxb


def make_arrays(N: int, M: int, Lrows: int, seed=None) -> tuple[np.ndarray, np.ndarray]:
    # use a dedicated RandomState for cross-run determinism if we were given a seed
    rnd = np.random.RandomState(seed)
    arr1 = rnd.randint(0, 10, size=(N, Lrows))
    arr2 = rnd.randint(0, 10, size=(M, Lrows))

    return arr1, arr2


if __name__ == "__main__":
    N = 100
    M = 300
    arr1, arr2 = make_arrays(N, M, Lrows=3, seed=42)

    # choose a random row from arr2 and replace a random row of arr1 with it,
    # to guarantee that we have an overlap. These calls to randint() are NOT
    # deterministic, so that we get different results on each run
    # NOTE: it's possible that the random match we create comes after some other naturally-occurring match
    idx1 = np.random.randint(N)
    idx2 = np.random.randint(M)
    print(f"Guaranteeing at least a match between rows {idx1} and {idx2}")
    arr1[idx1, ...] = arr2[idx2, ...]

    Nmatches = 0
    for Nmatches, match in enumerate(common_rows(arr1, arr2), 1):
        Lidx, Ridx = match
        print(f"Rows {Lidx} and {Ridx} match")

    if Nmatches == 0:
        print("No matches :(")
    else:
        print(f"{Nmatches=}")
