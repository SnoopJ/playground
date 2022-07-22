# Arbitrary program that calls into some of the standard library to illustrate
# how the tracer is able to find call stacks that pass through the target module
from pathlib import Path
import multiprocessing

from trace import who_is_calling


HERE = Path(__file__).parent.resolve()


def myfunc(pth: Path):
    return other(pth)


def other(pth: Path):
    return [p.name for p in pth.glob("**/*")]


TARGET_MODULES = {"__main__", "pathlib", "os", "multiprocessing"}

def _worker():
    # Example of how this tracer can be applied to a subprocess as well
    with who_is_calling(*TARGET_MODULES, outfile="trace_child.txt"):
        print("Hello world!")
        print(f"Calling other() from subprocess: {other(HERE)}")


with who_is_calling(*TARGET_MODULES, outfile="trace_parent.txt"):
    DUMMY_DIR = HERE.joinpath("dummy")
    DUMMY_DIR.mkdir(exist_ok=True)

    pth = DUMMY_DIR.joinpath("somefile.txt")
    pth.write_text("Note: this write calls some stuff in os, but none of it is written in Python, so it won't be traced!")

    proc = multiprocessing.Process(target=_worker)
    proc.start()
    proc.join()

    myfunc(pth)
