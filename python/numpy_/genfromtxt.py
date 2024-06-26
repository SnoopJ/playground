import numpy as np
import time

SAMPLEDATA = """Generated by trjconv : graphene in water t=   0.00000 ###ignore###
 4014
 1729SOL     OW    1   2.991   2.196   1.749 -0.0000  0.0000 -0.0000
 3065SOL    HW1 4010   0.057   1.693   1.608  0.0000  0.0000  0.0000
 3065SOL    HW2 4011   0.076   1.658   1.766 -0.0000  0.0000 -0.0000
 3066SOL     OW 4012   2.040   1.183   1.129 -0.0000 -0.0000  0.0000
 3066SOL    HW1 4013   1.970   1.154   1.063  0.0000  0.0000  0.0000
 3066SOL    HW2 4014   2.125   1.202   1.080  0.0001  0.0000 -0.0001
   6.95000   6.63200   2.84000  ###ignore###
Generated by trjconv : graphene in water t=   0.50000  ###ignore###
 4014   ###ignore###
 1729SOL     OW    1   3.082   2.163   1.664  0.3748  0.3087 -0.4980
 1729SOL    HW1    2   3.123   2.079   1.699 -1.0283 -0.0863  0.2113
 1729SOL    HW2    3   3.145   2.239   1.679  1.3255 -0.4782 -0.4386
 3065SOL    HW2 4011   0.097   1.603   1.739  3.0982  2.0249 -0.5412
 3066SOL     OW 4012   2.134   1.182   1.096 -0.2602 -0.4156 -0.4006
 3066SOL    HW1 4013   2.203   1.249   1.067 -0.1512 -1.6699 -3.1684
 3066SOL    HW2 4014   2.056   1.230   1.136  0.8463  1.1988 -0.1258
   6.95000   6.63200   2.84000 ###ignore###"""

# old solution:
# qframes = [(np.genfromtxt(file_name, 
#                           skip_header=2+line_count*frame_index+3*frame_index, 
#                           max_rows = line_count, 
#                           converters={1:lambda s: (-2  if (str(s, "UTF-8").startswith("O")) else 1)}, 
#                           usecols = np.r_[1,4,6]), frame_index) for frame_index in range(frame_count)]

def chunk(txt, prefix):
    """
    Partition an iterable of lines `txt` into lists separated by lines 
    beginning with `prefix` 
    """
    buf = []
    for line in txt:
        if line.lower().startswith(prefix) and buf:
            yield buf
            buf = [line]
        else:
            buf.append(line)
    yield buf

lookup = {'OW': -2.0,
          'default': 1.0}

def parse_step(frametxt):
    """
    Turn each frame into an ndarray by selecting the 3 columns we care about
    and munging the second column according to `lookup`
    """
    return np.genfromtxt(frametxt, usecols=[1,4,6],
            skip_header=2, 
            skip_footer=1, 
            converters={1: lambda k: lookup.get(k, lookup['default'])}) 

with open('testdata2.txt', 'r') as f:
    steptxt = chunk(f, prefix='generated')
    start = time.time()
    stepdata = [parse_step(step) for step in steptxt]
    end = time.time()
    print('Parsing took {:.3e} sec using genfromtxt() with `converters`'.format(end-start))
    print(stepdata)

NUMFIELDS = 9

def chunk_and_munge(txt, prefix):
    """
    Partition an iterable of lines `txt` into lists separated by lines 
    beginning with `prefix` 
    """
    buf = []
    for line in txt:
        if line.lower().startswith(prefix) and buf:
            yield buf
            buf = [line]
        else:
            # mutating this in Python as we load is probably must faster
            parts = line.split()
            if len(parts) == NUMFIELDS: # is this a field we want to munge?
                parts[1] = str(lookup.get(parts[2], lookup['default']))
            buf.append(' '.join(parts))
    yield buf


with open('testdata2.txt', 'r') as f:
    steptxt = chunk_and_munge(f, prefix='generated')
    start = time.time()
    stepdata = [parse_step(step) for step in steptxt]
    end = time.time()
    print('Parsing took {:.3e} sec using genfromtxt() with preliminary munging in Python'.format(end-start))
    print(stepdata)
