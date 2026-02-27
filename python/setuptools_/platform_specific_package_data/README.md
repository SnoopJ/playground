This is a (crude) example of how to determine the `package_data` for a
`setuptools` package based on the platform where the build occurs.

**IMPORTANT NOTE**: because this is a pure Python package, the resulting wheel
has the same filename on each platform! If you go down this route I would
recommend being a bit more careful to distinguish the wheels for each platform,
perhaps by manually tagging them, or changing the package name.


After running `python3 -m build .` on Linux:

```
$ unzip -l dist/mypkg-0.0.0-py3-none-any.whl
Archive:  dist/mypkg-0.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-02-27 22:10   mypkg/__init__.py
       11  2026-02-27 22:10   mypkg/linux/data.dat
       49  2026-02-27 22:12   mypkg-0.0.0.dist-info/METADATA
       91  2026-02-27 22:12   mypkg-0.0.0.dist-info/WHEEL
        6  2026-02-27 22:12   mypkg-0.0.0.dist-info/top_level.txt
      433  2026-02-27 22:12   mypkg-0.0.0.dist-info/RECORD
---------                     -------
      590                     6 files
```

After running `python -m build .` on Windows:

```
PS C:\tmp\platform_specific_package_data> unzip -l .\dist\mypkg-0.0.0-py3-none-any.whl
Archive:  .\dist\mypkg-0.0.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  2026-02-27 22:04   mypkg/__init__.py
       13  2026-02-27 22:04   mypkg/win32/data.dat
       54  2026-02-27 22:05   mypkg-0.0.0.dist-info/METADATA
       92  2026-02-27 22:05   mypkg-0.0.0.dist-info/WHEEL
        6  2026-02-27 22:05   mypkg-0.0.0.dist-info/top_level.txt
      433  2026-02-27 22:05   mypkg-0.0.0.dist-info/RECORD
---------                     -------
      598                     6 files
```
