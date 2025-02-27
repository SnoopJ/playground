An example showing off the functionality of [zipimport] to load and execute Python
modules from ZIP files, both implicitly by injecting the `.zip` file into `sys.path`
and explicitly by manually driving the import system.

[zipimport]: https://docs.python.org/3/library/zipimport.html

```
$ python3 main.py
> Attempting to import otherlib
> Failed
> Inserting otherlib.zip to sys.path
> Importing otherlib
> Succeeded
> Running otherlib.bark()
Bark bark! I'm otherlib running from __file__ = 'otherlib.zip/otherlib.py'

$ python3 manual_main.py
> Source listing of module otherlib from otherlib.zip
```python
    def bark():
        print(f"Bark bark! I'm otherlib running from {__file__ = }")
```
> Importing otherlib
> Running otherlib.bark()
Bark bark! I'm otherlib running from __file__ = 'otherlib.zip/otherlib.py'
```
