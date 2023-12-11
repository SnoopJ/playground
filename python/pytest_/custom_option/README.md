# Weird pytest behavior when adding a custom parser option

This example explores the behavior of `pytest` when adding a custom
command-line option (see [pytest documentation][pytest_example] for an example).

As described in the documentation for [`pytest_addoption`][pytest_addoption]:

> This function should be implemented only in plugins or conftest.py files
> situated **at the tests root directory** due to how pytest discovers plugins
> during startup.

So my reading of the documentation is that invoking `pytest` with the test
directory above the 'real' root should cause this additional option to be
unrecognized. In practice, I have noticed that the behavior seems to also
depend on whether or not a default value for the option is defined. I don't
understand this!

[pytest_example]: https://docs.pytest.org/en/stable/example/simple.html#pass-different-values-to-a-test-function-depending-on-command-line-options
[pytest_addoption]: https://docs.pytest.org/en/stable/reference/reference.html#std-hook-pytest_addoption

## Running test suite with 'right' root

### Without default

```
$ python3 -m pytest -rs -s dummypkg_nodefault/dummypkg/tests/  # no error, as expected
====== test session starts ======
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/custom_option
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 1 item

dummypkg_nodefault/dummypkg/tests/test_something.py flavor is None
.

====== 1 passed in 0.02s ======
```

### With default

```
$ python3 -m pytest -rs -s dummypkg_withdefault/dummypkg/tests/  # no error, as expected
====== test session starts =======
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/custom_option
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 1 item

dummypkg_withdefault/dummypkg/tests/test_something.py s

====== short test summary info ======
SKIPPED [1] dummypkg_withdefault/dummypkg/tests/test_something.py:1: Test does not run for default flavor
======= 1 skipped in 0.04s =======
```

## Running test suite with 'wrong' root

### Without default

```
$ python3 -m pytest -rs -s dummypkg_nodefault/  # broken, as expected
====== test session starts =======
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/custom_option
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 1 item

dummypkg_nodefault/dummypkg/tests/test_something.py E

============= ERRORS =============
__________________________________________________________________ ERROR at setup of test_something __________________________________________________________________

self = <_pytest.config.Config object at 0x7f8a8a97bf10>, name = 'flavor', default = <NOTSET>, skip = False

    def getoption(self, name: str, default=notset, skip: bool = False):
        """Return command line option value.

        :param name: Name of the option.  You may also specify
            the literal ``--OPT`` option instead of the "dest" option name.
        :param default: Default value if no option of that name exists.
        :param skip: If True, raise pytest.skip if option does not exists
            or has a None value.
        """
        name = self._opt2dest.get(name, name)
        try:
>           val = getattr(self.option, name)
E           AttributeError: 'Namespace' object has no attribute 'flavor'

/home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/site-packages/_pytest/config/__init__.py:1611: AttributeError

The above exception was the direct cause of the following exception:

request = <SubRequest 'skip_default_flavor' for <Function test_something>>

    @pytest.fixture
    def skip_default_flavor(request):
>       if request.config.getoption("--flavor") == "default":
E       ValueError: no option named 'flavor'

dummypkg_nodefault/dummypkg/tests/conftest.py:12: ValueError
======== 1 error in 0.19s ========
```

### With default

```
$ python3 -m pytest -rs -s dummypkg_withdefault/  # NOT broken, what the heck?!
====== test session starts =======
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/custom_option
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 1 item

dummypkg_withdefault/dummypkg/tests/test_something.py s

====== short test summary info ======
SKIPPED [1] dummypkg_withdefault/dummypkg/tests/test_something.py:1: Test does not run for default flavor
======= 1 skipped in 0.02s =======
```
