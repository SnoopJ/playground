from foo import Bar, MoveOnlyFoo, UMapStringCopyableMember as UMSCM
import foo

def test_copyable():
    copybar = Bar(UMSCM({"foo": 42, "bar": -1}))
    assert dict(copybar.m_map) == {"foo": 42, "bar": -1}
    copybar.m_map["foo"] = -1
    copybar.m_map["baz"] = 1337
    assert dict(copybar.m_map) == {"foo": -1, "bar": -1, "baz": 1337}

def test_moveonly():
    movebar = Bar("foo", 42)  # this makes a MoveOnlyMemberMap
    assert movebar.m_map  # we can only assert that the member map exists
