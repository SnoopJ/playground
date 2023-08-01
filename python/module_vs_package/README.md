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
running `import mymod`
Imported module mymod defined by file /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/mymod.py
mymod is NOT a package
mymod.data = 42

---

running `import pkg`
Imported module pkg defined by file /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg/__init__.py
pkg is a package, pkg.__path__ = ['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg']
pkg.data = 42

---

running `import pkg.submod`
Imported module pkg.submod defined by file /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg/submod.py
pkg.submod is NOT a package
pkg.submod.data = -1

---

running `import pkg.subpkg`
Imported module pkg.subpkg defined by file /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg/subpkg/__init__.py
pkg.subpkg is a package, pkg.subpkg.__path__ = ['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/module_vs_package/pkg/subpkg']
pkg.subpkg.data = 1337

---

```
