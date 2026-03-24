import inspect
import logging
import sys

from other import do_something


LOGGER = logging.getLogger(__name__)
LOGFMT = "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s(+L%(lineno)d): %(message)s"


def subprocess_audithook(name, hookargs) -> None:
    if name != "subprocess.Popen":
        return
    executable, args, cwd, env = hookargs

    # the calling frame is definitely in subprocess, and the target frame is the next non-subprocess frame above that
    frames = (frameinfo.frame for frameinfo in inspect.stack()[1:])
    # ASSUME: there is such a calling frame (i.e. this next() will not raise StopIteration)
    offset, target_frame = next((n, f) for n, f in enumerate(frames, 1) if f.f_globals.get("__name__", "<UNKNOWN>") != "subprocess")
    # NOTE: having identified the target_frame we *could* perform additional introspection to e.g. only log subprocess
    # usage by particular target modules, but that would further complicate this hook, so I'm just noting it as a possibility :)

    LOGGER.debug("running subprocess with args: %r\n\tenv = %r", args, env, stacklevel=1+offset)


# Install the hook we just defined
# https://docs.python.org/3/library/sys.html#sys.addaudithook
sys.addaudithook(subprocess_audithook)


def main():
    if "-v" in sys.argv:
        lvl = logging.DEBUG
    else:
        lvl = logging.INFO
    logging.basicConfig(level=lvl, format=LOGFMT)

    data = do_something()
    print(f"And the result is: {data = }")


if __name__ == "__main__":
    main()
