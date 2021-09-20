"""
Based on a question in Freenode #python on Dec 19, 2019 about how to read
a file 4 bytes at a time *except* a tail that may be up to 4 bytes long
"""
from io import BytesIO
from collections import deque

f = BytesIO(b"abcdefgh")

def chunks(s, n=4):
    chunk = s.read(n)
    while len(chunk):
        yield chunk
        chunk = s.read(n)

buf = deque(f.read(4))

for nibble in chunks(f):
    buf.extend(nibble)
    if 4 < len(buf) <= 8:
        yummy = bytes(buf.popleft() for _ in range(4))
        print(f"yummy bit: {yummy}")

print(f"not yummy tail: {bytes(buf)}")
