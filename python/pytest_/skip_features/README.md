This example demonstrates how to add feature flags to `pytest` that allow the
invoking user to skip tests that depend on fixtures associated with those flags


```
18:41 [snoopjedi@denton ~/playground/python/pytest_/skip_features (main *)]
$ python3 -m pytest
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_features
plugins: anyio-3.7.0
collected 4 items

test_stuff.py ....                                                             [100%]

================================= 4 passed in 0.02s ==================================
18:41 [snoopjedi@denton ~/playground/python/pytest_/skip_features (main *)]
$ python3 -m pytest --skip-foo
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_features
plugins: anyio-3.7.0
collected 4 items

test_stuff.py s.s.                                                             [100%]

============================ 2 passed, 2 skipped in 0.02s ============================
18:41 [snoopjedi@denton ~/playground/python/pytest_/skip_features (main *)]
$ python3 -m pytest --skip-bar
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_features
plugins: anyio-3.7.0
collected 4 items

test_stuff.py .ss.                                                             [100%]

============================ 2 passed, 2 skipped in 0.02s ============================
18:41 [snoopjedi@denton ~/playground/python/pytest_/skip_features (main *)]
$ python3 -m pytest --skip-foo --skip-bar
================================ test session starts =================================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/skip_features
plugins: anyio-3.7.0
collected 4 items

test_stuff.py sss.                                                             [100%]

============================ 1 passed, 3 skipped in 0.02s ============================
```
