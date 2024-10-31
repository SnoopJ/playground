This example shows off how to selective promote messages in a `logging` hierarchy into runtime exceptions based on their
logging level and/or the contents of the logged message.

My specific use-case is to catch warnings emitted by [PyInstaller] that in my personal usage are a very reliable
indicator that the build will be broken (generally because the invoking environment is not configured correctly).

[PyInstaller]: https://pyinstaller.readthedocs.io/


## Quiet-failure case

```
$ python3 main.py
531 INFO: PyInstaller: 6.7.0, contrib hooks: 2024.6
533 INFO: Python: 3.9.16
541 INFO: Platform: Linux-5.15.0-113-generic-x86_64-with-glibc2.35
544 INFO: wrote /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.spec
555 INFO: UPX is available but is disabled on non-Windows due to known compatibility problems.
557 INFO: Removing temporary files and cleaning cache in /home/snoopjedi/.cache/pyinstaller
560 WARNING: collect_data_files - skipping data collection for module 'thispackagedoesnotexist' as it is not a package.
561 WARNING: collect_dynamic_libs - skipping library collection for module 'thispackagedoesnotexist' as it is not a package.
============================================================================================================================
============= NOTE: in my use-cases, the above warnings are a surefire sign that something is wrong ========================
============================================================================================================================
902 INFO: Extending PYTHONPATH with paths
['/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal']
1410 INFO: checking Analysis
1411 INFO: Building Analysis because Analysis-00.toc is non existent
1411 INFO: Running Analysis Analysis-00.toc
```

## Promoted warning case

```
$ python3 main.py --promote-collection-warnings
663 INFO: PyInstaller: 6.7.0, contrib hooks: 2024.6
665 INFO: Python: 3.9.16
672 INFO: Platform: Linux-5.15.0-113-generic-x86_64-with-glibc2.35
674 INFO: wrote /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.spec
685 INFO: UPX is available but is disabled on non-Windows due to known compatibility problems.
686 INFO: Removing temporary files and cleaning cache in /home/snoopjedi/.cache/pyinstaller
Traceback (most recent call last):
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.py", line 61, in <module>
    main(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.py", line 56, in main
    run_pyinstaller(args)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/__main__.py", line 212, in run
    run_build(pyi_config, spec_file, **vars(args))
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/__main__.py", line 69, in run_build
    PyInstaller.building.build_main.main(pyi_config, spec_file, **kwargs)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/building/build_main.py", line 1189, in main
    build(specfile, distpath, workpath, clean_build)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/building/build_main.py", line 1129, in build
    exec(code, spec_namespace)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.spec", line 7, in <module>
    tmp_ret = collect_all('thispackagedoesnotexist')
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/utils/hooks/__init__.py", line 1086, in collect_all
    datas = collect_data_files(package_name, include_py_files, excludes=exclude_datas, includes=include_datas)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/.direnv/python-3.9.16/lib/python3.9/site-packages/PyInstaller/utils/hooks/__init__.py", line 803, in collect_data_files
    logger.warning("collect_data_files - skipping data collection for module '%s' as it is not a package.", package)
  File "/home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/logging/__init__.py", line 1458, in warning
    self._log(WARNING, msg, args, **kwargs)
  File "/home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/logging/__init__.py", line 1589, in _log
    self.handle(record)
  File "/home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/logging/__init__.py", line 1598, in handle
    if (not self.disabled) and self.filter(record):
  File "/home/snoopjedi/.pyenv/versions/3.9.16/lib/python3.9/logging/__init__.py", line 806, in filter
    result = f.filter(record)
  File "/var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/logging_/treat_library_warning_as_fatal/main.py", line 34, in filter
    raise Exception(record.getMessage())
Exception: collect_data_files - skipping data collection for module 'thispackagedoesnotexist' as it is not a package.
```
