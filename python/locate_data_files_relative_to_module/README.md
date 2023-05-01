This example shows off a
[`pathlib`](https://docs.python.org/3/library/pathlib.html) "pre-amble" that I
often add to my Python modules when I want to locate other files relative to
the module.

### Sample output

```
$ python3 program.py
Contents of foo.txt:
This is the text inside of foo.txt!

Contents of bar.txt:
This is the text inside of bar.txt!
```

### Cautionary note

The `__file__` module attribute is not always defined (it will
necessarily not be defined for modules written in C, etc.), and even when
it _is_ defined, the file it points to may not be a `.py` file (e.g. if
you are running a Python program [from inside of a ZIP file](https://docs.python.org/3/library/zipapp.html)).
However, the solution given here works for many use-cases. If you want to load
"resource" data from a package in a way that works for more edge cases, check
out the documentation for the [`importlib.resources` module](https://docs.python.org/3/library/importlib.resources.html).
