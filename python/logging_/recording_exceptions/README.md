This sample shows off the functionality of the `exc_info` parameter to `logging.Logger`
instances (documented [here](https://docs.python.org/3/library/logging.html#logging.Logger.debug))
to add exception information to a logging message.


### Without `exc_info`

```
$ python3 main.py
INFO:__main__:A regular old logging message
ERROR:root:An error occurred exc_info=False
```

### With `exc_info`

```
$ python3 main.py --exc-info
INFO:__main__:A regular old logging message
ERROR:root:An error occurred exc_info=True
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/recording_exceptions/main.py", line 21, in main
    failing_function()
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/recording_exceptions/main.py", line 15, in failing_function
    raise RuntimeError("Something went wrong")
RuntimeError: Something went wrong
```
