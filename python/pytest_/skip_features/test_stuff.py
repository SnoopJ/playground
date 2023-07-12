import pytest


@pytest.fixture
def need_foo(request):
    if request.config.getoption("--skip-foo"):
        pytest.skip(reason="Skipping foo was requested")
    # do whatever else the fixture requires


@pytest.fixture
def need_bar(request):
    if request.config.getoption("--skip-bar"):
        pytest.skip(reason="Skipping bar was requested")
    # do whatever else the fixture requires


def test_foo(need_foo): ...
def test_bar(need_bar): ...
def test_foo_bar(need_foo, need_bar): ...
def test_other_stuff(): ...
