from unittest.mock import Mock, call, patch

import pytest

from main import good_run, bad_run


def _mock_call_names(mock: Mock):
    return [kall[0] for kall in mock.mock_calls]


@pytest.fixture
def main_mock():
    main_mock = Mock()
    with patch.multiple("main", funcA=main_mock.funcA, funcB=main_mock.funcB, funcC=main_mock.funcC):
        yield main_mock


def test_good_run(main_mock):
    good_run()
    # NOTE:_Call objects are tuples of the form (funcname, args, kwargs) so here we can express that
    # we care only about the order of calls (and not the arguments) by extracting the names
    assert _mock_call_names(main_mock) == ["funcA", "funcB", "funcC"]


@pytest.mark.xfail
def test_bad_run(main_mock):
    bad_run()
    assert _mock_call_names(main_mock) == ["funcA", "funcB", "funcC"]
