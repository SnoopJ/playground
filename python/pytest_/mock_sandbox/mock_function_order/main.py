def funcA():
    print("Hello from function A")


def funcB(x: int):
    print("Hello from function B")


def funcC():
    print("Hello from function C")


def good_run():
    funcA()
    funcB(42)
    funcC()


def bad_run():
    funcA()
    funcC()
    funcB(42)
