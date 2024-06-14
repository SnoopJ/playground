"""
An experiment in re-writing the signature of a pure Python function to change some arguments into keyword-only arguments

This is probably not useful to do in production code, but I found myself wondering if it was possible after encountering
some upstream code that *really* should have not let me pass some parameters by position
"""
import inspect
from collections.abc import Callable
from typing import Any


def func(val, obscure_param1, obscure_param2):
    """
    This dummy function illustrates a function that would have been more wisely written with a keyword-only argument
    """
    ...


def convert_trailing_args_to_kwonly(fn: Callable[..., Any], Nargs: int) -> Callable[..., Any]:
    old_argcount = func.__code__.co_argcount
    old_kwonlyargcount = func.__code__.co_kwonlyargcount

    if Nargs > old_argcount:
        raise ValueError(f"Cannot convert {Nargs} arguments: target function only has {old_argcount} positional arguments")

    new_code = func.__code__.replace(
        co_argcount=old_argcount-Nargs,
        co_kwonlyargcount=old_kwonlyargcount+Nargs,
    )

    new_func = type(func)(
        new_code,
        name=f"{fn.__name__}__converted_{Nargs}kwargs",
        globals=fn.__globals__,
    )

    return new_func


functions = [
    func,
    convert_trailing_args_to_kwonly(func, 1),
    convert_trailing_args_to_kwonly(func, 2),
    convert_trailing_args_to_kwonly(func, 3),
]

args = [
    ("val", 1),
    ("obscure_param1", 2),
    ("obscure_param2", 3)
]
for f in functions:
    print(f"{f.__name__}():\n  {inspect.getfullargspec(f)}\n==============")
    for n in range(3, -1, -1):
        posargs = [val for (name, val) in args[:n]]
        kwargs = {name:val for (name, val) in args[n:]}
        try:
            f(*posargs, **kwargs)
            print(f"SUCCESS: called with {n} positional arguments, {3-n} keyword arguments")
        except:
            print(f"FAILED: called with {n} positional arguments, {3-n} keyword arguments")
    print()

# Output:
# -------
# $ python3 convert_arg_to_kwonly.py
# func():
#   FullArgSpec(args=['val', 'obscure_param1', 'obscure_param2'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={})
# ==============
# SUCCESS: called with 3 positional arguments, 0 keyword arguments
# SUCCESS: called with 2 positional arguments, 1 keyword arguments
# SUCCESS: called with 1 positional arguments, 2 keyword arguments
# SUCCESS: called with 0 positional arguments, 3 keyword arguments
# 
# func__converted_1kwargs():
#   FullArgSpec(args=['val', 'obscure_param1'], varargs=None, varkw=None, defaults=None, kwonlyargs=['obscure_param2'], kwonlydefaults=None, annotations={})
# ==============
# FAILED: called with 3 positional arguments, 0 keyword arguments
# SUCCESS: called with 2 positional arguments, 1 keyword arguments
# SUCCESS: called with 1 positional arguments, 2 keyword arguments
# SUCCESS: called with 0 positional arguments, 3 keyword arguments
# 
# func__converted_2kwargs():
#   FullArgSpec(args=['val'], varargs=None, varkw=None, defaults=None, kwonlyargs=['obscure_param1', 'obscure_param2'], kwonlydefaults=None, annotations={})
# ==============
# FAILED: called with 3 positional arguments, 0 keyword arguments
# FAILED: called with 2 positional arguments, 1 keyword arguments
# SUCCESS: called with 1 positional arguments, 2 keyword arguments
# SUCCESS: called with 0 positional arguments, 3 keyword arguments
# 
# func__converted_3kwargs():
#   FullArgSpec(args=[], varargs=None, varkw=None, defaults=None, kwonlyargs=['val', 'obscure_param1', 'obscure_param2'], kwonlydefaults=None, annotations={})
# ==============
# FAILED: called with 3 positional arguments, 0 keyword arguments
# FAILED: called with 2 positional arguments, 1 keyword arguments
# FAILED: called with 1 positional arguments, 2 keyword arguments
# SUCCESS: called with 0 positional arguments, 3 keyword arguments


