"""
Use sympy to compute the recurrence relation:

    seq[n] = f*seq[n-2] - seq[n-1]

Output:

0	1
1	x
2	0
3	x**2
4	-x**2
5	x**3 + x**2
6	-2*x**3 - x**2
7	x**4 + 3*x**3 + x**2
8	-3*x**4 - 4*x**3 - x**2
9	x**5 + 6*x**4 + 5*x**3 + x**2
----------------------------------------
0	x**2
1	x
2	10*x**2 - x
3	-10*x**2 + 11*x
4	110*x**2 - 21*x
5	-210*x**2 + 131*x
6	1310*x**2 - 341*x
7	-3410*x**2 + 1651*x
8	16510*x**2 - 5061*x
9	-50610*x**2 + 21571*x
"""
from itertools import islice

import sympy


x = sympy.symbols('x')

def seq(T0=x**0, T1=x, mult_factor=x):
    pprev = T0
    prev = T1
    yield pprev
    yield prev
    while True:
        cur = mult_factor*pprev - prev
        yield cur
        pprev, prev = prev, cur


if __name__ == "__main__":
    NUM_TERMS = 10
    for idx, val in enumerate(islice(seq(), NUM_TERMS)):
        print(f"seq[{idx}]", val.expand(), sep='\t')

    print("-"*40)

    for idx, val in enumerate(islice(seq(T0=x**2, T1=x, mult_factor=10), NUM_TERMS)):
        print(f"seq[{idx}]", val.expand(), sep='\t')
