import inspect


def summarize(module):
    """Prints out a summary of the given module"""
    name = module.__name__

    print(f"\n{name} summary\n-----")

    for var_name in ("toplevel", "x", "y"):
        if hasattr(module, var_name):
            print(f"{name}.{var_name} = {getattr(module, var_name)!r}")
        else:
            print(f"{name} does NOT define {var_name}")

    print("\n===\n")


print("Importing nspkg\n-----")
import nspkg
summarize(nspkg)

print("Importing regpkg\n-----")
import regpkg
summarize(regpkg)

print("Importing nspkg.subpkg\n-----")
import nspkg.subpkg
summarize(nspkg.subpkg)

print("Importing regpkg.subpkg\n-----")
import regpkg.subpkg
summarize(regpkg.subpkg)
