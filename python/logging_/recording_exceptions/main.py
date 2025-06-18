import argparse
import logging
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--exc-info", action="store_true")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def failing_function():
    raise RuntimeError("Something went wrong")


def main(args):
    logger.info("A regular old logging message")
    try:
        failing_function()
    except Exception as exc:
        logging.exception("An error occurred exc_info=%r", args.exc_info, exc_info=args.exc_info)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
