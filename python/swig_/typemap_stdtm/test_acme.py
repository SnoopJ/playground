import datetime

from acme import time_in, time_out


def test_time_in_datetime():
    dt = datetime.datetime.now()
    time_in(dt)


def test_time_in_date():
    dt = datetime.date.today()
    time_in(dt)


def test_time_out():
    dt = time_out()
    assert isinstance(dt, datetime.datetime)
