`pip` has two different kinds of [caching](https://pip.pypa.io/en/stable/topics/caching/#what-is-cached):

1) Caching wheels built **by `pip` on the local system** (either from local sources, or from sources provided by a remote index)
2) Caching **HTTP responses** from an index (including pre-built wheels downloaded from the index)

Somewhat confusingly, the `pip cache list` command **only** tells you about (1) and provides no mechanism for inspecting
the cache entries associated with (2). That caching works very much like a web browser cache and as far as I know it is
not reversible (i.e. you cannot go from `~/.cache/pip/http-v2/e/a/c/e/4/eace4375bd28305395cc944828aca397282df81912e8222d72def3fd.body` to `https://...`).

This is an example program that manually crawls the HTTP cache and reconstructs the names and versions of pre-built
distributions that have previously been downloaded from an index.

**IMPORTANT NOTE:** this reconstruction is **completely unaware of [compatibility tags](https://peps.python.org/pep-0425/)**.
If there is a possibility that you have wheels for multiple versions/runtimes of Python or multiple platforms, this program
is totally unable to distinguish between those. I wrote this for fun, not to be someone's load-bearing hack. User beware!

### Example invocation

```
$ python3 crawl_pip_http_cache.py

Found wheels in pip HTTP cache:
-------------------------------
importlib_metadata==8.4.0
numpy==1.23.4
numpy==2.0.2
packaging==24.1
pip==24.2
q==2.7
setuptools==74.1.1
tomli==2.0.1
versioningit==3.1.2
wheel==0.44.0
zipp==3.20.1
```

