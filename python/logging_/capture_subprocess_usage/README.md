This example demonstrates the usage of CPython's [audit hook system] to record usage of `subprocess` by third-party code
into an application's existing `logging` hierarchy, with accurate stack offsets.

[audit hook system]: https://docs.python.org/3/library/sys.html#sys.addaudithook


```
$ python3 main.py
And the result is: data = (b'Wow, amazing computation!\n', '42\n')

$ python3 main.py -v
2026-03-24 15:59:47,050 [DEBUG] other.do_something(+L11): running subprocess with args: ['echo', 'Wow, amazing computation!']
        env = {'ACME_DATA': 'Be careful, the environment might have secrets in it!'}
2026-03-24 15:59:47,056 [DEBUG] other._run_second_computation(+L6): running subprocess with args: ['echo', '42']
        env = None
And the result is: data = (b'Wow, amazing computation!\n', '42\n')
```
