from glom import glom
from pprint import pprint

class ScopeInspectorSpec(object):
    def glomit(self, target, scope):
        pprint(dict(scope))
        return target

target = {'example': 'object'}

glom(target, ScopeInspectorSpec())
