"""
Adding a global legend to a matplotlib figure with subplots
Based on a question in #python on freenode, Nov 7, 2018
"""
import matplotlib

matplotlib.use("agg")
from matplotlib import pyplot as plt
import numpy as np

arr = np.array([1, 2, 3])
fig = plt.figure(figsize=(2 * 4, 4))
plt.subplot(121)
l1 = plt.plot(arr, arr ** 2, label="foo")
l2 = plt.plot(arr, arr ** 3, label="bar")

plt.subplot(122)
l3 = plt.plot(arr, arr ** 2, "k--", label="bin")
l4 = plt.plot(arr, arr ** 3, "rs", mfc="none")  # no label!

lgnd = fig.legend(
    bbox_to_anchor=(1.1, 1.0)
)  # unfortunately, loc='best' doesn't work very well here
fig.tight_layout()

# the legend is not accounted for by default when calling savefig(), so we need to give some hints
# N.B. that `bbox_extra_artists` is not strictly necessary here to get the right output, but it's a good idea!
fig.savefig("out_clipped.png")
fig.savefig("out.png", bbox_extra_artists=[lgnd], bbox_inches="tight")
