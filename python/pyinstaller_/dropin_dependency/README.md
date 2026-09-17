This example shows off how to configure a PyInstaller distribution to depend on a separately-vendored dependency
that will be installed ad-hoc into a folder (`vendor/`) next to the main executable

```
14:25 [jgerity@giskard ~/playground/python/pyinstaller_/dropin_dependency (main 2026-03-24 *⏳)]
$ make bundle
python3 -m PyInstaller --noconfirm app.spec
63 INFO: PyInstaller: 6.22.3, contrib hooks: 2026.7
63 INFO: Python: 3.9.25
...
3777 INFO: Build complete! The results are available in: /home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist
mkdir dist/app/vendor

$ ./dist/app/app  # confirm that the dependency is not available
Inserting vendor path on sys.path: PosixPath('/home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist/app/vendor')
Cannot import acme

$ cp acme.py dist/app/vendor/  # install the ad-hoc dependency

$ ./dist/app/app  # re-run to confirm that the dependency can be loaded
Inserting vendor path on sys.path: PosixPath('/home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist/app/vendor')
Loaded acme from '/home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist/app/vendor/acme.py'
arf arf!
```

This approach also works with [the `--target` option to `pip install`](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-t)
if the dependency to be provided is installable by `pip`:

```
$ rm -fr ./dist/app/vendor/*  # wipe the slate clean
$ pip install --target ./dist/app/vendor acme-1.0-py2.py3-none-any.whl  # demonstrate that we can install such a dependency from a wheel, too
$ ./dist/app/app  # re-run to confirm that the dependency can be loaded
Inserting vendor path on sys.path: PosixPath('/home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist/app/vendor')
Loaded acme from '/home/jgerity/personal/playground/python/pyinstaller_/dropin_dependency/dist/app/vendor/acme.py'
arf arf!

```
