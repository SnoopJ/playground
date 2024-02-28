import argparse
import profile
import signal
import sys


parser = argparse.ArgumentParser()
parser.add_argument('--outfile', type=str, default="out.prof")
parser.add_argument('target', type=str)


def main():
    args = parser.parse_args()
    prof = profile.Profile()

    def _dump_on_sigterm(signum, frame):
        # NOTE: the profiler is still running and we must disable it before
        # dumping, or it will recursively try to profile its own machinery
        sys.setprofile(None)
        prof.dump_stats(args.outfile)

        # NOTE: this could simply be a sys.exit(), but this shows how we can
        # invoke a pre-existing handler if one exists. Applications that set
        # their own SIGTERM handler may need additional logic here, depending
        # on what that handler does. The old handler will not appear in the
        # profile, nor will anything that happens afterwards if an existing
        # handler continues program execution.
        signal.signal(signal.SIGTERM, oldhandler)
        signal.raise_signal(signal.SIGTERM)

    oldhandler = signal.signal(signal.SIGTERM, _dump_on_sigterm)

    with open(args.target, "rb") as f:
        src = f.read()
        code = compile(src, args.target, 'exec')

    globs = {
        '__file__': args.target,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }

    prof.runctx(code, globs, None)
    prof.dump_stats(args.outfile)


if __name__ == "__main__":
    main()
