This sample shows off how to determine what parts of a program are running `import <something>` (where the example
`<something>` is `numpy`), using two different approaches:

* Installing an [audit hook](https://docs.python.org/3/library/sys.html#sys.addaudithook) for the `import` event
* Patching `builtins.__import__`

```
$ python3 target_program.py
Patched __import__:     numpy imported at /tmp/whats-importing-that-module/target_program.py:8
Audit hook:     numpy imported at /tmp/whats-importing-that-module/target_program.py:8
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/dtypes.py:69
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/_dtype.py:6
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/numeric.py:9
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/fromnumeric.py:8
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/arrayprint.py:33
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/defchararray.py:28
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/memmap.py:3
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/function_base.py:6
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/core/_dtype_ctypes.py:29
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/index_tricks.py:6
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/stride_tricks.py:8
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/_typing/_scalars.py:3
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/_typing/_dtype_like.py:12
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/_typing/_array_like.py:7
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/function_base.py:8
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/histograms.py:9
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/nanfunctions.py:25
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/utils.py:13
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/arraysetops.py:19
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/npyio.py:12
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/format.py:164
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/_iotools.py:6
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/lib/arraypad.py:6
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/polynomial.py:82
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/polyutils.py:33
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/_polybase.py:13
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/chebyshev.py:110
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/legendre.py:82
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/hermite.py:78
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/hermite_e.py:78
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/polynomial/laguerre.py:78
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ctypeslib.py:56
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/core.py:31
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/core.py:35
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/core.py:36
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/core.py:41
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/core.py:2820
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/extras.py:33
Patched __import__:     numpy imported at /home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/numpy/ma/extras.py:34
Patched __import__:     numpy imported at /tmp/whats-importing-that-module/helper.py:1

$ python3 target_program.py | grep -v "site-packages"  # filter out numpy importing itself, notice that the audit hook doesn't find the helper
Patched __import__:     numpy imported at /tmp/whats-importing-that-module/target_program.py:8
Audit hook:     numpy imported at /tmp/whats-importing-that-module/target_program.py:8
Patched __import__:     numpy imported at /tmp/whats-importing-that-module/helper.py:1
```
