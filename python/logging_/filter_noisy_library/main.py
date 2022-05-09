import logging

from somelib import func


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def example():
    # Calling this function will produce either one or two logger messages,
    # depending on whether or not the filter defined below is installed
    logger.info("This is a nice message from main.py, I want it to be output")
    func()
    print()


print("First example: expect two messages\n---")
example()


def myfilter(record):
    # https://docs.python.org/3/library/logging.html#filter-objects
    if record.name.startswith("somelib"):
        return False
    else:
        return True


# NOTE: I find this a little confusing because it seems the filter should be
# added to the handler(s) in question, NOT the Logger instances
logging.root.handlers[0].addFilter(myfilter)

print("Second example: expect one message\n---")
example()


# output:
# $ python3 main.py
# First example: expect two messages
# ---
# INFO:__main__:This is a nice message from main.py, I want it to be output
# DEBUG:somelib.pkg:This is a noisy log message from somelib.pkg, I want it filtered out
#
# Second example: expect one message
# ---
# INFO:__main__:This is a nice message from main.py, I want it to be output
