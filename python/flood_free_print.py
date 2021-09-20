"""
Based on a question in Freenode #python on August 6, 2019
"""
from datetime import datetime, timedelta

class FloodFreePrinter():
    """
    Only prints 1 message during any time window of width `delay` (in sec)
    """
    def __init__(self, delay=4):
        self.delay = delay
        self._timestamp = datetime.now() - timedelta(seconds=delay)
        pass

    def print(self, msg):
        timer = (datetime.now() - self._timestamp).seconds >= self.delay
        if (not timer):
            return # we're in a timeout window, eject!
        else: # we're not in the window
            print(msg)
            self._timestamp = datetime.now()


if __name__ == "__main__":
    myprinter = FloodFreePrinter(delay=1)

    for _ in range(1_000_000):
        myprinter.print(f"Hello world! {datetime.now()}")

