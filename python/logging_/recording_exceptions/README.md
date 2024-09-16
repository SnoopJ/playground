This sample shows off the functionality of the `exc_info` parameter to `logging.Logger`
instances (documented [here](https://docs.python.org/3/library/logging.html#logging.Logger.debug))
to add exception information to a logging message.

```
$ python3 main.py
INFO:__main__:A regular old logging message
ERROR:root:An error occurred (with exc_info)
ValueError: original cause

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/recording_exceptions/main.py", line 13, in <module>
    raise RuntimeError("A subsequent error") from ValueError("original cause")
RuntimeError: A subsequent error
ERROR:root:An error occurred (without exc_info)
```
