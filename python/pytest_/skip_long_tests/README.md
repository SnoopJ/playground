This sample is taken pretty much directly from [a post by jwodder](https://jwodder.github.io/kbits/posts/pytest-mark-off/#option-2-use-pytest-mark-skipif)
showing how to disable slow tests by default and run them only when explicitly
requested.


```
$ python3 -m pytest -v .
======================================================================== test session starts =========================================================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_long_tests
configfile: pyproject.toml
plugins: anyio-3.7.0
collected 2 items

test_lib.py::test_short PASSED                                                                                                                                 [ 50%]
test_lib.py::test_long SKIPPED (Test is marked slow and --run-slow was not given)                                                                              [100%]

==================================================================== 1 passed, 1 skipped in 0.12s ====================================================================
$ python3 -m pytest --run-slow -v .
======================================================================== test session starts =========================================================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_long_tests
configfile: pyproject.toml
plugins: anyio-3.7.0
collected 2 items

test_lib.py::test_short PASSED                                                                                                                                 [ 50%]
test_lib.py::test_long PASSED                                                                                                                                  [100%]

========================================================================= 2 passed in 2.12s ==========================================================================
```
