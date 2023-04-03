from collections import ChainMap
import inspect


def dispatch(subcmd, *args, **kwargs):
    frames = inspect.getouterframes(inspect.currentframe())
    caller_frame = frames[-2].frame
    func_name = f"func_{subcmd}"
    try:
        func = ChainMap(caller_frame.f_locals, caller_frame.f_globals)[func_name]
    except LookupError:
        print(f"Lookup failed for {func_name}")
        return False

    func(*args, **kwargs)
    return True
