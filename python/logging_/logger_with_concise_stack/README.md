This example shows off defining a custom `logging.Formatter` with a `formatStack()`
method that leaves off code context in the reported stack.

```
$ python3 logger_with_concise_stack.py
[INFO]: This is a logger message with a verbose stack
Stack (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 31, in <module>
    func("This is a logger message with a verbose stack", level=3)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
    func(msg, level - 1)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
    func(msg, level - 1)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
    func(msg, level - 1)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 28, in func
    logger.info(msg, stack_info=True)
[INFO]: This is a logger message with a concise stack
Stack (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 36, in <module>
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 26, in func
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/logger_with_concise_stack.py", line 28, in func
```
