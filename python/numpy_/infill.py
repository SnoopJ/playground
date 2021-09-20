import numpy as np


# def infill(arr, N):
#    """
#    Given a 1D array (or array-like) `arr`, return a new array with `N` new equally-spaced steps between every entry.
#
#    Parameters
#    ----------
#    arr - input array or array-like
#    N - (int) number of steps to interpolate
#
#    Examples
#    --------
#    >>> arr = np.array([1,2,3])
#    >>> infill(arr, 2)
#    array([1.        , 1.33333333, 1.66666667, 2.        , 2.33333333, 2.66666667, 3.        ])
#    >>> infill(arr, 3)
#    array([1.  , 1.25, 1.5 , 1.75, 2.  , 2.25, 2.5 , 2.75, 3.  ])
#
#    Returns
#    -------
#    filled - ndarray (with implicit dtype), shape (arr.size + N*(arr.size-1),)
#    """
#    arr = np.asarray(arr)
#    assert arr.ndim == 1, "Array must be 1-dimensional"
#    assert N > 0
#    aligned = np.stack((arr[:-1], arr[1:]), axis=-1)
#    result = np.empty(arr.size + N * (arr.size - 1))
#    # it's intuitive to do this by just collating the results of each linspace() below and using np.concatenate(), but
#    # allocating ahead of time is imo the best idea, because we only have to hold one intermediate linspace() in memory,
#    # which could mean substantial savings in the case of a very large input (or N)
#    for idx, (start, stop) in enumerate(aligned):
#        # N.B. this overlaps the previous region so we don't double-count the endpoints with our linspace()!
#        # we could instead pass endpoint=False to linspace(), but then we'd have to do `result[-1] = arr[-1]`
#        # at the end of the loop to handle the edge case, which feels inelegant.
#        sidx = idx * (N + 1)
#        eidx = sidx + (N + 2)
#        result[sidx:eidx] = np.linspace(start, stop, N + 2)
#    return result
def infill(arr, N):
    """
    Given a 1D array (or array-like) `arr`, return a new array with `N` new equally-spaced steps between every entry.
    
    Parameters
    ----------
    arr - input array or array-like
    N - (int) number of steps to interpolate
    
    Examples
    --------
    >>> arr = np.array([1,2,3])
    >>> infill(arr, 2)
    array([1.        , 1.33333333, 1.66666667, 2.        , 2.33333333, 2.66666667, 3.        ])
    >>> infill(arr, 3)
    array([1.  , 1.25, 1.5 , 1.75, 2.  , 2.25, 2.5 , 2.75, 3.  ]) 
    
    Returns
    -------
    filled - ndarray, shape (arr.size + N*(arr.size-1),)
    """
    arr = np.asarray(arr)
    assert arr.ndim == 1, "Array must be 1-dimensional"
    assert N > 0
    Nintervals = arr.size - 1
    # the arithmetic here is:
    #     old_size + (Npts * Nintervals)
    Nsamples = arr.size + N * (arr.size - 1)
    samples = np.linspace(0, Nintervals, Nsamples)
    # the trick here is to create a function mapping an index to a value
    # and then piecewise interpolate (which `np.interp()` does by default).
    # Cheers to Alexer from Freenode #python for this improvement over the
    # one above!
    return np.interp(samples, np.arange(arr.size), arr)


arr = np.array([1, 2, 3])
for i in (2, 3):
    print(f"infill(arr, {i}):\n{infill(arr, i)}")
