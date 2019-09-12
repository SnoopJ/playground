"""
Based on a question in Freenode #python on Sept 12, 2019 about finding
all combinations of entries in an ndarray.

It *feels* like there should be a more numpythonic solution that creates the
`indices` in a single call, but I can't figure it out. The number of such
combinations is `Nvec*(Nvec-1)`, so this solution is probably only bad if Nvec
becomes quite large, and in that case you'd be creating a large array with numpy
anyway...
"""
import numpy as np
from itertools import combinations

Nvec = 4
Lvec = 3

arr = np.arange(Nvec*Lvec).reshape((Nvec, Lvec))

print("Initial array:")
print(arr)

indices = list(combinations(range(Nvec), 2))

print("Pairs of indices:")
print(indices)

# Need an ndarray for indexing purposes
indices = np.asarray(indices)

pairings = arr[indices]
print(f"Unique pairings of vectors ({indices.size} total):")
print(arr[indices])
