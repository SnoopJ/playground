import attr

@attr.s
class Foo:
    bar = attr.ib()
    baz = attr.ib()
    bic = attr.ib(default=42)

@attr.s
class Bar:
    bar = attr.ib()
    baz = attr.ib()

    @classmethod
    def from_foo(cls, other):
        fields = [a.name for a in attr.fields(cls)]
        vals = {name:getattr(other, name) for name in fields}
        return cls(**vals)

if __name__ == "__main__":
    f = Foo([1,2,3], "baz")
    b = Bar.from_foo(f)
    print(f)
    print(b)


