from typing import Protocol


class ModuleProto(Protocol):
    """
    This Protocol requires a particular interface for a module
    """
    someattr: str
    def func1(self, x: int) -> str: ...
    def func2(self) -> None: ...


def consume_module(mod: ModuleProto):
    """A helper to give us somewhere to hang our annotation"""
    pass


import good_mod
import bad_mod

consume_module(good_mod)   # valid
consume_module(bad_mod)    # invalid: func1() has the wrong type; func2(), someattr are missing
