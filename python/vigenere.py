"""
Implement a Vigenere cipher using deques
"""
from collections import deque
import string

ring = deque(string.ascii_letters)

msg = "Attack at dawn"
key = "Lorem ipsum dolor sit amet"


def _transform(msgc, keyc, direction=-1):
    """ Return the ciphered value of msgc for the Caesar cipher dictated by keyc """
    if any(c not in string.ascii_letters for c in (msgc, keyc)):
        return msgc

    r2 = ring.copy()
    r2.rotate(direction * ring.index(keyc))
    return r2[ring.index(msgc)]


def encode(msgc, keyc):
    return _transform(msgc, keyc, -1)


def decode(msgc, keyc):
    return _transform(msgc, keyc, +1)


def cipher(msg, key):
    return "".join(encode(m, k) for m, k in zip(msg, key))


def decipher(msg, key):
    return "".join(decode(m, k) for m, k in zip(msg, key))


ciphered = cipher(msg, key)

print(ciphered)
deciphered = decipher(ciphered, key)
print(deciphered)
