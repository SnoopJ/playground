import importlib


def import_and_describe_module(import_name):
    # NOTE: what's printed here is a bit of a lie, but
    # `importlib.import_module(name)` is the same as `import name` for this
    # program's purposes
    print(f"running `import {import_name}`")
    mod = importlib.import_module(import_name)

    module_name = mod.__name__
    print(f"Imported module {module_name} defined by file {mod.__file__}")

    if hasattr(mod, "__path__"):
        print(f"{module_name} is a package, {module_name}.__path__ = {mod.__path__}")
    else:
        print(f"{module_name} is NOT a package")

    print(f"{module_name}.data = {mod.data}")
    print("\n---\n")


import_and_describe_module("mymod")
import_and_describe_module("pkg")
import_and_describe_module("pkg.submod")
import_and_describe_module("pkg.subpkg")
