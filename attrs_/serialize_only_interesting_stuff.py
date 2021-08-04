"""
A sample showing how to serialize only mandatory and non-default attributes on an attrs instance
"""
import typing as t

import attr


@attr.s(auto_attribs=True)
class Foo:
    """A simple object with some mandatory and optional fields"""
    x: str
    y: int = 42
    z: t.Optional[str] = None


@attr.s(auto_attribs=True)
class Bar:
    """A more structured attrs object that contains another"""
    foo: Foo
    name: str
    location: str = "Earth"


def filter_defaults(attrib: attr.Attribute, val) -> bool:
    if attrib.default is attr.NOTHING:
        # mandatory attributes are always included
        return True
    elif isinstance(attrib.default, attr.Factory):
        raise TypeError("This case exists, but I won't solve this (kinda tricky) general problem here")
    elif val != attrib.default:
        # field is optional, but was given a non-default value
        return True

    # field is both optional and default-valued, omit it
    return False



if __name__ == "__main__":
    foo = Foo("Hello there", y=-1)
    goo = Foo("O frabjous day!")

    bar = Bar(foo=foo, name="Aineko")
    var = Bar(foo=goo, name="Manfred", location="The Ring Imperium")


    print("attr.asdict(obj)")
    print("-------------")
    print(foo, attr.asdict(foo))
    print(goo, attr.asdict(goo))
    print(bar, attr.asdict(bar))
    print(var, attr.asdict(var))

    print("attr.asdict(obj, filter=...)")
    print("-------------")
    print(foo, attr.asdict(foo, filter=filter_defaults))
    print(goo, attr.asdict(goo, filter=filter_defaults))
    print(bar, attr.asdict(bar, filter=filter_defaults))
    print(var, attr.asdict(var, filter=filter_defaults))
