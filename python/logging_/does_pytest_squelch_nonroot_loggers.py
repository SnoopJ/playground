import logging
from logging import StreamHandler
import sys

import pytest

rootlogger = logging.getLogger(__name__)
rootlogger.setLevel(logging.INFO)
stdout_handler = StreamHandler(sys.stdout)
rootlogger.addHandler(stdout_handler)

sublogger = rootlogger.getChild("foo")


def func():
    rootlogger.info("ROOT")
    sublogger.info("CHILD")

def test_func():
    func()
