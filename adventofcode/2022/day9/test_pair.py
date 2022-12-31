import pytest

from pair import Pair


def test_pair_eq():
    assert Pair(0, 0) == Pair(0, 0)
    assert Pair(0, 0) == (0, 0)

    assert Pair(0, 0) != Pair(1, 0)
    assert Pair(0, 0) != (1, 0)


def test_pair_add():
    assert Pair(0, 0) + Pair(1, -1) == Pair(1, -1)
    assert Pair(0, 0) + (1, -1) == Pair(1, -1)

    assert Pair(1, 1) + Pair(1, -1) == Pair(2, 0)
    assert Pair(1, 1) + (1, -1) == Pair(2, 0)


def test_pair_move_towards():
    p1 = Pair(5, 5)

    p2 = Pair(0, 5)
    for movenum in range(1, 10):
        p2 = p2.move_towards(p1)
        x_exp = min(movenum, 4)
        assert p2 == (x_exp, 5)

