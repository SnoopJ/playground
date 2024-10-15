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
   importlib_metadata==8.4.0  /home/snoopjedi/.cache/pip/http-v2/4/8/0/9/a/4809a32889b4bce95d324331e45c36059ebd9a208518fd1df3a74fe1.body
               numpy==1.23.4  /home/snoopjedi/.cache/pip/http-v2/4/e/0/2/1/4e0216b300e4dde31328924def1efba0dcdbafaa2f93cc39b4f072aa.body
                numpy==2.0.2  /home/snoopjedi/.cache/pip/http-v2/c/0/b/7/c/c0b7c8f556dc2f24aa2eb52b6f16c9cecfd02048ca00aa0e89b67e98.body
             packaging==24.1  /home/snoopjedi/.cache/pip/http-v2/c/d/6/0/d/cd60de26b5c99a8064df56c2a3888451ddcd34abbeeb720d610dfdaf.body
                   pip==24.2  /home/snoopjedi/.cache/pip/http-v2/8/f/0/1/4/8f0141915fe0b79e18317c9c8d5fe78ebfbff35923832100db4c51da.body
               pygame==2.6.1  /home/snoopjedi/.cache/pip/http-v2/5/a/a/4/e/5aa4e0a11bd5065f6436878fcdf679770847be42e607cc404d2c716e.body
                      q==2.7  /home/snoopjedi/.cache/pip/http-v2/a/b/5/1/3/ab5132e872e9db5fcfbd16ed66c6c7418fb7f5309e402609f86851a4.body
          setuptools==74.1.1  /home/snoopjedi/.cache/pip/http-v2/9/8/b/8/0/98b8067cf7c3152f44990eb21836bd0b74028f249880d2c2ce620990.body
          setuptools==75.1.0  /home/snoopjedi/.cache/pip/http-v2/0/4/9/1/3/04913e6ed91046ac58c7318fa4680857b7e130fee9f1428aea5245fb.body
                tomli==2.0.1  /home/snoopjedi/.cache/pip/http-v2/6/4/9/8/a/6498a97ba33d5bdd385aa8f5ea5d4d15aa22b0d23b6bd2e36e941896.body
         versioningit==3.1.2  /home/snoopjedi/.cache/pip/http-v2/d/8/e/7/f/d8e7f308be03b2f1ce420beaf0ec046009c3aac1088d447b2327b96b.body
               wheel==0.44.0  /home/snoopjedi/.cache/pip/http-v2/6/8/1/f/4/681f47f5e78d74219fba37d0f09e9d0800b8f0b35851037d7081c26a.body
                zipp==3.20.1  /home/snoopjedi/.cache/pip/http-v2/1/8/c/d/e/18cde7bede1e79f8e703469df2cf65ec693cb5a87ca8a6ab1a0e35e9.body
```

