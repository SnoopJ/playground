"""
Apparently, you can yield from lambdas _and_ comprehensions! The latter
is interesting because in Py2, list comprehensions were *not* functions,
but basically fancy for loops. I.e. try:

    def f():
      [x for x in range(5)]

    dis.dis(f)

in both Py2 and Py3. In Py3, also look at the bytecode of the stored 
`<code <listcomp>>` object:

    dis.dis(f.__code__.co_consts[1])

In Py2, you *can* do `{(yield x) for x in range(5)}`, but 
`[(yield x) for x in range(5)]` is a syntax error! Both are acceptable
(if not grotesque) in Py3.
"""

import dis


lstgenfactory = lambda: [(yield x + 1) for x in range(10)]
setgenfactory = lambda: {(yield x + 1) for x in range(10)}
seqgenfactory = lambda: ((yield 1), (yield 2))

lstgen = lstgenfactory()
setgen = setgenfactory()
seqgen = seqgenfactory()

gen = (x + 1 for x in range(10))


def genfunc():
    for x in range(10):
        yield x + 1


print("\nList comp lambda bytecode:")
dis.dis(lstgen)

print("\nSet comp lambda bytecode:")
dis.dis(setgen)

print("\nDequence lambda bytecode:")
dis.dis(seqgen)

print("\nGenerator comprehension bytecode:")
dis.dis(gen)

print("\nGenerator function bytecode:")
dis.dis(genfunc)
