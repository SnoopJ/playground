import sys
import time


if __name__ == "__main__":
    start = time.monotonic()
    print("Hello world!")
    print("Dummy service running on:\n" + sys.version)

    while True:
        msg = f"Dummy service has been running for {time.monotonic() - start:.1f} seconds"
        print(msg)
        time.sleep(3)
