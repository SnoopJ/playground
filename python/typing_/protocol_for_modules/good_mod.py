someattr = "This is a string attribute required by the module interface"

unconstrained_attr = "This attribute is not part of ModuleProto, but is allowed"

def func1(x: int) -> str:
    return "A string"

def func2() -> None:
    return


def unconstrained_func() -> None:
    print("This function isn't part of ModuleProto, but is allowed")
