import sys
from pathlib import Path

import pytest


HERE = Path(__file__).parent.resolve()


IS_BUNDLE = getattr(sys, "frozen", False)

if IS_BUNDLE:
    TESTSDIR = Path(HERE, "tests")
else:
    TESTSDIR = HERE


if __name__ == "__main__":
    pytest.main(["-v", TESTSDIR.resolve()])
