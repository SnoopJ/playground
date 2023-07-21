import time

import pytest


def test_short():
    time.sleep(0.1)


@pytest.mark.slow
def test_long():
    time.sleep(2)
