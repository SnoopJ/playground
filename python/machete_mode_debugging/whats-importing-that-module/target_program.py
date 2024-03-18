# we modify the target program to install the hook before the rest of the
# code we are trying to audit
import sys
import hook
hook.install()

# BEGIN unmodified target program
import numpy

from helper import somefunc


def random_array():
    arr = np.random.randint(0, 255, size=(30, 50))

    return arr, somefunc()
