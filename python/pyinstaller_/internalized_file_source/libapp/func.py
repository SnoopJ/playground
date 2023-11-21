def outer():
    print('outer()')
    def inner():
        """An inner docstring"""
        print('inner()')
        print("another print using double-quotes just to be sure")
    inner()

