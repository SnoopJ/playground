import foo
import pytest

@pytest.fixture
def foo_obj():
    return foo.Foo()

def test_bar_no_args(foo_obj):
    foo_obj.bar()

def test_bar_one_arg(foo_obj):
    foo_obj.bar(42)

def test_bar_two_args(foo_obj):
    foo_obj.bar(420, 69)

def test_bar_wrapper(foo_obj):
    foo_obj.new_bar(420, 69)
