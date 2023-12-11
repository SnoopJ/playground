import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--flavor",
        default="default",
    )


@pytest.fixture
def skip_default_flavor(request):
    if request.config.getoption("--flavor") == "default":
        pytest.skip(reason="Test does not run for default flavor")
