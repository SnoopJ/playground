"""
  grym was complaining about the speed of Apache MXNet's NDArray.asnumpy(), which
  does a synchronous gather (MXNDArraySyncCopyToCPU()), and it got me wondering about
  whether you could create a "shell" ndarray whose data point elsewhere. It wasn't
  meaningful for his case (because the synchronize would just end up somewhere else), 
  but it was a fruitful way to play with ctypes and the ndarray interface.

  https://github.com/apache/incubator-mxnet/blob/master/python/mxnet/ndarray/ndarray.py#L1959
"""
import numpy as np
import ctypes

def addr(arr):
  """ Get address of numpy array's data """
  return arr.__array_interface__['data'][0]

def summ(arr, header=''):
  """ Summarize the state of an array """
  print(header + f' (0x{addr(arr):x})')
  print(f"{' '.join(str(arr).split())}\n")

dtype = 'i4'
sz = np.nbytes[dtype]
N = 10
origarray = np.random.randint(0, 16, size=N, dtype=dtype)
viewarray = origarray.view()
cparray = origarray.copy()

summ(origarray, 'original array:')
summ(viewarray, 'view over original array:')
summ(cparray, 'copied array:')

print("------------------------")

newdata = (ctypes.c_int32*N)(*range(N))
print(f'new data (c_int32 array, N={N}):\t(0x{ctypes.addressof(newdata):x})')
newarr = np.empty(shape=(N,), dtype=dtype)
summ(newarr, 'new, unitialized array')
newarr.data = newdata
summ(newarr, 'newarr after setting newarr.data')

# frombuffer() is an even more concise way to do this, and it supports offsets!
halfarr = np.frombuffer(newdata, offset=sz*N//2, dtype=dtype)
summ(halfarr, "halfarr")

# of course, possibly silly things like reinterpreting the bytes can be done, too
watarr = np.frombuffer(newdata, dtype='i8')
summ(watarr, "watarr")

newdata[:] = [-1]*N

print("------------after modifying underlying memory------------")
summ(newarr, 'newarr')
summ(halfarr, 'halfarr')
summ(watarr, 'watarr')

newdata[:] = np.random.randint(16**2, size=N)

# we can even do Evil Things™ like memcpy()!
ctypes.memmove(addr(origarray), addr(newarr), origarray.nbytes//2)

print('------------after randomization and memmove()------------')
summ(newarr, 'newarr')
summ(origarray, 'origarray')
summ(viewarray, 'viewarray')
summ(cparray, 'cparray')
