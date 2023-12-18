This is an example of a [custom pylint checker](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html)
designed to issue a warning for long `if/elif/else` suites. The target use-case
here is using the linter to identify candidates for refactoring, like:

```python
if something():
    # 50 lines of code
elif something_else():
    # 50 more lines of code
else:
    # 50 final lines of code
```

Which is almost always be better expressed as some variation of:

```python
if something():
    handle_something(state)
elif something_else():
    handle_something_else(state)
else:
    handle_else(state)
```

## Usage

```
$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --score=n \
    --load-plugins=long_if_checker \
    --disable=all \
    --enable=if-body-too-long \
    --max-if-suite-length=50 \
    target_program.py

$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --score=n \
    --load-plugins=long_if_checker \
    --disable=all \
    --enable=if-body-too-long \
    --max-if-suite-length=1 \
    target_program.py
************* Module target_program
target_program.py:9:0: W8900: overlong suite body (if-body-too-long)
target_program.py:18:0: W8900: overlong suite body (if-body-too-long)
target_program.py:28:4: W8900: overlong suite body (if-body-too-long)

$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --score=n \
    --load-plugins=long_if_checker \
    --disable=all \
    --enable=if-body-too-long \
    --max-if-suite-length=0 \
    --check-pure-if-length=y \
    target_program.py  # NOTE: Lines 38 and 42 are reported
************* Module target_program
target_program.py:9:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:18:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:28:4: W8900: overlong conditional body (if-body-too-long)
target_program.py:38:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:42:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:49:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:50:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:51:6: W8900: overlong conditional body (if-body-too-long)


$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --score=n \
    --load-plugins=long_if_checker \
    --disable=all \
    --enable=if-body-too-long \
    --max-if-suite-length=0 \
    --check-pure-if-length=n \
    target_program.py  # NOTE: Lines 38 and 42 are NOT reported
************* Module target_program
target_program.py:9:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:18:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:28:4: W8900: overlong conditional body (if-body-too-long)
target_program.py:49:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:50:0: W8900: overlong conditional body (if-body-too-long)
target_program.py:51:6: W8900: overlong conditional body (if-body-too-long)
```
