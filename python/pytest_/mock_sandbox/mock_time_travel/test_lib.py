import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from lib import orchestrate, Something


@pytest.fixture
def FakeSomething():
    class _FakeSomething(Something):
        ref_time = datetime.now()
        expensive_dt = timedelta(hours=1)
        num_calls = 0

        def expensive_func(self) -> str:
            time.sleep(1)
            self.__class__.num_calls += 1
            return "FAKE expensive() done"

        @classmethod
        def now(cls):
            rel_dt = datetime.now() - cls.ref_time

            return cls.ref_time + rel_dt + cls.num_calls * cls.expensive_dt


    yield _FakeSomething


def test_orchestrate(FakeSomething):
    with (
        patch("lib.Something", FakeSomething),
        patch("datetime.datetime", now=FakeSomething.now)
    ):
        max_time = timedelta(hours=3)
        n_iter = 10
        orchestrate(Niter=n_iter, max_time=max_time)


    stop = datetime.now()
    assert stop - FakeSomething.ref_time <= max_time, "Time budget exceeded"

    assert FakeSomething.num_calls <= (n_iter//2), "expensive_func() called more than expected"
