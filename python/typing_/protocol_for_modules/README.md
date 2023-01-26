This example demonstrates how to use [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
to enforce a particular interface for modules.

```
$ python3 -m mypy main.py  # mypy==0.991
main.py:21: error: Argument 1 to "consume_module" has incompatible type Module; expected "ModuleProto"  [arg-type]
main.py:21: note: "ModuleType" is missing following "ModuleProto" protocol members:
main.py:21: note:     func2, someattr
main.py:21: note: Following member(s) of "Module bad_mod" have conflicts:
main.py:21: note:     Expected:
main.py:21: note:         def func1(x: int) -> str
main.py:21: note:     Got:
main.py:21: note:         def func1(x: int) -> int
Found 1 error in 1 file (checked 1 source file)
```
