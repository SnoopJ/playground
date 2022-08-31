from pathlib import Path

HERE = Path(__file__).parent.resolve()
TARGET_PATH = HERE.joinpath("target.py")

## NOTE: deprecated (since Python 3.6) but more obvious way
# from importlib.machinery import SourceFileLoader
# 
# loader = SourceFileLoader("target_module", TARGET_PATH)
# mod = loader.load_module()

## NOTE: modern but marginally more annoying way
from importlib.util import module_from_spec, spec_from_file_location

def import_that_file(pth):
    spec = spec_from_file_location("target_module", pth)
    mod = module_from_spec(spec)  # NOTE: creates an empty module
    spec.loader.exec_module(mod)  # NOTE: populate that module by executing the target's code
    return mod

mod = import_that_file(TARGET_PATH)

print(mod)
print(f"mod.x = {mod.x}")
print(f"mod.func(1) = {mod.func(1)}")

## NOTE: the module above is not cached in sys.modules, you should be able to hot-reload without fuss!
# import sys
# from pprint import pprint
# pprint(sorted(sys.modules.keys()))
