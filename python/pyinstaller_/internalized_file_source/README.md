This is a proof-of-concept of using [`libCST`](https://pypi.org/project/libcst/)
to internalize the source code of functions and classes in a way that allows
them to be located by TensorFlow's [AutoGraph](https://www.tensorflow.org/api_docs/python/tf/autograph)
functionality even if the `.py` files are not included in the final PyInstaller
distribution.

This involves doing some source tree transformation to stash the source of each
function/class inside of the `__acme_source__` attribute on the resulting object.
This _does_ result in some slightly different code as observed by AutoGraph,
in that classes and nested functions will see additional assignment statements,
but this should have a marginal effect on the resulting computational graphs
at most.

```
$ make
mkdir -p staging/
cp libapp.py main.py staging/
env -C staging/\
        python3 -m PyInstaller \
                --distpath ../dist \
                --workpath ../build \
                --name app \
                libapp.py \
                main.py
168 INFO: PyInstaller: 6.2.0
168 INFO: Python: 3.9.14
172 INFO: Platform: Linux-5.15.0-88-generic-x86_64-with-glibc2.31
... snip ...
50316 INFO: Building COLLECT because COLLECT-00.toc is non existent
50316 INFO: Building COLLECT COLLECT-00.toc
51181 INFO: Building COLLECT COLLECT-00.toc completed successfully.
mkdir -p transformed/
python3 transform_source.py libapp.py > transformed/libapp.py
cp patch.py transformed/libapp.py main.py staging/
env -C staging/\
        python3 -m PyInstaller \
                --distpath ../dist \
                --workpath ../build \
                --name app_patched \
                patch.py \
                libapp.py \
                main.py
197 INFO: PyInstaller: 6.2.0
197 INFO: Python: 3.9.14
201 INFO: Platform: Linux-5.15.0-88-generic-x86_64-with-glibc2.31
... snip ...
51086 INFO: Building COLLECT because COLLECT-00.toc is non existent
51086 INFO: Building COLLECT COLLECT-00.toc
51927 INFO: Building COLLECT COLLECT-00.toc completed successfully.


$ # in the unpatched bundle, TensorFlow's introspection cannot find the source (because the bundle does not include the .py file)
$ ./dist/app/app
WARNING:tensorflow:AutoGraph is not available in this environment: functions lack code information. This is typical of some environments like the interactive Python shell. See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/autograph/g3doc/reference/limitations.md#access-to-source-code for more information.
Source for object: <class 'libapp.Widget'>
Traceback (most recent call last):
  File "main.py", line 9, in <module>
    src = inspect_utils.getimmediatesource(obj)
  File "tensorflow/python/autograph/pyct/inspect_utils.py", line 142, in getimmediatesource
  File "inspect.py", line 835, in findsource
OSError: could not get source code
[515203] Failed to execute script 'main' due to unhandled exception!
20:29 [jgerity@giskard /tmp/source_sandbox]


$ # in the patched bundle, we hook TensorFlow's introspection to use the internalized source code whenever possible
$ ./dist/app_patched/app_patched
WARNING:tensorflow:AutoGraph is not available in this environment: functions lack code information. This is typical of some environments like the interactive Python shell. See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/autograph/g3doc/reference/limitations.md#access-to-source-code for more information.
Source for object: <class 'libapp.Widget'>
Using internalized source for <class 'libapp.Widget'>
class Widget:
    def __init__(self, value):
        self.value = value

    __init__.__acme_source__ = 'def __init__(self, value):\n    self.value = value\n'


    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value!r})"

    __repr__.__acme_source__ = '\ndef __repr__(self):\n    return f"{self.__class__.__name__}(value={self.value!r})"\n'



---
Source for object: <function Widget.__init__ at 0x7f9d47e91af0>
Using internalized source for <function Widget.__init__ at 0x7f9d47e91af0>
def __init__(self, value):
    self.value = value


---
Source for object: <function Widget.__repr__ at 0x7f9d47e91b80>
Using internalized source for <function Widget.__repr__ at 0x7f9d47e91b80>

def __repr__(self):
    return f"{self.__class__.__name__}(value={self.value!r})"


---
Source for object: <function outer at 0x7f9d47e91940>
Using internalized source for <function outer at 0x7f9d47e91940>


def outer():
    print('outer()')
    def inner():
        """An inner docstring"""
        print('inner()')
        print("another print using double-quotes just to be sure")

    inner.__acme_source__ = 'def inner():\n    """An inner docstring"""\n    print(\'inner()\')\n    print("another print using double-quotes just to be sure")\n'

    inner()


---
all good :)
```
