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
DISABLE_SOURCE_TRANSFORM=1 python3 -m PyInstaller app.spec
160 INFO: PyInstaller: 6.2.0
160 INFO: Python: 3.9.14
163 INFO: Platform: Linux-5.15.0-88-generic-x86_64-with-glibc2.31
... snip ...
SKIPPING source transformation
47127 INFO: checking PYZ
47127 INFO: Building PYZ because PYZ-00.toc is non existent
47127 INFO: Building PYZ (ZlibArchive) /tmp/source_sandbox/build/app/PYZ-00.pyz
... snip ...
49771 INFO: checking COLLECT
49771 INFO: Building COLLECT because COLLECT-00.toc is non existent
49771 INFO: Building COLLECT COLLECT-00.toc
50552 INFO: Building COLLECT COLLECT-00.toc completed successfully.
python3 -m PyInstaller app.spec
152 INFO: PyInstaller: 6.2.0
152 INFO: Python: 3.9.14
155 INFO: Platform: Linux-5.15.0-88-generic-x86_64-with-glibc2.31
... snip ...
766 INFO: checking TransformedSourcePYZ
767 INFO: Building TransformedSourcePYZ because TransformedSourcePYZ-00.toc is non existent
... snip ...
9059 INFO: checking COLLECT
9062 INFO: Building COLLECT COLLECT-00.toc
9832 INFO: Building COLLECT COLLECT-00.toc completed successfully.


$ # in the unpatched bundle, TensorFlow's introspection cannot find the source (because the bundle does not include the .py file)
$ ./dist/app_broken/app_broken
WARNING:tensorflow:AutoGraph is not available in this environment: functions lack code information. This is typical of some environments like the interactive Python shell. See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/autograph/g3doc/reference/limitations.md#access-to-source-code for more information.
Source for object: <class 'libapp.widget.Widget'>
Traceback (most recent call last):
  File "main.py", line 10, in <module>
    src = inspect_utils.getimmediatesource(obj)
  File "patch.py", line 14, in _getimmediatesource
    return _getimmediatesource_original(obj)
  File "tensorflow/python/autograph/pyct/inspect_utils.py", line 142, in getimmediatesource
  File "inspect.py", line 835, in findsource
OSError: could not get source code
[636658] Failed to execute script 'main' due to unhandled exception!


$ # in the patched bundle, we hook TensorFlow's introspection to use the internalized source code whenever possible
$ ./dist/app/app
WARNING:tensorflow:AutoGraph is not available in this environment: functions lack code information. This is typical of some environments like the interactive Python shell. See https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/autograph/g3doc/reference/limitations.md#access-to-source-code for more information.
Source for object: <class 'libapp.widget.Widget'>
Using internalized source for <class 'libapp.widget.Widget'>
class Widget:
    def __init__(self, value):
        self.value = value

    __init__.__acme_source__ = 'def __init__(self, value):\n    self.value = value\n'


    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value!r})"

    __repr__.__acme_source__ = '\ndef __repr__(self):\n    return f"{self.__class__.__name__}(value={self.value!r})"\n'



---
Source for object: <function Widget.__init__ at 0x7f0cdbab0700>
['__acme_source__', '__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
Using internalized source for <function Widget.__init__ at 0x7f0cdbab0700>
def __init__(self, value):
    self.value = value


---
Source for object: <function Widget.__repr__ at 0x7f0cdbab0790>
['__acme_source__', '__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
Using internalized source for <function Widget.__repr__ at 0x7f0cdbab0790>

def __repr__(self):
    return f"{self.__class__.__name__}(value={self.value!r})"


---
Source for object: <function outer at 0x7f0cdb2cbca0>
['__acme_source__', '__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
Using internalized source for <function outer at 0x7f0cdb2cbca0>
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
