from inspect import getdoc

def wrap(f):
    def g(*args, **kwargs):
        print('hi from wrap()')
        return f(*args, **kwargs)
    return g

def wrap_withdoc(f):
    def g(*args, **kwargs):
        print('hi from wrap_withdoc()')
        return f(*args, **kwargs)
    g.__docstring__ = getdoc(f)
    return g

@wrap
def foo():
    """ foo's docstring """
    print('hi')

@wrap_withdoc
def bar():
    """ bar's docstring """
    print('yo')

help(foo)
help(bar)
