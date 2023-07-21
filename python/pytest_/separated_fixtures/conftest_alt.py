# this alternate conftest.py shows off how to discover fixture modules instead
# of listing them explicitly, which is a more clever (pejorative) way to do it
from pathlib import Path


HERE = Path(__file__).parent
FIXTURES = Path(HERE, "fixtures")

def _scan_fixtures():
    """
    Look for .py files under fixtures/ and yield fully qualified plugin
    names for them
    """
    for pth in FIXTURES.glob("**/*.py"):
        yield ".".join(pth.relative_to(HERE).with_suffix('').parts)


pytest_plugins = list(_scan_fixtures())
