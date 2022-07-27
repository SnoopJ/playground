from multiprocessing import Pool
import os
import random
import subprocess
from threading import Thread
import time

import requests
import uvicorn

from consumer import Consumer


def _run_consumer():
    unlock = "UNLOCK" in os.environ
    c = Consumer(unlock=unlock)
    c.run()


def _send():
    response = requests.post("http://localhost:8000/submit", json={"data": random.randint(0, 255)})
    response.raise_for_status()

    return response


def send_requests(num_req: int = 5, num_proc: int = 2):
    print(f"Sending {num_req} requests with a pool of {num_proc} processes")

    with Pool(num_proc) as pool:
        results = [pool.apply_async(_send) for _ in range(num_req)]

        for res in results:
            print(f"Got server reply: {res.get().json()}")



if __name__ == "__main__":
    consumer_thread = Thread(target=_run_consumer)
    consumer_thread.start()

    proc = subprocess.Popen(["uvicorn", "--workers", "2", "server:app"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f"Running server in subprocess (pid={proc.pid})")

    # give the server a few seconds to establish itself
    time.sleep(3)

    send_requests()

    consumer_thread.join()
