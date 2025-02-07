import pytest


@pytest.fixture(params=[1, 2, 3])
def varying(request):
    value = 1 + request.param
    yield value


def test_with_parametrized_fixture(varying):
    assert varying <= 4


@pytest.mark.parametrize("name, val", [('Larry', 1), ('Moe', 2), ('Curly Joe', 3)])
def test_with_direct_parameterization(name, val):
    assert len(name) >= 3
    assert val < 4
