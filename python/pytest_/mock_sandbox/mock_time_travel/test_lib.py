import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from lib import orchestrate


class MockExpensive:
    def __init__(self):
        self.numcalls = 0

    def __call__(self) -> str:
        time.sleep(1)
        self.numcalls += 1
        return "fake expensive() return"


def test_orchestrate():
    mock_exp = MockExpensive()

    ref_time = datetime.now()
    expensive_dt = timedelta(hours=1)

    def mock_now():
        """
        Fake now() in terms of how many calls we've made to expensive()
        """
        # time actually elapsed
        # i.e. including time we spent in cheap_func()
        rel_dt = datetime.now() - ref_time

        return ref_time + rel_dt + mock_exp.numcalls * expensive_dt

    mock_datetime = Mock(now=mock_now)

    with (
        patch("lib.expensive_func", mock_exp),
        patch("datetime.datetime", mock_datetime)
    ):
        max_time = timedelta(hours=3)
        n_iter = 10
        orchestrate(Niter=n_iter, max_time=max_time)


    stop = datetime.now()
    assert stop - ref_time <= max_time, "Time budget exceeded"

    assert mock_exp.numcalls < (n_iter//2), "expensive_func() called more than expected"
