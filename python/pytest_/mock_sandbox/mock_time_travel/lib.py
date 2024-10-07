import datetime
import time


HOUR = 60*60  # in sec


def cheap_func() -> str:
    time.sleep(1)
    return "cheap computation done"


def expensive_func() -> str:
    time.sleep(1*HOUR)
    return "expensive computation done"


def orchestrate(Niter: int, max_time: datetime.timedelta):
    start = datetime.datetime.now()

    for n in range(Niter):
        if (n % 2) == 0:
            msg = cheap_func()
        else:
            msg = expensive_func()

        now = datetime.datetime.now()
        print(f"[{now.isoformat()}] {msg}")

        if (now - start) >= max_time:
            print(f"Time limit reached ({max_time}), terminating loop early")
            break



if __name__ == "__main__":
    orchestrate()
