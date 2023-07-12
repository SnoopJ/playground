def pytest_addoption(parser):
    parser.addoption(
        "--skip-foo", action="store_true",
    )
    parser.addoption(
        "--skip-bar", action="store_true",
    )

