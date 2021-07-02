import pytest
import foo

@pytest.fixture
def fooobj():
    return foo.Foo(42)

def test_foo(fooobj):
    foo.munge(fooobj, 2112)
    pass
