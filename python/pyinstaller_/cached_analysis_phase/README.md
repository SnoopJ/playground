This is an example of adding caching of the [`Analysis`](https://pyinstaller.org/en/stable/operating-mode.html#analysis-finding-the-files-your-program-needs)
process to a [`PyInstaller`](https://pyinstaller.org/) build chain.

Briefly, this phase walks the dependency graph of the application being built
in order to build up a series of Table of Contents (`TOC`) objects that are
used by the later stages of `PyInstaller`. For complex applications, this
analysis may dominate the build time, but may often be unchanged between
builds, in particular when debugging. The specific case that caused me to write
this proof-of-concept is a build that takes about 30 minutes to run, and 20
minutes of that build time is spent in the analysis phase!

The machinery of `main.spec` checks for the `PYI_ANALYSIS_CACHE` environment
variable, and tries to load cached analysis data from the given filename if it
is defined. If the envvar is not defined, it runs the usual `Analysis` phase
and saves the result to `analysis_cache.json`

For a demonstration, use the included `make` targets:

```
$ time make run  # build and run the original distribution
---
Building original bundle
---

108 INFO: PyInstaller: 5.9.0
109 INFO: Python: 3.9.9
113 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
...
10236 INFO: Building EXE from EXE-00.toc completed successfully.
10238 INFO: checking COLLECT
10238 INFO: Building COLLECT because COLLECT-00.toc is non existent
10238 INFO: Building COLLECT COLLECT-00.toc
11618 INFO: Building COLLECT COLLECT-00.toc completed successfully.
---
Running original bundle
---

./dist/main/main
Hello world!

real    0m12.175s
user    0m10.015s
sys     0m1.458s
$ time make run-modified  # build and run the modified distribution, using the cache created by the previous step
---
Building modified bundle
---

103 INFO: PyInstaller: 5.9.0
104 INFO: Python: 3.9.9
107 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
...
207 INFO: Building EXE from EXE-00.toc completed successfully.
209 INFO: checking COLLECT
210 INFO: Removing dir /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/dist/main
221 INFO: Building COLLECT COLLECT-00.toc
1478 INFO: Building COLLECT COLLECT-00.toc completed successfully.
---
Running modified bundle
---

./dist/main/main
I have modified the debug message. Pray I do not alter it further.

real    0m1.948s
user    0m0.925s
sys     0m0.710s
```

Note that the caching saves ~80% of the build time!
