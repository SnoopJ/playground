def test_something(request, skip_default_flavor):
    flavor = request.config.getoption("--flavor")
    print(f"flavor is {flavor!r}")
