from pathlib import Path


# this Path object points to the directory this module lives in
HERE = Path(__file__).parent

# the __file__ attribute on a module is a string containing the path to
# the file this module was loaded from
# https://docs.python.org/3/reference/import.html#file__


# we can now use HERE to locate files relative to this module
FOO_PATH = HERE.joinpath("foo.txt")
BAR_PATH = HERE.joinpath("subdir", "bar.txt")

print("Contents of foo.txt:")
print(FOO_PATH.read_text())

print("Contents of bar.txt:")
print(BAR_PATH.read_text())
