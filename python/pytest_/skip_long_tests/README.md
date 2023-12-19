This sample is taken pretty much directly from [a post by jwodder](https://jwodder.github.io/kbits/posts/pytest-mark-off/#option-2-use-pytest-mark-skipif)
showing how to disable slow tests by default and run them only when explicitly
requested.

I've also expanded on the example and added an option to reorder test execution
so that tests marked as slow will run *after* not-slow tests.


```
$ python3 -m pytest -v .
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0 -- /home/snoopjedi/.pyenv/versions/3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_long_tests
configfile: pyproject.toml
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 4 items

test_lib.py::test_short PASSED                                                 [ 25%]
test_lib.py::test_long SKIPPED (Test is marked slow and --run-slow was not...) [ 50%]
test_lib.py::test_another_short PASSED                                         [ 75%]
test_lib.py::test_another_long SKIPPED (Test is marked slow and --run-slow...) [100%]

============================ 2 passed, 2 skipped in 0.24s ============================
$ python3 -m pytest -v --run-slow .
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0 -- /home/snoopjedi/.pyenv/versions/3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_long_tests
configfile: pyproject.toml
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 4 items

test_lib.py::test_short PASSED                                                 [ 25%]
test_lib.py::test_long PASSED                                                  [ 50%]
test_lib.py::test_another_short PASSED                                         [ 75%]
test_lib.py::test_another_long PASSED                                          [100%]

================================= 4 passed in 4.25s ==================================
$ python3 -m pytest -v --run-slow --reorder-slow .
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0 -- /home/snoopjedi/.pyenv/versions/3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_long_tests
configfile: pyproject.toml
plugins: requests-mock-1.9.3, xdist-3.3.1, mock-3.11.1, sopel-8.0.0.dev0, cov-4.1.0
collected 4 items

test_lib.py::test_short PASSED                                                 [ 25%]
test_lib.py::test_another_short PASSED                                         [ 50%]
test_lib.py::test_long PASSED                                                  [ 75%]
test_lib.py::test_another_long PASSED                                          [100%]

================================= 4 passed in 4.24s ==================================
```
