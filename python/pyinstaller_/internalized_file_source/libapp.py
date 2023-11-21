class Widget:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value!r})"


def outer():
    print('outer()')
    def inner():
        """An inner docstring"""
        print('inner()')
        print("another print using double-quotes just to be sure")
    inner()
