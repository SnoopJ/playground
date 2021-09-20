from functools import partial

def f(x, m, b):
    """Gives the value `y = m*x + b`"""
    return m*x + b

# here we use partial to make two objects that can be called with just the value of x,
# i.e. we have "frozen" their values of m, b
line1 = partial(f, m=2, b=0)
line2 = partial(f, m=-2, b=10)

STEP = 1
for line in (line1, line2):
    for stepnum in range(10):
        x = stepnum*STEP
        y = line(x)
        print(f"{x=}, {y=}")
    print("---")
