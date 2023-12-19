import time

import pytest


def test_short():
    time.sleep(0.1)


@pytest.mark.slow
def test_long():
    time.sleep(2)


def test_another_short():
    time.sleep(0.1)


@pytest.mark.slow
def test_another_long():
    time.sleep(2)
