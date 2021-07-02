import numpy as np

# see https://jamesgerity.com/remembery/img/numpy_ndarray.png for the structure of ndarray

arr = np.arange(2*2*3)  # 12 distinct values, in terms of how they can be cleanly divided
print(f"{arr.shape=}, {arr.size=}, {arr.ndim}")
print(f"arr=\n{arr}")

# `arr` is one-dimensional, just some numbers in memory: 
#   arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# If we "stride" over those numbers, we can treat them as though they are 
# N-dimensional. E.g. let's build an array with two "columns" (a new axis) by
# taking two values at a time to make each "row"

arr2 = arr.reshape(2*3, 2)  # note: reshape() takes an argument called `order` 
                            # which is 'C' by default (for the language C, 
                            # where the LAST axis varies the "fastest")
print(f"{arr2.shape=}, {arr2.size=}, {arr2.ndim}")
print(f"arr2=\n{arr2}")

# Now, arr2 is two-dimensional, with 6 rows, 2 columns:
#   arr2 = np.array([[0, 1]
#                    [2, 3],
#                    [4, 5], 
#                    [6, 7],
#                    [8, 9],
#                    [10, 11]])
# Note how arr2 "counts up" by reading first across the columns, then down the rows

# NOTE: the `order` argument to reshape() tells us which in what order to
# collect values. If we pass `order='F'` (for the language Fortran, where the 
# FIRST axis varies "fastest")

arr2_F = arr.reshape(2*3, 2, order='F')
print(f"{arr2_F.shape=}, {arr2_F.size=}, {arr2_F.ndim}")
print(f"arr2_F=\n{arr2_F}")

# Note how arr2_F "counts up" by reading first the first column down the rows, then the second
#   arr2_F = np.array([[0, 6]
#                      [1, 7],
#                      [2, 8], 
#                      [3, 9],
#                      [4, 10],
#                      [5, 11]])

arr3 = arr.reshape(2, 2*3)  # this reshape does 2 rows, 6 columns. To build
                            # each row, we'll take the next 6 values in the array
print(f"{arr3.shape=}, {arr3.size=}, {arr3.ndim}")
print(f"arr3=\n{arr3}")

# arr3 is also two-dimension, with 2 rows, 6 columns:
#   arr3 = np.array([[0, 1, 2, 3, 4, 5],
#                    [6, 7, 8, 9, 10, 11]])

# We can have as many axes as we want, as long as the product of all the axis sizes is equal to the number of elements.

arr4 = arr.reshape(2, 2, 3)  # this is a 3D array, with 2 "rows", 2 "columns", and 3 steps of "depth"
print(f"{arr4.shape=}, {arr4.size=}, {arr4.ndim}")
print(f"arr4=\n{arr4}")

# NOTE: since N*1 = N for all N, we can have as many size-1 axes as we want:

arr5 = arr.reshape(1, 2, 2, 3, 1)  # this is a 5D array!
print(f"{arr5.shape=}, {arr5.size=}, {arr5.ndim}")
print(f"arr5=\n{arr5}")
