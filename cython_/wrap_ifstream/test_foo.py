import pytest

from foo import load_wrap

def test_load_wrap():
    result = load_wrap(__file__)
    assert result.startswith("import pytest")
