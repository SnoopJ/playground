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

class MyFilter(logging.Filter):
    def filter(self, record):
        return record.name.startswith("somelib")


logger.addFilter(MyFilter())

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
