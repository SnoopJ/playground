"""
    Some ideas for a decorator factory that wraps the decorated function in a
    test of a predicate function AND passes the value along to the function to 
    be re-used.

    This was in response to a question in freenode #python on Oct 5, 2018.
"""
class PredicateError(Exception):
    pass

def predicate(**preds): 
    """
    Decorate a function with one or more predicate callables, and only call 
    the function if no predicate raises an exception. The result of each 
    predicate will be stored in the associated attribute on the decorated function.
    """
    def outer(f, *args, **kwargs):
      def dec(*args, **kwargs): 
          # here I use a predicate that accepts ALL args of the function, but 
          # this isn't strictly necessary
          for key, pred in preds.items():
              setattr(dec, key, pred(*args, **kwargs))
          return f(*args, **kwargs) 
      return dec
    return outer

def magnitude(*args):
    """ Predicate: the sum of squares of all values is less than 100 """
    mag = sum(val**2 for val in args)**0.5
    if mag >= 100:
        raise PredicateError('Magnitude larger than allowable!')
    else:
        return mag

import os, glob
def lsdirs(mask):
    """ Predicate: all directories matching `glob.glob(mask)` are nonempty """
    dirs = {d:os.listdir(d) for d in glob.glob(mask) if os.path.isdir(d)}
    for d,contents in dirs.items():
        if not len(contents):
            raise PredicateError('Directory {d} is empty!'.format(d=d))
    return dirs

@predicate(mag=magnitude)
def protected_sum(*args): 
    return sum(args)  

@predicate(d=lsdirs)
def getfiles(mask): 
    return getfiles.d.values()

print('protected_sum(1, 2, 3):\t\t{s}'.format(s=protected_sum(1, 2, 3)))
try:
    print('protected_sum(1, 100):\t\t{s}'.format(s=protected_sum(1, 100)))
except PredicateError:
    print('protected_sum(1, 100):\t\tfailed!')
