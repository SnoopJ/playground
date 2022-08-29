This sample shows how to [parametrize](https://docs.pytest.org/en/latest/how-to/parametrize.html) a `pytest` fixture using data loaded from a JSON file

### Output

```
$ python3 -m pytest -v
============================================================= test session starts ==============================================================
platform linux -- Python 3.9.9, pytest-7.1.2, pluggy-1.0.0 -- /home/snoopjedi/playground/.direnv/python-3.9.9/bin/python3
cachedir: .pytest_cache
rootdir: /home/snoopjedi/playground/python/pytest_/fixture_parametrized_by_json
collected 5 items

test_user.py::test_valid_user[valid_user0] PASSED                                                                                        [ 20%]
test_user.py::test_valid_user[valid_user1] PASSED                                                                                        [ 40%]
test_user.py::test_valid_user[valid_user2] PASSED                                                                                        [ 60%]
test_user.py::test_invalid_user[invalid_user0] XFAIL (Invalid user data)                                                                 [ 80%]
test_user.py::test_invalid_user[invalid_user1] XFAIL (Invalid user data)                                                                 [100%]

========================================================= 3 passed, 2 xfailed in 0.05s =========================================================
```
