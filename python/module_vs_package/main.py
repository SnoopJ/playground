import mymod

import pkg
import pkg.subpkg
import pkg.submod


def describe_module(mod):
    module_name = mod.__name__
    print(f"{module_name}.__name__ = {module_name}")
    if hasattr(mod, "__path__"):
        print(f"{module_name} is a package, {module_name}.__path__ = {mod.__path__}")
    else:
        print(f"{module_name} is NOT a package")

    print(f"{module_name}.data = {mod.data}")
    print("\n---\n")


describe_module(mymod)
describe_module(pkg)
describe_module(pkg.submod)
describe_module(pkg.subpkg)
