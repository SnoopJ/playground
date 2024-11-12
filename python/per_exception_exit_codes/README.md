This example shows off the definition of an application-specific exception hierarchy and custom [`sys.excepthook`](https://docs.python.org/3/library/sys.html#sys.excepthook)
to associate specific exit codes with each application-specific exception.

```
$ python3 main.py; echo -e "\nexited with code $?"
Running the first step
Running the second step

exited with code 0
$ python3 main.py --fail-general; echo -e "\nexited with code $?"
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 71, in <module>
    main(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 61, in main
    raise RuntimeError("This is a general failure caused by an exception outside the Python exception hierarchy")
RuntimeError: This is a general failure caused by an exception outside the Python exception hierarchy

exited with code 1
$ python3 main.py --fail-acme; echo -e "\nexited with code $?"
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 71, in <module>
    main(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 63, in main
    raise AcmeException("This is a general Acme failure not associated with a specific failure mode")
AcmeException: This is a general Acme failure not associated with a specific failure mode

exited with code 32
$ python3 main.py --fail-first; echo -e "\nexited with code $?"
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 71, in <module>
    main(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 65, in main
    first_step(fail=args.fail_first)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 31, in first_step
    raise FirstStepFailure("The first step has failed")
FirstStepFailure: The first step has failed

exited with code 33
$ python3 main.py --fail-second; echo -e "\nexited with code $?"
Running the first step
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 71, in <module>
    main(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 66, in main
    second_step(fail=args.fail_second)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/per_exception_exit_codes/main.py", line 38, in second_step
    raise SecondStepFailure("The second step has failed")
SecondStepFailure: The second step has failed

exited with code 34
```
