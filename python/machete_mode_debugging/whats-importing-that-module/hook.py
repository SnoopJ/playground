import builtins
import inspect
import sys
from pprint import pprint


TARGET_MODULE = "numpy"


def _line_info(offset):
    stack = inspect.stack()
    target_frame = stack[offset+1]
    fn = target_frame.filename
    lineno = target_frame.lineno

    return fn, lineno


def audit_numpy_import(event, args):
    # NOTE: this audit event only fires when the module is being found/loaded!
    if event != "import":
        return

    module, filename, syspath, sysmeta_path, syspath_hooks = args
    if module == TARGET_MODULE:
        # offset 0 is *this* frame, offset 1 is our patched __import__(), offset 2 is where the import actually happened
        fn, lineno = _line_info(offset=2)
        print(f"Audit hook:\t{TARGET_MODULE} imported at {fn}:{lineno}")


_original___import__ = builtins.__import__
def _patched_import(name, *args, **kwargs):
    if name == TARGET_MODULE:
        # offset 0 is *this* frame, offset 1 is where the import actually happened
        fn, lineno = _line_info(offset=1)

        # suppress importlib frames
        if not fn.startswith("<frozen importlib"):
            print(f"Patched __import__:\t{TARGET_MODULE} imported at {fn}:{lineno}")

    return _original___import__(name, *args, **kwargs)


def install():
    sys.addaudithook(audit_numpy_import)
    builtins.__import__ = _patched_import
