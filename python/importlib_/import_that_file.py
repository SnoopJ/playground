TARGET_PATH = "/path/to/target.py"

## NOTE: deprecated (since Python 3.6) but more obvious way
# from importlib.machinery import SourceFileLoader
# 
# loader = SourceFileLoader("target_module", TARGET_PATH)
# mod = loader.load_module()

## NOTE: modern but marginally more annoying way
from importlib.util import module_from_spec, spec_from_file_location

spec = spec_from_file_location("target_module", TARGET_PATH)
mod = module_from_spec(spec)  # NOTE: creates an empty module
spec.loader.exec_module(mod)  # NOTE: populate that module by executing the target's code

print(mod)
print(f"{mod.x=}")
print(f"{mod.func(1)=}")
