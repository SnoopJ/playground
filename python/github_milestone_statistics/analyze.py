import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint
from typing import Iterable, Optional

import dateutil.parser

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator, date2num


HERE = Path(__file__).parent


@dataclass
class Entry:
    """Representation of a GitHub issue or PR"""
    number: int
    title: str
    milestones: dict[str, datetime]
    created_at: datetime
    closed_at: Optional[datetime] = None

    @classmethod
    def from_graphql(cls, **datum):
        createdAt_raw = datum.pop("createdAt")
        created_at = dateutil.parser.isoparse(createdAt_raw)

        closedAt_raw = datum.pop("closedAt")
        if closedAt_raw is not None:
            closed_at = dateutil.parser.isoparse(closedAt_raw)
        else:
            closed_at = None

        milestone_events_raw = datum.pop("timelineItems")["nodes"]
        milestones = {}
        for evt in milestone_events_raw:
            milestones[evt["milestoneTitle"]] = dateutil.parser.isoparse(evt["createdAt"])

        return cls(milestones=milestones, created_at=created_at, closed_at=closed_at, **datum)

    def is_open_at(self, t: datetime) -> bool:
        if self.created_at > t or not self.closed_at:
            return False

        if self.closed_at < t:
            return False
        else:
            return True


def show_entries(entries: list[Entry]):
    for ent in entries:
        ass_info = f"assigned: {ent.milestones['8.0.0']}"
        close_info = f", closed: {ent.closed_at}" if ent.closed_at else ""
        ent_info = f"{ass_info}{close_info}"
        print(f"#{ent.number:<4} — {ent.title:<80}  ({ent_info})")


def plot_entries(entries: list[Entry]):
    delta = timedelta(days=7)

    dates, num_open, num_closed = zip(*_points(entries, delta))

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Sopel 8.0.0 over time")

    axes[0].plot(dates, num_open, 'rx-')
    axes[0].grid(True, axis='y')
    axes[0].set_title("Open issues/PRs")
    axes[0].xaxis.set_minor_locator(MonthLocator())
    axes[0].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    for label in axes[0].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

    axes[1].plot(dates, num_closed, 'bx-')
    axes[1].grid(True, axis='y')
    axes[1].set_title("Closed issues/PRs")
    axes[1].xaxis.set_minor_locator(MonthLocator())
    axes[1].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    for label in axes[1].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')

    plt.tight_layout()
    plt.savefig('out.png')

    print("Output saved to 'out.png'")


def _points(entries: list[Entry], delta: timedelta) -> Iterable[tuple[float, int, int]]:
    """
    Create a series of `(timestamp, num_open, num_closed)` tuples, spanning the
    range of the given `entries` and spaced out by `delta`

    For each time-point in this range, count up the number of open/closed issues
    that are associated with the 8.0.0 milestone. Issues/PRs are *not* counted
    when they are re-assigned to another milestone (and I have assumes that
    issues are moved into the 8.0.0 milestone only once).
    """
    start = entries[0].milestones["8.0.0"]
    stop = entries[-1].milestones["8.0.0"]
    cur = start - delta

    while (cur := cur + delta) < stop:
        num_open = 0
        num_closed = 0
        for ent in entries:
            if ent.created_at > cur:
                # item doesn't exist yet
                continue

            assigned = ent.milestones["8.0.0"]

            if assigned > cur:
                # item hasn't been assigned to this milestone yet
                continue
            elif len(ent.milestones) > 1:
                other_ms = [(key, ms) for key, ms in ent.milestones.items() if key != "8.0.0"]
                if any(ms >= cur for key, ms in other_ms):
                    # this was reassigned to some other milestone
                    continue

            # otherwise this is in the 8.0.0 milestone at this date
            if ent.is_open_at(cur):
                num_open += 1
            else:
                num_closed += 1

        yield date2num(cur), num_open, num_closed


def main():
    DATA_FN = HERE.joinpath("sopel_milestone_data.json")

    with open(DATA_FN, "r") as f:
        data = json.load(f)

    milestone = data["data"]["repository"]["milestones"]["nodes"][0]
    issues = milestone["issues"]["nodes"]
    prs = milestone["pullRequests"]["nodes"]
    entries = [Entry.from_graphql(**args) for args in (*issues, *prs)]
    entries.sort(key=lambda ent: ent.milestones["8.0.0"])

    plot_entries(entries)


if __name__ == "__main__":
    main()
