import zipimport
from textwrap import indent


imp = zipimport.zipimporter("otherlib.zip")

print("> Source listing of module otherlib from otherlib.zip")
src = indent(imp.get_source("otherlib"), prefix="    ")
print("```python\n" + src + "```")

print("> Importing otherlib")
otherlib = imp.load_module("otherlib")


if __name__ == "__main__":
    print("> Running otherlib.bark()")
    otherlib.bark()
