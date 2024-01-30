This is an example showing off the use of the [`pytest-order`](https://pypi.org/project/pytest-order)
plugin to `pytest` to run a final test that asserts that we covered every
value of one dimension of a multidimensional parameterization.

The sample application code includes some combinations of parameters that are
invalid as a simulacrum of the 'real' case that originally caused me to wonder
how to spell this.

```
$ python3 -m pytest test_acmelib.py
=============================== test session starts ===============================
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/combinatoric_sanity_check
plugins: order-1.2.0
collected 4 items

test_acmelib.py F..F                                                        [100%]

# ... snip ...

============================= short test summary info =============================
FAILED test_acmelib.py::test_run_job[comb0] - RuntimeError: Combination AA->A is INVALID
FAILED test_acmelib.py::test_saw_all_outputformat - AssertionError: Missing some output formats: [<OutputFormat.C: 'C'>]
===================== 2 failed, 2 passed, 1 warning in 0.17s ======================
```
