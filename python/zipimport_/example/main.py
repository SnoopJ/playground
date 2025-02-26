print("> Attempting to import otherlib")
try:
    import otherlib
except ImportError:
    print("> Failed")

import sys
print("> Inserting otherlib.zip to sys.path")
sys.path.insert(0, "otherlib.zip")

print("> Importing otherlib")
import otherlib
print("> Succeeded")


if __name__ == "__main__":
    print("> Running otherlib.bark()")
    otherlib.bark()
