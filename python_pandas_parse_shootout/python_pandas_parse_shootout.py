import pandas as pd
import re
import time

filename = '10um-10nm-1000F.dat'

class Foo:
    pass

thisrun = Foo()

t1 = time.time()
# pre-existing way
with open(filename, 'r') as f:
    for line in f:
        if re.search(r'\s*sphere\s*host', line) is not None:
            headers = line.split()
            line = next(f)
            thisrun.sphere_data_dict = dict()
            while re.match(r'^\s*\d+', line):
                thisrow = line.split()
                thisdict = {a: float(b) for a, b in
                            zip(headers[1:], thisrow[1:])}
                thisdict['host'] = int(thisdict['host'])
                thisrun.sphere_data_dict[int(thisrow[0])] = thisdict
                line = next(f)

t2 = time.time()
dt = 1e3*(t2-t1)
print(f"Python loop with re, comprehensions: {dt:.2f} ms")

# pandas way
with open(filename, 'r') as f:
    lines = f.readlines() # rather than iterating lazily, let's just load it all

    startidx, header = next((i, line) for i, line in enumerate(lines) if line.strip().startswith('sphere'))
    endidx = next(i for i, line in enumerate(lines) if line.strip().startswith('unpolarized'))

    data = pd.DataFrame(lines[startidx:endidx]).to_dict()

t3 = time.time()
dt = 1e3*(t3-t2)
print(f"Pandas approach: {dt:.2f} ms")
