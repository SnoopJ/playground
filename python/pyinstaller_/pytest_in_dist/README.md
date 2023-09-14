This example shows off how to include `pytest` and a separate test suite inside of
a PyInstaller distribution, in order to run the test suite inside of the final
bundle.

```
$ make test
WITH_TESTS=1 python3 -m PyInstaller --noconfirm main.spec
168 INFO: PyInstaller: 5.13.0
169 INFO: Python: 3.9.16
173 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
...snip...

cp -r /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/pytest_in_dist/tests ./dist/main/
./dist/main/run_tests
============================== test session starts ===============================
platform linux -- Python 3.9.16, pytest-7.4.0, pluggy-1.2.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/pytest_in_dist/dist/main/run_tests
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/pytest_in_dist
collected 2 items

dist/main/tests/test_main.py::test_add PASSED                              [ 50%]
dist/main/tests/test_main.py::test_sub FAILED                              [100%]

==================================== FAILURES ====================================
____________________________________ test_sub ____________________________________

    def test_sub():
        for _ in range(10):
            x = random.randint(0, 256)
            y = random.randint(0, 256)
>           assert sub(x, y) == x - y
E           assert -1 == (146 - 132)
E            +  where -1 = sub(146, 132)

dist/main/tests/test_main.py:17: AssertionError
============================ short test summary info =============================
FAILED dist/main/tests/test_main.py::test_sub - assert -1 == (146 - 132)
========================== 1 failed, 1 passed in 0.10s ===========================
```
