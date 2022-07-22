from contextlib import contextmanager
import sys
import traceback


@contextmanager
def who_is_calling(*modules: str, outfile: str = "trace.txt") -> dict:
    # e.g. who_is_calling("pathlib", "os")
    modules = set(modules)
    records = []

    def _trace(frame, event, arg):
        if event == "call":
            ns = frame.f_globals
            qualname = ns.get("__name__", "<UNKNOWN>")
            name, _, *rest = qualname.partition(".")

            if name in modules:
                [(filename, lineno, funcname, text)] = traceback.extract_stack(frame, limit=1)
                records.append(f"{qualname}:{funcname}(L{lineno}) — {text}")

        sys.settrace(_trace)

    # begin tracing
    sys.settrace(_trace)

    # execute the block this context manager is managing
    yield

    # wrapped block has ended, write out the results
    with open(outfile, "w") as f:
        f.write(f"### Calls to {modules=} in order\n#\n")
        f.write("\n".join(records))
