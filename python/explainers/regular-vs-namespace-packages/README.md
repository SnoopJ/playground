This sample attempts to demonstrate the difference between "regular" packages
(ones defined by the presence of an `__init__.py`) and "namespace" packages.

If you want the long and kinda-technical story on the distinction, you can read
the [official import system documentation](https://docs.python.org/3/reference/import.html#packages)
and/or [PEP 420](https://peps.python.org/pep-0420/), but I wrote this thinking
that it may help demonstrate some of the differences.

Brief summary:

* Namespace packages only let you do/define useful things in subpackages  
* Regular packages have `__init__.py` which is a natural place to do/define "top-level" stuff

### Sample output

```
$ python3 demo.py
Importing nspkg
-----

nspkg summary
-----
nspkg does NOT define toplevel
nspkg does NOT define x
nspkg does NOT define y

===

Importing regpkg
-----
executing regpkg/__init__.py (this module is called regpkg)
executing regpkg/subpkg.py (this module is called regpkg.subpkg)

regpkg summary
-----
regpkg.toplevel = "A value that lives at the top level of this 'regular' package"
regpkg.x = 42
regpkg does NOT define y

===

Importing nspkg.subpkg
-----
executing nspkg/subpkg.py (this module is called nspkg.subpkg)

nspkg.subpkg summary
-----
nspkg.subpkg does NOT define toplevel
nspkg.subpkg.x = -1
nspkg.subpkg.y = 'Aineko'

===

Importing regpkg.subpkg
-----

regpkg.subpkg summary
-----
regpkg.subpkg does NOT define toplevel
regpkg.subpkg.x = 42
regpkg.subpkg.y = 'Manny'

===

```
