This is an example of how to locate data files when running a PyInstaller
distribution in `--onefile` mode, which extracts the distribution's contents to
a temporary location on startup. Both approaches shown here are explained
[in the PyInstaller docs](https://pyinstaller.org/en/stable/runtime-information.html)

```
$ python3 -m PyInstaller --clean --noconfirm --onefile app.py --add-data data.txt:.
233 INFO: PyInstaller: 5.13.0
234 INFO: Python: 3.9.16
238 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
... snip ...
16973 INFO: Building EXE from EXE-00.toc completed successfully.
$ ./dist/app
Hello world!
Running from sys._MEIPASS = '/tmp/_MEIvqQW4Q' (HERE = PosixPath('/tmp/_MEIvqQW4Q'))
Running open(Path(HERE, 'data.txt'), 'r')
Read data: 'this is some ancillary data\n'
Running open(Path(sys._MEIPASS, 'data.txt'), 'r')
Read data: 'this is some ancillary data\n'
```
