import attr

def type_validator(self, attr, val):
    if not isinstance(val, attr.type):
        raise TypeError(f"Attribute {attr.name} must be of type {attr.type}, got {type(val)}")

@attr.s
class Foo:
    x: int = attr.ib(validator=type_validator)
    y: str = attr.ib(validator=type_validator)
    z: bool = attr.ib(default=False, validator=type_validator)


def pick_class(cls, pick):
    picked = {f.name:f for f in attr.fields(cls) if f.name in pick}

    return attr.make_class(f"Pick{cls.__name__}", picked)

PickFoo = pick_class(Foo, ('x', 'z'))

# the default value of z is retained
pf = PickFoo(x=-1)

# the validators are retained, this is a TypeError
# pf = PickFoo(x=42, z="foo")
