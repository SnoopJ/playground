import sys


idx = 1
while True:
    if idx > 2:
        breakpoint()

    line = sys.stdin.readline()
    if not line:
        break

    print(f"Line #{idx} of stdin is:\n{line}")

    idx += 1
