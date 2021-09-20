"""
  My blind attempt at function composition. Turns out this is part of the `toolz` library, which
  has some nice features like composition of docstrings (!!!)
  https://github.com/pytoolz/toolz
"""
import inspect
import collections

def _is_seq(obj):
    return isinstance(obj, collections.abc.Sequence)

def _accepts_kwarg(func, k):
    """ Return True if func accepts k as a keyword argument """
    s = inspect.getfullargspec(func)
    return (s.varkw or
            k in s.args or
            k in s.kwonlyargs
            )

def compose(*funcs, **kwargs):
    """
    Return a composition of functions, calculating f1(*f2(..., **kwargs2), **kwargs1)
    where only keyword arguments allowed by each function's spec will be passed at
    each call.

    N.B. functions from `funcs` are applied in reverse order, i.e. `compose(f, g)`
    should be read as "f of g"
    """
    def inner(*args):
        res = tuple(args)
        for f in reversed(funcs):
            res = f(*res, **{k:v for k,v in kwargs.items() if _accepts_kwarg(f, k)})
            if not _is_seq(res):  # ensure *res makes sense if it is not a sequence
                res = (res,)
        return res

    return inner

if __name__ == '__main__':
    def f(n):
        return n+1

    def g(n):
        return 2*n

    def h(a, b):
        return b, a

    def i(a, b):
        return a/b, a*b

    print('f(g(1)) = {}'.format(compose(f, g)(1)))
    print('g(f(1)) = {}'.format(compose(g, f)(1)))
    print('h(i(1, 2)) = {}'.format(compose(h, i)(1, 2)))
    print('i(h(1, 2)) = {}'.format(compose(i, h)(1, 2)))
