This is an example of a [custom pylint checker](https://pylint.pycqa.org/en/latest/development_guide/how_tos/custom_checkers.html)
designed to issue a warning for long `if/elif/else` clauses. The target use-case
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
    --max-if-clause-length 50 \
    target_program.py

$ PYTHONPATH=$PWD \
  python3 -m pylint \
    --score=n \
    --load-plugins=long_if_checker \
    --disable=all \
    --enable=if-body-too-long \
    --max-if-clause-length 1 \
    target_program.py
************* Module target_program
target_program.py:9:0: W8900: overlong suite body (if-body-too-long)
target_program.py:18:0: W8900: overlong suite body (if-body-too-long)
target_program.py:28:4: W8900: overlong suite body (if-body-too-long)
```

## Inconsistent treatment of `else` length

Note that `astroid` treats `else` clauses different from `if/elif`, so the
line number reported for a too-long `else` clause will be the first line in
the body of the clause, but the report for `if/elif` will be the line containing
the predicate. It is easier for this proof-of-concept to accept this quirk
than to try and work around it, but it's worth mentioning since it means there
is an off-by-one to the length counting of these clauses.
