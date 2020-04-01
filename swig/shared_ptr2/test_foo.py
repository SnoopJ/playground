import pytest
import foo

@pytest.fixture
def fooobj():
    return foo.Foo()

def test_foo():
    res = foo.munge_num(42);
    assert res;
