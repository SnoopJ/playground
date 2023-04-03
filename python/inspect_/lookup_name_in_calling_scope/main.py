from util import dispatch


def signature(*args, **kwargs) -> str:
    sig = ", ".join(repr(arg) for arg in args)
    if kwargs:
        sig += ", " + ", ".join(f"{key!r}={val!r}" for key,val in kwargs.items())
    return sig


def func_foo(*args, **kwargs):
    sig = signature(*args, **kwargs)
    print(f"foo({sig})")


def func_bar(*args, **kwargs):
    sig = signature(*args, **kwargs)
    print(f"bar({sig})")


def func(subcmd, *args, **kwargs):
    sig = signature(*args, **kwargs)
    if dispatch(subcmd, *args, **kwargs):
        print("was dispatched")
        return

    print(f"was NOT dispatched")


for subcmd in ("foo", "bar", "baz"):
    for arg in (42, 1337, -1):
        func(subcmd, arg, data="Twas brillig and the slithy toves")
    print('---\n')
