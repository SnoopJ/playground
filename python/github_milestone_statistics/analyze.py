import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint
from typing import Iterable, Optional

import dateutil.parser
from packaging.version import Version

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
        if self.created_at > t:
            return False

        if self.closed_at and self.closed_at < t:
            return False
        else:
            # item is either never closed, or not yet closed; either way, it's open
            return True


def plot_entries(entries_by_milestone: dict[str, list[Entry]]):
    delta = timedelta(days=7)

    plottable_data = []
    for idx, (milestone, entries) in enumerate(entries_by_milestone.items()):
        if not entries:
            print(f"milestone #{idx} ({milestone!r}) has no entries")
            continue

        print(f"handling milestone #{idx}: {milestone}")

        pts = list(_points(entries, milestone, delta))
        if not pts:
            print(f"milestone #{idx} ({milestone!r}) has no points (?)")
            continue
        elif len(pts) < 10:
            print(f"milestone #{idx} ({milestone!r}) does not have more than 10 points, omitting")
            continue

        plottable_data.append((milestone, *zip(*pts)))


    W = 2
    H = len(plottable_data)
    fig, axes = plt.subplots(H, W, figsize=(16, 6*H))
    axes = axes.squeeze()
    fig.suptitle("Sopel over time", x=0.53, y=0.995)

    for idx, (milestone, dates, num_open, num_closed) in enumerate(plottable_data):
        axes[idx, 0].plot(dates, num_open, 'rx-')
        axes[idx, 0].grid(True, axis='y')
        axes[idx, 0].set_title(f"Open issues/PRs ({milestone} milestone)")
        axes[idx, 0].xaxis.set_minor_locator(MonthLocator())
        axes[idx, 0].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        for label in axes[idx, 0].get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right')

        axes[idx, 1].plot(dates, num_closed, 'bx-')
        axes[idx, 1].grid(True, axis='y')
        axes[idx, 1].set_title(f"Closed issues/PRs ({milestone} milestone)")
        axes[idx, 1].xaxis.set_minor_locator(MonthLocator())
        axes[idx, 1].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        for label in axes[idx, 1].get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right')

    plt.tight_layout()
    plt.savefig('out.png')

    print("Output saved to 'out.png'")


def _points(entries: list[Entry], milestone: str, delta: timedelta) -> Iterable[tuple[float, int, int]]:
    """
    Create a series of `(timestamp, num_open, num_closed)` tuples, spanning the
    range of the given `entries` and spaced out by `delta`

    For each time-point in this range, count up the number of open/closed issues
    that are associated with the `milestone`. Issues/PRs are *not* counted
    when they are re-assigned to another milestone (and I have assumes that
    issues are moved into a milestone only once).
    """
    start = entries[0].milestones[milestone]
    stop = entries[-1].milestones[milestone]
    cur = start - delta

    while (cur := cur + delta) < stop:
        num_open = 0
        num_closed = 0
        for ent in entries:
            if ent.created_at > cur:
                # item doesn't exist yet
                continue

            assigned = ent.milestones[milestone]

            if assigned > cur:
                # item hasn't been assigned to this milestone yet
                continue
            elif len(ent.milestones) > 1:
                other_ms = [(key, ms) for key, ms in ent.milestones.items() if key != milestone]
                if any(ms >= cur for key, ms in other_ms):
                    # this was reassigned to some other milestone
                    continue

            # otherwise this is in the milestone at this date
            if ent.is_open_at(cur):
                num_open += 1
            else:
                num_closed += 1

        yield date2num(cur), num_open, num_closed


def main():
    DATA_FN = HERE.joinpath("sopel_milestone_data.json")

    with open(DATA_FN, "r") as f:
        milestones = json.load(f)
        milestones.sort(key=lambda ms: Version(ms['title']))

    entries_by_milestone = {}
    for ms in milestones:
        title = ms["title"]
        if Version(title) >= Version("6.0.0"):
            print(f"Processing milestone {title!r}")
        else:
            print(f"Skipping milestone {title!r}")
            continue
        issues = ms["issues"]["nodes"]
        prs = ms["pullRequests"]["nodes"]
        entries = [Entry.from_graphql(**args) for args in (*issues, *prs)]
        entries.sort(key=lambda ent: ent.milestones.get(title, datetime(year=2112, month=7, day=20)).timestamp())

        entries_by_milestone[title] = entries

    plot_entries(entries_by_milestone)


if __name__ == "__main__":
    main()
