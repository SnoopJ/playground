import inspect


def _current_func(offset: int=0):
    """
    Returns the name of the function object at the given offset (default: caller) or None

    Parameters
    ----------
    offset: int, optional
        Offset to the target frame from the caller's location.
    """
    _frame = inspect.currentframe()
    _caller_frame = inspect.getouterframes(_frame)[1 + offset]
    _funcname = getattr(_caller_frame, "function", None)

    if _funcname is None:
        return None
    else:
        # NOTE: kind of a sloppy way to do this, but it should be exact for offset=0
        return globals()[_funcname]


def first_func():
    print(f"Current function is: {_current_func()}")


def second_func():
    print(f"Current function is: {_current_func()}")


third_func = first_func  # NOTE: this doesn't change the function object's name!

print("first_func()")
first_func()

print()

print("second_func()")
second_func()

print()

# will be "first_func"
print("third_func()")
third_func()


class Foo:
    def bar(self):
        print(f"Current function is: {_current_func()}")


# Unfortunately, this code can't tell if we're inside an instance method, but
# the function name is at least still accessible. We could cheat and look for
# the name "self" in the caller's locals (this is what pudb does, for
# instance), but this isn't guaranteed to work. I don't know if there's a way
# to do that, do you? :)
print("Foo().bar()")
Foo().bar()
