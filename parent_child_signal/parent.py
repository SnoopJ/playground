import subprocess
from sys import stdout, stderr
import time

DELAY = 10  # bail out time, seconds; will send SIGUSR2 after this
SIGUSR1, SIGUSR2 = subprocess.signal.SIGUSR1, subprocess.signal.SIGUSR2

print("Parent: spawning child...")
child = subprocess.Popen(["python", "child.py"])  # , stdout=subprocess.PIPE, stderr=)
start = time.time()

print(f"Parent: waiting for KeyboardInterrupt or until {DELAY} seconds elapse...")

try:
    while time.time() - start < DELAY:
        pass
    print("Parent: sending child SIGUSR2")
    child.send_signal(SIGUSR2)
except KeyboardInterrupt:
    print("Parent: sending child SIGUSR1")
    child.send_signal(SIGUSR1)
