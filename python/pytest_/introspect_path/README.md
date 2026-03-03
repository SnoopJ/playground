An example of introspecting the running `pytest` session to find the test root for the whole session

```
$ python3 -m pytest -s .
==================================== test session starts ====================================
platform linux -- Python 3.9.16, pytest-8.4.2, pluggy-1.6.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/introspect_path
collected 2 items

subsuite/test_sub.py subsuite: request.config.rootdir = local('/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/introspect_path')
.
test_top.py top: request.config.rootdir = local('/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/introspect_path')
.

===================================== 2 passed in 0.02s =====================================
```
