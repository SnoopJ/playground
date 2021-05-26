import pytest

from lib import Foo, FooWrap


def test_Foo():
    f = Foo()
    assert f.get_data() == -1
    with pytest.raises(AttributeError):
        f.set_data(42)


def test_FooWrap():
    f = FooWrap()
    assert f.get_data() == -1
    f.set_data(42)
    assert f.get_data() == 42
