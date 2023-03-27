from contextlib import contextmanager
import inspect


@contextmanager
def name_binder(**kwargs):
    frames = inspect.getouterframes(inspect.currentframe())
    target_frame = frames[-1]
    target_globals = target_frame.frame.f_globals
    oldvals = {}

    for key, val in kwargs.items():
        if key in target_globals:
            old_val = target_globals[key]
            print(f"Storing current value of {key=} ({old_val=})")
            oldvals[key] = old_val

        print(f"Storing new value of {key=} ({val=})")
        target_globals[key] = val

    yield

    for key in kwargs.keys():
        if key in oldvals:
            print(f"Restoring previous value of {key=}")
            target_globals[key] = oldvals[key]
        else:
            print(f"Unbinding {key=}")
            target_globals.pop(key)


x = 42
print(x)

with name_binder(x=-1, y=-1):
    print(f"{x = }")
    print(f"{y = }")

print(x)
print(y)  # NameError
