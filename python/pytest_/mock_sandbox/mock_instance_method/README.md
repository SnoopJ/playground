This example shows off an approach to mocking a single instance on a target
class in a way that still provides access to the "real" instance.

I originally tried patching the method on the original class _directly_, but
found myself needing access to the true instance and unable to get it that way.
After thinking about it a bit, I realized patching the class itself with a
subclass was a better fit to the task


```
$ python3 -m pytest -rP
=============================== test session starts ===============================
platform linux -- Python 3.9.16, pytest-8.3.2, pluggy-1.5.0
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/mock_sandbox/mock_instance_method
plugins: anyio-4.4.0
collected 2 items                                                                 

test_main.py ..                                                             [100%]

===================================== PASSES ======================================
____________________________________ test_main ____________________________________
------------------------------ Captured stdout call -------------------------------
Inside real func method:
        self = <main.RealClass object at 0x7f99b9436fd0>,
        self.data = 0
Performing some stateful activity, self.data = 1
Inside real func method:
        self = <main.RealClass object at 0x7f99b9436fd0>,
        self.data = 1
Performing some stateful activity, self.data = 2
Inside real func method:
        self = <main.RealClass object at 0x7f99b9436fd0>,
        self.data = 2
Performing some stateful activity, self.data = 3
_________________________________ test_main_fake __________________________________
------------------------------ Captured stdout call -------------------------------
Inside fake method (elapsed time: 0:00:00.000016):
        self = <test_main.FakeClass object at 0x7f99b9436d30>,
        self.data = 0
Performing some stateful activity, self.data = 1
Inside fake method (elapsed time: 0:00:00.000083):
        self = <test_main.FakeClass object at 0x7f99b9436d30>,
        self.data = 1
Performing some stateful activity, self.data = 2
Inside fake method (elapsed time: 0:00:00.000104):
        self = <test_main.FakeClass object at 0x7f99b9436d30>,
        self.data = 2
Performing some stateful activity, self.data = 3
================================ 2 passed in 0.07s ================================
```
