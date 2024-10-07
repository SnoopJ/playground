This example shows using a stateful `Mock` to perform "time travel" when
mocking an expensive function, advancing the observed clock by a fixed amount
(in this case, an hour) each time the mocked-away expensive function is called.

I wrote this example because I have some 'real' code that has similar structure
to this sample (where individual functions are brought togther in an orchestration
function) and I want to write tests for a time-budgeting feature similar to the
one shown off in this example.

```
$ python3 -m pytest -v -rP test_lib.py 
=============================== test session starts ===============================
platform linux -- Python 3.9.16, pytest-7.4.3, pluggy-1.3.0 -- /home/snoopjedi/scratch/.direnv/python-3.9.16/bin/python3
cachedir: .pytest_cache
rootdir: /home/snoopjedi/scratch/mock_time_travel
plugins: typeguard-4.3.0
collected 1 item                                                                  

test_lib.py::test_orchestrate PASSED                                        [100%]

===================================== PASSES ======================================
________________________________ test_orchestrate _________________________________
------------------------------ Captured stdout call -------------------------------
[2024-10-07T13:20:42.454484] cheap computation done
[2024-10-07T14:20:43.461883] fake expensive() return
[2024-10-07T14:20:44.469464] cheap computation done
[2024-10-07T15:20:45.479158] fake expensive() return
[2024-10-07T15:20:46.481345] cheap computation done
[2024-10-07T16:20:47.490099] fake expensive() return
Time limit reached (3:00:00), terminating loop early
================================ 1 passed in 6.08s ================================
```
