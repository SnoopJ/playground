import argparse
import atexit
import profile

from profiler_target import main as target_main


parser = argparse.ArgumentParser()
parser.add_argument('--outfile', type=str, default="out.prof")


def main():
    args = parser.parse_args()
    pr = profile.Profile()

    def _dump():
        pr.dump_stats(args.outfile)

    atexit.register(_dump)

    pr.runctx("target_main()", globals=globals(), locals=globals())
    _dump()
    atexit.unregister(_dump)


if __name__ == "__main__":
    main()
