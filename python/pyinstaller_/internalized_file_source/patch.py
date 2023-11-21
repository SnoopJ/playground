#####
# Patch tensorflow's getimmediatesource() to use internalized source where possible
#####
from tensorflow.python.autograph.pyct import inspect_utils


_getimmediatesource_original = inspect_utils.getimmediatesource
def _getimmediatesource(obj):
    if hasattr(obj, "__acme_source__"):
        print(f"Using internalized source for {obj}")
        return obj.__acme_source__
    else:
        return _getimmediatesource_original(obj)
inspect_utils.getimmediatesource = _getimmediatesource



