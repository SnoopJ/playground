from packaging.version import Version
from packaging.requirements import Requirement
from packaging.specifiers import Specifier, SpecifierSet


def drop_local_from_req(req: Requirement) -> Requirement:
    """
    Drop `local` field from any version specifiers in the given `Requirement`

    NOTE: handles multiple specifiers, extras, environment markers, but the local
    version identifier is dropped from *ALL* specifiers present
    """
    result = Requirement(str(req))  # take a copy
    newspecs = []
    for spec in req.specifier:
        newver = Version(spec.version).public
        ns = Specifier(spec.operator + newver)
        newspecs.append(ns)

    # I regret to say that mutation of a `Requirement` object is the solution
    # to this problem with which I am most satisfied.
    #
    # Unfortunately, the official `packaging` API does not provide very good
    # primitives for this, you end up routing through `str` a bunch of times
    # (see silly copy idiom above). If it were possible to create a `Specifier`
    # like:
    #
    #     Specifier(operator="==", version="1.2.3")
    #
    # and a `Requirement` like:
    #
    #     Requirement(name="pkg", specifier=specifier, extras=…, markers=…)
    #
    # then this could be written in a way I find much more satisfying. But as it
    # stands, this is the best I can do.
    result.specifier = SpecifierSet(','.join(map(str, newspecs)))

    return result


if __name__ == "__main__":
    req = Requirement('pkg[ex1, ex2]==1.2.3.dev+local, <2; sys.platform == "Windows" or sys.platform == "BeOS"')
    new_req = drop_local_from_req(req)
    print(f"Before: {str(req)!r}")
    print(f"After:  {str(new_req)!r}")
