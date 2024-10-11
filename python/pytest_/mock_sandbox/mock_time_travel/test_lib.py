import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from lib import orchestrate, Something


@pytest.fixture
def FakeSomething():
    class _FakeSomething(Something):
        num_calls = 0

        def expensive_func(self) -> str:
            time.sleep(1)
            self.__class__.num_calls += 1
            return "FAKE expensive() done"

    yield _FakeSomething


def test_orchestrate(FakeSomething):
    ref_time = datetime.now()
    expensive_dt = timedelta(hours=1)

    def mock_now():
        """
        Fake now() in terms of how many calls we've made to expensive()
        """
        # time actually elapsed
        # i.e. including time we spent in cheap_func()
        rel_dt = datetime.now() - ref_time

        return ref_time + rel_dt + FakeSomething.num_calls * expensive_dt

    with (
        patch("lib.Something", FakeSomething),
        patch("datetime.datetime", now=mock_now)
    ):
        max_time = timedelta(hours=3)
        n_iter = 10
        orchestrate(Niter=n_iter, max_time=max_time)


    stop = datetime.now()
    assert stop - ref_time <= max_time, "Time budget exceeded"

    assert FakeSomething.num_calls < (n_iter//2), "expensive_func() called more than expected"
