This example shows off how to build a PyInstaller bundle that has multiple EXEs
with common(ish) dependencies without running multiple `Analysis` phases. I
wrote this as a proof of concept for speeding up the build of a project with
multiple `Analysis` instances where each instance had largely the same graph,
but was very expensive to compute.


```
$ python3 -m PyInstaller app.spec
233 INFO: PyInstaller: 5.13.0
234 INFO: Python: 3.9.16
238 INFO: Platform: Linux-5.4.0-124-generic-x86_64-with-glibc2.31
247 INFO: UPX is available but is disabled on non-Windows due to known compatibility problems.
253 INFO: Extending PYTHONPATH with paths
['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis',
 '/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis']
691 INFO: checking Analysis
691 INFO: Building Analysis because Analysis-00.toc is non existent

... snip ...

43323 INFO: checking PYZ
43324 INFO: Building PYZ because PYZ-00.toc is non existent
43324 INFO: Building PYZ (ZlibArchive) /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis/build/app/PYZ-00.pyz
45330 INFO: Building PYZ (ZlibArchive) /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis/build/app/PYZ-00.pyz completed successfully.
45375 INFO: checking PKG
45375 INFO: Building PKG because PKG-00.toc is non existent
45376 INFO: Building PKG (CArchive) main.pkg
45415 INFO: Building PKG (CArchive) main.pkg completed successfully.
45417 INFO: Bootloader /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/bootloader/Linux-64bit-intel/run
45417 INFO: checking EXE
45417 INFO: Building EXE because EXE-00.toc is non existent
45418 INFO: Building EXE from EXE-00.toc
45418 INFO: Copying bootloader EXE to /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis/build/app/main
45419 INFO: Appending PKG archive to custom ELF section in EXE
45489 INFO: Building EXE from EXE-00.toc completed successfully.
45492 INFO: checking PKG
45492 INFO: Building PKG because PKG-01.toc is non existent
45493 INFO: Building PKG (CArchive) other.pkg
45539 INFO: Building PKG (CArchive) other.pkg completed successfully.
45541 INFO: Bootloader /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/bootloader/Linux-64bit-intel/run
45541 INFO: checking EXE
45542 INFO: Building EXE because EXE-01.toc is non existent
45542 INFO: Building EXE from EXE-01.toc
45543 INFO: Copying bootloader EXE to /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pyinstaller_/multiple_exes_same_analysis/build/app/other
45543 INFO: Appending PKG archive to custom ELF section in EXE
45585 INFO: Building EXE from EXE-01.toc completed successfully.
45608 INFO: checking COLLECT
45613 INFO: Building COLLECT because COLLECT-00.toc is non existent
45614 INFO: Building COLLECT COLLECT-00.toc
47079 INFO: Building COLLECT COLLECT-00.toc completed successfully.
$ ./dist/app/main
Hello from the main program
arr = array([0, 1, 2, 3, 4, 5, 6])
$ ./dist/app/other
Hello from the other program
df =    foo bar
0    1   a
1    2   b
2    3   c
3    4   d
4    5   e
$ pyi-archive_viewer --brief --list --recursive dist/app/main > main_archive.txt
$ pyi-archive_viewer --brief --list --recursive dist/app/other > other_archive.txt
$ diff main_archive.txt other_archive.txt  # the only difference between the bundled data is the entrypoint itself
1c1
< Contents of 'main' (PKG/CArchive):
---
> Contents of 'other' (PKG/CArchive):
13c13
<  main
---
>  other

$ pyi-archive_viewer --brief --list --recursive dist/app/main | grep pandas | wc -l # main's PYZ contains pandas data, even though it isn't needed
262
