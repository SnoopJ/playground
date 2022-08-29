import json
from pathlib import Path

import pytest

from user import User, VALID_COLORS


HERE = Path(__file__).parent.resolve()
TEST_DATA_FILE = HERE.joinpath("test_data.json")


with open(TEST_DATA_FILE, "r") as f:
    TEST_DATA = json.load(f)


@pytest.fixture(params=TEST_DATA["valid_users"])
def valid_user(request):
    yield User(**request.param)


@pytest.fixture(params=TEST_DATA["invalid_users"])
def invalid_user(request):
    yield User(**request.param)


def test_valid_user(valid_user):
    assert valid_user.name
    assert valid_user.favorite_color in VALID_COLORS


@pytest.mark.xfail(reason="Invalid user data")
def test_invalid_user(invalid_user):
    assert invalid_user.name
    assert invalid_user.favorite_color in VALID_COLORS
