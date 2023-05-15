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
variable, and if it is defined, tries to load cached analysis data from the
`pyi_analysis_cache/` directory in the same path as the spec file being run. If
the envvar is not defined, it runs the usual `Analysis` phase and saves the
result to `analysis_cache.json`

For a demonstration, use the included `make` targets:

```
$ time make run  # build and run the original distribution
---
Building original bundle
---

118 INFO: PyInstaller: 5.9.0
118 INFO: Python: 3.9.9
122 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
133 INFO: UPX is available.
134 INFO: Removing temporary files and cleaning cache in /home/snoopjedi/.cache/pyinstaller
149 INFO: Running main analysis
...
9935 INFO: Building EXE from EXE-00.toc completed successfully.
9936 INFO: checking COLLECT
9936 INFO: Building COLLECT because COLLECT-00.toc is non existent
9936 INFO: Removing dir /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/dist/main
9946 INFO: Building COLLECT COLLECT-00.toc
11256 INFO: Building COLLECT COLLECT-00.toc completed successfully.
---
Running original bundle
---

./dist/main/main
Hello world!

real    0m11.748s
user    0m9.734s
sys     0m1.393s
$ time make run-modified  # build and run the modified distribution, using the cache created by the previous step
---
Building modified bundle
---

132 INFO: PyInstaller: 5.9.0
133 INFO: Python: 3.9.9
137 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
149 INFO: UPX is available.
150 INFO: Removing temporary files and cleaning cache in /home/snoopjedi/.cache/pyinstaller
164 INFO: Using cached analysis from '/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/pyi_analysis_cache'
179 INFO: checking PYZ
179 INFO: Building PYZ because PYZ-00.toc is non existent
180 INFO: Building PYZ (ZlibArchive) /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/build/main/PYZ-00.pyz
2013 INFO: Building PYZ (ZlibArchive) /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/build/main/PYZ-00.pyz completed successfully.
2022 INFO: checking PKG
2022 INFO: Building PKG because PKG-00.toc is non existent
2023 INFO: Building PKG (CArchive) main.pkg
2073 INFO: Building PKG (CArchive) main.pkg completed successfully.
2075 INFO: Bootloader /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.9/lib/python3.9/site-packages/PyInstaller/bootloader/Linux-64bit-intel/run
2075 INFO: checking EXE
2075 INFO: Building EXE because EXE-00.toc is non existent
2075 INFO: Building EXE from EXE-00.toc
2076 INFO: Copying bootloader EXE to /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/build/main/main
2077 INFO: Appending PKG archive to custom ELF section in EXE
2098 INFO: Building EXE from EXE-00.toc completed successfully.
2100 INFO: checking COLLECT
2100 INFO: Building COLLECT because COLLECT-00.toc is non existent
2101 INFO: Removing dir /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/cached_analysis_phase/dist/main
2113 INFO: Building COLLECT COLLECT-00.toc
3542 INFO: Building COLLECT COLLECT-00.toc completed successfully.
---
Running modified bundle
---

./dist/main/main
I have modified the debug message. Pray I do not alter it further.

real    0m4.086s
user    0m2.716s
sys     0m0.967s
```

Note that the caching saves an appreciable amount of the build time.
