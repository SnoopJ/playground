import signal
from signal import SIGINT, SIGUSR1, SIGUSR2, SIG_IGN


def handler(sig, frame):
    print(f"Child: received signal {sig}, now exiting!")
    exit()


signal.signal(SIGINT, SIG_IGN)  # explicitly ignore interrupt
signal.signal(SIGUSR1, handler)
signal.signal(SIGUSR2, handler)

print("Child: Waiting for SIGUSR1 or SIGUSR2...")

while True:
    signal.pause()
