import pytest

from lib import Foo


def test_FooWrap():
    f = Foo(-1)
    assert f.get_data() == -1
    f.set_data(42)
    assert f.get_data() == 42
