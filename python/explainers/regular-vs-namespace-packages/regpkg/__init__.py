print(f"executing regpkg/__init__.py (this module is called {__name__})")

# a regular package can import subpackages when imported (making those subpackages available without an explicit import)
# namespace packages cannot do this
from . import subpkg

# we can also "extract" values from subpackages, which can be extremely useful for providing a simple API
# to the user of your library while still keeping all your various components organized
from .subpkg import x

# we can also define values to live at the top level of our package
toplevel = "A value that lives at the top level of this 'regular' package"
