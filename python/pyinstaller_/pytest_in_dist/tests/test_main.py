import random

from main import add, sub


def test_add():
    for _ in range(10):
        x = random.randint(0, 256)
        y = random.randint(0, 256)
        assert add(x, y) == x + y


def test_sub():
    for _ in range(10):
        x = random.randint(0, 256)
        y = random.randint(0, 256)
        assert sub(x, y) == x - y
