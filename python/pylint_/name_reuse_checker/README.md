This is an example of a [custom pylint checker](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html)
designed to issue a warning for multiple assignment statements targeting the same name in a single scope. The target use-case
is using the linter to catch code like this:

```python
name = 42
name = munge(name)
```

Which is almost always be better expressed as some variation of:

```python
name = 42
name_munged = munge(name)
```

## Usage

```
$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --load-plugins=name_reuse_checker \
    --score=n \
    --disable=all \
    --enable=multiple-name-assignment \
    target_program.py
************* Module target_program
target_program.py:7:4: W8901: name assigned to multiple times (multiple-name-assignment)
target_program.py:13:4: W8901: name assigned to multiple times (multiple-name-assignment)
target_program.py:19:4: W8901: name assigned to multiple times (multiple-name-assignment)
target_program.py:19:7: W8901: name assigned to multiple times (multiple-name-assignment)
target_program.py:25:4: W8901: name assigned to multiple times (multiple-name-assignment)
```
