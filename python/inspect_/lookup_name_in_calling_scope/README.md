This sample shows off how to lookup a name in the context of a calling function

```
$ python3.9 main.py
foo(42, 'data'='Twas brillig and the slithy toves')
was dispatched
foo(1337, 'data'='Twas brillig and the slithy toves')
was dispatched
foo(-1, 'data'='Twas brillig and the slithy toves')
was dispatched
---

bar(42, 'data'='Twas brillig and the slithy toves')
was dispatched
bar(1337, 'data'='Twas brillig and the slithy toves')
was dispatched
bar(-1, 'data'='Twas brillig and the slithy toves')
was dispatched
---

Lookup failed for func_baz
was NOT dispatched
Lookup failed for func_baz
was NOT dispatched
Lookup failed for func_baz
was NOT dispatched
---
```
