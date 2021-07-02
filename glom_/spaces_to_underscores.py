from pprint import pprint

from glom import *

data = {
        "foo object": {
            "taco": 42,
            "property with spaces": -1,
        },
        "bar": {
            "taco": 42,
            "some other property with spaces": "This value shouldn't have its spaces modified",
        },
        "O frabjous day!": {
            "taco": 42,
            "yet another member with spaces!": "Callooh! Callay!",
        },
}

from typing import Callable, Optional

class RenameKeys:
    def __init__(self, fn: Optional[Callable[[str], str]]=None, **kwargs: str):
        self._fn = fn or (lambda val: val)
        self._rename_map = kwargs

    def glomit(self, target, scope):
        if isinstance(target, dict):
            # blegh, I don't like the recursion here, why even use glom then?!
            return {self._fn(k):self.glomit(v, scope) for k,v in target.items()}
        else:
            return target

if __name__ == "__main__":
    spec = Switch({
        dict: RenameKeys(lambda k: k.replace(" ", "_"))
                })
    result = glom(data, spec)
    pprint(result)
