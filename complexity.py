"""
  Illustrating the time complexity of builtin Python types
"""
import timeit
from textwrap import dedent
import random
import sys
from string import ascii_letters as letters

N = 20_000
NUMTEST = 100_000

sortedlist = list(range(N))
randlist = sortedlist.copy()
random.shuffle(randlist)
d = {i:i for i in range(N)}

#for obj in ('sortedlist', 'randlist', 'd'):
#    for testval in (0, N, 2*N, random.randint(0, N)):
#        dt = timeit.timeit(f'testval in {obj}', number=NUMTEST, globals=locals())
#        print(f'Time for {NUMTEST} evaluations of `{testval} in {obj}`:\t\t {dt:.1e} sec (avg = {dt/NUMTEST:.2e} sec)')
#
#        op = dedent(
#        f"""
#        try:
#            {obj}[testval]
#        except:
#            pass
#        """)
#
#        dt = timeit.timeit(op, number=NUMTEST, globals=locals())
#        print(f'Time for {NUMTEST} evaluations of `{obj}[{testval}]`:\t\t {dt:.1e} sec (avg = {dt/NUMTEST:.1e} sec)')
#        
#        op = dedent(
#        f"""
#        try:
#            {obj}[testval] = 'foo'
#        except:
#            pass
#        """)
#
#        dt = timeit.timeit(op, number=NUMTEST, globals=locals())
#        print(f'Time for {NUMTEST} evaluations of `{obj}[{testval}] = "foo"`:\t\t {dt:.1e} sec (avg = {dt/NUMTEST:.1e} sec)')

d = {i:i for i in range(10)}
l = list(range(10))

sizes = [(len(d), sys.getsizeof(l), sys.getsizeof(d))]
for Nresize in range(15):
    while sys.getsizeof(d) <= sizes[-1][2]:
        r1 = ''.join(random.choice(letters) for _ in range(10))
        r2 = ''.join(random.choice(letters) for _ in range(10))
        d[r1] = r2
        l.append(r2)
    sizes.append((len(d)-1, sys.getsizeof(l), sys.getsizeof(d)))
    print(f'Dict resize {Nresize+1:>2} at {sizes[-1][0]:>10} elements! Old size = {sizes[-2][2]:>10} bytes, New size = {sizes[-1][1]:>10} bytes (ratio ~ {sizes[-1][2]/sizes[-2][2]:.1f})')
    print(f'{"":>29}d/l = {sizes[-1][2]/sizes[-1][1]:.2f}')


