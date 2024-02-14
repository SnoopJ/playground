import argparse
import sys

import pytest


if sys.version_info >= (3, 9):
    # NOTE: requires Python 3.9+, but provides --no-<option> as well
    BOOLEAN_ACTION = argparse.BooleanOptionalAction
else:
    # NOTE: works in Python 3.8 and prior, but does not provide --no-<option>
    BOOLEAN_ACTION = "store_true"


def pytest_addoption(parser):
    parser.addoption(
        "--run-slow",
        action=BOOLEAN_ACTION,
        default=False,
        help="Run slow tests",
    )
    parser.addoption(
        "--reorder-slow",
        action=BOOLEAN_ACTION,
        default=False,
        help="Order slow tests last",
    )


def pytest_collection_modifyitems(config, items):
    skipper = pytest.mark.skip(reason="Test is marked slow and --run-slow was not given")
    pops = []
    for idx, item in enumerate(items):
        if "slow" in item.keywords:
            pops.append(idx)

            if not config.getoption("--run-slow"):
                item.add_marker(skipper)

    if config.getoption("--reorder-slow"):
        reordered = []
        for idx in reversed(pops):
            reordered.append(items.pop(idx))
        items.extend(reversed(reordered))
