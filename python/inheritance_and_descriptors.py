"""
Based on a question in Libera.net #python on 16 Dec 2021 about calling the setter
of a base class's @property from the derived class
"""
class Base:
    def __init__(self, foo=-1):
        self._foo = foo

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, val):
        self._foo = val


class Derived(Base):
    @property
    def foo(self):
        print("hello from Derived.foo() getter")
        return super().foo

    @foo.setter
    def foo(self, val):
        print("hello from Derived.foo() setter")
        # the naive approach doesn't work:
        # super().foo = val

        # you can instead do:
        # super(self.__class__, self.__class__).foo.fset(self, val)

        # this spelling (thanks to dabeaz) handles non-property descriptors too, see: https://bugs.python.org/issue14965#msg179217
        super(self.__class__, self.__class__).foo.__set__(self, val)


if __name__ == "__main__":
    d = Derived()
    print(d.foo)
    d.foo = 42
    print(d.foo)
