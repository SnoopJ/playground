.. code-block:: python

    >>> class Foo:
    ...   def __init__(self, marker):
    ...     self.marker = marker  # store the marker the user gave us on this instance (`self`)
    ...
    ...   def bar(self, x):
    ...     print(f"Foo.bar() called for Foo object with marker={self.marker}, x={x}")
    ...

    >>> Foo.bar(42)  # because we're calling this method _on the class_, there is
                     # no instance for the interpreter to pass for us, we have to
                     # do that ourselves. we didn't here, so this is an error
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: bar() missing 1 required positional argument: 'x'

    >>> first_foo = Foo("the first of many")  # here we create an instance of the
                                              # class by calling the class object
                                              # (which does a bunch of things, one
                                              # of which is calling __init__ for
                                              # that instance)

    >>> Foo.marker  # the class does not have this attribute, so this is an AttributeError...
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: type object 'Foo' has no attribute 'marker'


    >>> first_foo.marker  # ...but instances do, because it is set during their
                          # initialization (the code we wrote in __init__)
    'the first of many'

    >>> second_foo = Foo("foo strikes back")
    >>> first_foo.marker  # creating a second instance of Foo does not change the previous instance
    'the first of many'

    >>> second_foo.marker  # each of these instances has its own state, which in
                           # this case is the marker data we passed in during
                           # initialization
    'foo strikes back'

    >>> first_foo.bar(42)  # here, we are calling the bar() method on _an instance_
                           # of this class; Python will pass `first_foo` as the
                           # first argument (we called it `self`) and the rest (42, named `x`)
                           # will follow
    Foo.bar() called for Foo object with marker=the first of many, x=42

    >>> Foo.bar(first_foo, 42)  # this is basically what the interpreter does for
                                # us when we call an instance method on an instance
    Foo.bar() called for Foo object with marker=the first of many, x=42

    >>> Foo.bar(second_foo, -1)  # if we passed a different instance...
    Foo.bar() called for Foo object with marker=foo strikes back, x=-1

    >>> second_foo.bar(-1)  # ...it will pass that instance for `self`. This is the same as calling it directly on the instance
    Foo.bar() called for Foo object with marker=foo strikes back, x=-1
