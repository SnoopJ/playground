import pytest
import foo

@pytest.fixture
def fooobj():
    return foo.Foo()

def test_foo(fooobj):
    # write a test for your object here
    pass
