This sample attempts to demonstrate the difference between a Python _module_
and a Python _package_.


A [_module_](https://docs.python.org/3/glossary.html#term-module) is a 'box'
that holds Python code. The most common way to create a module is a plain old
`.py` file.


A [_package_](https://docs.python.org/3/glossary.html#term-package) is a
**special kind** of module that may contain other modules or packages. The most
common way to create a package is to create a directory containing an
`__init__.py`, which is a special filename recognized by the interpreter.
Continuing the 'box' analogy, you can think of a package as a box that might
hold other boxes.


## Example output

```
$ python3 main.py
mymod.__name__ = mymod
mymod is NOT a package
mymod.data = 42

---

pkg.__name__ = pkg
pkg is a package, pkg.__path__ = ['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg']
pkg.data = 42

---

pkg.submod.__name__ = pkg.submod
pkg.submod is NOT a package
pkg.submod.data = -1

---

pkg.subpkg.__name__ = pkg.subpkg
pkg.subpkg is a package, pkg.subpkg.__path__ = ['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg/subpkg']
pkg.subpkg.data = 1337

---

```
