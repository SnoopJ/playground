"""
StopIteration is a fundamental part of the iterator protocol, and this can 
lead to some surprising bugs in Python prior to 3.7. From PEP 479: 

"StopIteration raised accidentally inside a generator function will be
interpreted as the end of the iteration by the loop construct driving the
generator."

Try running this file with an interpreter <= 3.6, and 3.7+ to see the
difference. The former will silently end the outer generator without
indicating that the final value has been skipped, the latter will convert the
StopIteration into a RuntimeError which is raised.

Lots more information in PEP 479:
https://www.python.org/dev/peps/pep-0479/
"""

def outer():
    def inner():
        it = iter([1,2,3])
        yield next(it)  # yields 1
        yield next(it)  # yields 2
        yield next(it)  # yields 3
        yield next(it)  # raises StopIteration
        yield "final value"  # this is unreachable, but prior to 3.7 you wouldn't know you'd missed any values

    # → In Python <= 3.6, the StopIteration  from next() will be erroneously
    # interpreted as signaling the (successful) end of inner(), missing the
    # final value
    # → In Python 3.7+, the StopIteration from next() is converted to a
    # RuntimeError before it leaves inner()
    yield from inner()

if __name__ == "__main__":
    try:
        l = list(outer())
        print(f"No exception, result is l={l}")
    except Exception as exc:
        print(f"Got exception: {repr(exc)}")
