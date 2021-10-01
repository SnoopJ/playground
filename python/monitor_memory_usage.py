#!/usr/bin/env python3
# pylint: skip-file
import time
from typing import List

import click
import matplotlib

matplotlib.use("agg")
import numpy as np
import psutil
from matplotlib import pyplot as plt


@click.command()
@click.option("--from", "fromfile", type=click.Path(exists=True, dir_okay=False, readable=True), default=None)
@click.option(
    "--pid", type=int, default=None, help="Monitor the given process ID until it terminates (or until interrupted)"
)
@click.option(
    "--sample", type=float, default=1, help="If monitoring a process, the time between usage samples in seconds"
)
@click.option(
    "--update-dt",
    type=float,
    default=-1,
    help="Time between live updates to the plot (negative values disable live plotting)",
)
@click.option("--swap", is_flag=True, help="Include swap")
def main(fromfile, pid, sample, update_dt, swap):
    if fromfile and pid:
        raise ValueError("--from and --pid are mutually exclusive")
    elif fromfile:
        # file should be one column, one usage entry per line
        memdata = np.loadtxt(fromfile)
        assert memdata.ndim == 1
    elif pid:
        times, memdata, swapdata = _monitor_process(pid, sample, update_dt=update_dt)
    else:
        raise ValueError("One of {--from, --pid} is required")

    _plot(times, memdata, swapdata)


def _plot(times, memdata, swapdata=None):
    deltamem = memdata - memdata[0]

    fig = plt.figure()
    plt.plot(times, deltamem / 1e6, "k-", label="memory")
    if swapdata is not None:
        deltaswap = swapdata - swapdata[0]
        plt.plot(times, deltaswap / 1e6, "g--", label="swap")
        plt.legend()
    plt.xlabel("Δt (sec)")
    plt.title(f"memory{'/swap' if swapdata is not None else ''} over time (MB)\n(difference vs. start of profiling)")
    plt.tight_layout()
    plt.savefig("mem.png")
    plt.close(fig)


def _monitor_process(pid, sample_dt=1, update_dt=-1) -> List[np.ndarray]:
    proc = psutil.Process(pid)

    mem = []
    swap = []
    sample_times = []
    start = time.monotonic()
    lastplot = time.monotonic()

    print(f"Monitoring process {pid}...")
    while True:
        try:
            if not proc.is_running():
                break
            else:
                mi = proc.memory_full_info()
                now = time.monotonic()
                timestamp = now - start
                mem.append(mi.rss)
                swap.append(mi.swap)
                sample_times.append(timestamp)
                if update_dt > 0 and (now - lastplot > update_dt):
                    _plot(sample_times, np.asarray(mem), np.asarray(swap))
                    lastplot = now
                time.sleep(sample_dt)
        except (KeyboardInterrupt, psutil.NoSuchProcess):
            break

    print("Done sampling")

    return [np.asarray(sample_times), np.asarray(mem), np.asarray(swap)]


if __name__ == "__main__":
    main()
