This example shows using a stateful fake object to perform "time travel" when
mocking an expensive function, advancing the observed clock by a fixed amount
(in this case, an hour) each time the mocked-away expensive function is called.

I wrote this example because I have some 'real' code that has similar structure
to this sample (where individual functions are brought togther in an orchestration
function) and I want to write tests for a time-budgeting feature similar to the
one shown off in this example.

```
$ python3 -m pytest -v -rP test_lib.py
=============================== test session starts ===============================
platform linux -- Python 3.9.16, pytest-8.3.2, pluggy-1.5.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/mock_sandbox/mock_time_travel
plugins: anyio-4.4.0
collected 1 item                                                                  

test_lib.py::test_orchestrate PASSED                                        [100%]

===================================== PASSES ======================================
________________________________ test_orchestrate _________________________________
------------------------------ Captured stdout call -------------------------------
[2024-10-07T16:52:42.875751] cheap computation done
[2024-10-07T17:52:43.882272] FAKE expensive() done
[2024-10-07T17:52:44.886276] cheap computation done
[2024-10-07T18:52:45.892727] FAKE expensive() done
[2024-10-07T18:52:46.894637] cheap computation done
[2024-10-07T19:52:47.896945] FAKE expensive() done
Time limit reached (3:00:00), terminating loop early
================================ 1 passed in 6.11s ================================
```
