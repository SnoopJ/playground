This is a reproduction of a pretty obscure bug I encountered at the
intersection of [PyInstaller](https://pyinstaller.org/) and the Windows Service
system.

In this code, `pyinstaller_entrypoint.py` wraps behavior defined in
`acmelib.py` into a Windows Service, and also installs a top-level
[excepthook](https://docs.python.org/3/library/sys.html#sys.excepthook) that
logs uncaught exceptions to the log file before passing them on to other
handlers (here, the default top-level handler which prints a traceback and
shuts down Python)

I believe this happens because of a quirk of Windows Services that causes
`sys.stdout, sys.stderr` to be `None`, but I'm not entirely sure what to do
about this basically artificial error that is hiding the error I _do_ want to
see.

### Reproduction steps

On Windows, run:

`python -m pip install -r requirements.txt`  
`python -m PyInstaller --noconfirm pyinstaller_entrypoint.py`  
`.\dist\pyinstaller_entrypoint\pyinstaller_entrypoint.exe install`  
`.\dist\pyinstaller_entrypoint\pyinstaller_entrypoint.exe start`  
`cat .\dist\pyinstaller_entrypoint\acmelib.log`
`.\dist\pyinstaller_entrypoint\pyinstaller_entrypoint.exe remove`  

I was able to reproduce this on Windows 10 with Python 3.7, PyInstaller 5.8.0 (as well as 4.9)

```
DEBUG:acmelib:entrypoint excepthook installed
INFO:acmelib:acmelib.main() beginning
INFO:acmelib:acmelib.main() looping (iteration #0)
INFO:acmelib:acmelib.main() looping (iteration #1)
INFO:acmelib:acmelib.main() looping (iteration #2)
INFO:acmelib:acmelib.main() looping (iteration #3)
INFO:acmelib:acmelib.main() looping (iteration #4)
ERROR:acmelib:Uncaught exception:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: 'NoneType' object has no attribute 'flush'
ERROR:acmelib:Uncaught exception:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: 'NoneType' object has no attribute 'flush'
```
