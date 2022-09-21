"""
Sample program based on a question in #python on Libera.chat, 20 Sept 2022
about collating statistics about a collection of datetime objects

NOTE: this sample requires Python 3.10 or higher because of the use of 
itertools.pairwise()
"""
import itertools
from datetime import datetime, date, timedelta
import random
import statistics


class DatetimeCollection:
    def __init__(self, datetimes: list[datetime]):
        self.datetimes = datetimes

    def __repr__(self):
        sep = "\n  "
        dts_repr = sep.join(repr(dt) for dt in self.datetimes)
        return f"{self.__class__.__name__}({sep}{dts_repr}\n)"

    def mean_gap(self):
        """
        Compute the average 'gap' between consecutive datetimes
        """
        N = len(self.datetimes)
        diffs_sec = (abs(dt2-dt1).total_seconds() for dt1, dt2 in itertools.pairwise(self.datetimes))
        mean_sec = statistics.mean(diffs_sec)
        return timedelta(seconds=mean_sec)

    def latest(self):
        return max(self.datetimes, key=datetime.timestamp)

    def earliest(self):
        return min(self.datetimes, key=datetime.timestamp)

    def max_date(self):
        return self.latest().date()

    def min_date(self):
        return self.earliest().date()


random.seed(42)  # reproducibility

def _random_datetime():
    return datetime(
        year=2022,
        month=9,
        day=random.randint(1, 30),
        hour=random.randint(0, 23),
        second=random.randint(0, 60),
    )


dtc = DatetimeCollection([_random_datetime() for _ in range(4)])
print(f"{dtc = }")
print(f"{dtc.earliest() = }")
print(f"{dtc.latest() = }")
print(f"{dtc.min_date() = }")
print(f"{dtc.max_date() = }")
print(f"{dtc.mean_gap() = }")

# ---
#
# $ python3.10 datetimestatistics.py
# dtc = DatetimeCollection(
#   datetime.datetime(2022, 9, 21, 3, 0, 1)
#   datetime.datetime(2022, 9, 24, 8, 0, 15)
#   datetime.datetime(2022, 9, 8, 4, 0, 47)
#   datetime.datetime(2022, 9, 4, 21, 0, 47)
# )
# dtc.earliest() = datetime.datetime(2022, 9, 4, 21, 0, 47)
# dtc.latest() = datetime.datetime(2022, 9, 24, 8, 0, 15)
# dtc.min_date() = datetime.date(2022, 9, 4)
# dtc.max_date() = datetime.date(2022, 9, 24)
# dtc.mean_gap() = datetime.timedelta(days=7, seconds=47994)

