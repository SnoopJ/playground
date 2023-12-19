import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run slow tests",
    )
    parser.addoption(
        "--reorder-slow",
        action="store_true",
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
