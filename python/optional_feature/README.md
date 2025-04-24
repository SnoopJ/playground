This sample shows off how to implement support for an optional dependency in a larger application. This approach uses
a [façade](https://en.wikipedia.org/wiki/Facade_pattern) to hide away the details of the conditional import (and in real
code, additional configuration/complexity that goes with each optional component).

With this approach, the application logic can poll the availability of its dependencies and issue prompt errors when a
requested task is known to require some optional feature that is not satisfied. This can be a big deal in applications
where the optional dependency will only be used late in the program's lifespan, and in a naïve approach much wasted work
may be done before reaching that point.


```
$ python3 -m optional_feature
WARNING:optional_feature.somelib_facade:somelib is not available, functionality will be degraded
INFO:root:OK

$ python3 -m optional_feature -v
WARNING:optional_feature.somelib_facade:somelib is not available, functionality will be degraded
DEBUG:optional_feature.somelib_facade:Exception details:
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/optional_feature/somelib_facade.py", line 6, in <module>
    import somelib
ModuleNotFoundError: No module named 'somelib'
INFO:root:OK
```
