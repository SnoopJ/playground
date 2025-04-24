import argparse
import logging

logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument("--use-somelib", action="store_true")
parser.add_argument("-v", dest="verbosity", action="count", default=0)


class FeatureUnavailable(Exception):
    """Raised to indicate that a required feature is not available"""


def main():
    args = parser.parse_args()
    loglevel = logging.INFO - 10*args.verbosity
    logging.basicConfig(level=loglevel)

    # NOTE:deferred import so that the logging hierarchy is configured first
    from . import somelib_facade

    if args.use_somelib and not somelib_facade.SOMELIB_AVAILABLE:
        raise FeatureUnavailable("somelib requested, but not available")

    logger.info("OK")


if __name__ == "__main__":
    main()
